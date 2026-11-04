#!/usr/bin/env python3

import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config/rotation_universe.json"
FLAT = ROOT / "data/market_pulse_flat.json"
OUT = ROOT / "data/rotation"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("rotation")


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write("\n")


def last_completed_friday():
    today = datetime.now(timezone.utc).date()
    days_back = (today.weekday() - 4) % 7
    if days_back == 0:
        days_back = 7
    return pd.Timestamp(today - timedelta(days=days_back))


def get_market_symbols(config, flat):
    markets = config["markets"]
    result = {}

    for key, market in markets.items():
        if "constituents" in market:
            symbols = list(market["constituents"])
        else:
            symbols = []
            for row in flat:
                if market.get("geography_bucket"):
                    match = (
                        row.get("geography_bucket")
                        == market["geography_bucket"]
                    )
                else:
                    match = (
                        row.get("market_group")
                        == market.get("market_group")
                    )

                if match and row.get("symbol"):
                    symbols.append(row["symbol"])

            symbols = list(dict.fromkeys(symbols))

        benchmark = market["benchmark"]
        symbols = [
            s for s in symbols
            if s != benchmark
        ]

        result[key] = {
            "config": market,
            "symbols": symbols,
            "benchmark": benchmark
        }

    return result



def extract_ticker_frame(download, ticker):
    if download is None or download.empty:
        return pd.DataFrame()

    if isinstance(download.columns, pd.MultiIndex):
        for level in range(download.columns.nlevels):
            values = download.columns.get_level_values(level)
            if ticker in values:
                frame = download.xs(
                    ticker, axis=1, level=level, drop_level=True
                )
                if isinstance(frame, pd.Series):
                    frame = frame.to_frame()
                if isinstance(frame.columns, pd.MultiIndex):
                    frame.columns = frame.columns.get_level_values(-1)
                return frame.copy()

        return pd.DataFrame()

    return download.copy()


def normalize_history(frame, ticker):
    if frame is None or frame.empty:
        return pd.DataFrame()

    frame = frame.copy()

    if isinstance(frame.columns, pd.MultiIndex):
        return pd.DataFrame()

    frame.columns = [
        str(c).strip().title() for c in frame.columns
    ]

    required = ["Open", "High", "Low", "Close", "Volume"]
    if not all(c in frame.columns for c in required):
        return pd.DataFrame()

    frame = frame[required].copy()
    frame.index = pd.to_datetime(frame.index)

    if frame.index.tz is not None:
        frame.index = frame.index.tz_localize(None)

    frame = frame.sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    frame = frame.dropna(subset=["Close"])
    frame["Volume"] = pd.to_numeric(
        frame["Volume"], errors="coerce"
    ).fillna(0)

    if frame.empty:
        return pd.DataFrame()

    return frame


def download_one(ticker):
    for attempt in range(1, 4):
        try:
            raw = yf.download(
                ticker,
                period="5y",
                interval="1d",
                auto_adjust=True,
                progress=False,
                threads=False,
                repair=False,
                timeout=30
            )

            frame = extract_ticker_frame(raw, ticker)
            frame = normalize_history(frame, ticker)

            if not frame.empty:
                log.info(
                    "Downloaded %s: %d daily rows",
                    ticker, len(frame)
                )
                return frame

            log.warning(
                "%s returned no usable data (attempt %d)",
                ticker, attempt
            )

        except Exception as exc:
            log.warning(
                "%s download failed (attempt %d): %s",
                ticker, attempt, exc
            )

    return pd.DataFrame()


def download_history(symbols):
    symbols = list(dict.fromkeys(symbols))
    history = {}

    for start in range(0, len(symbols), 10):
        batch = symbols[start:start + 10]
        log.info("Downloading batch %d: %d symbols",
                 start // 10 + 1, len(batch))

        batch_ok = False

        try:
            raw = yf.download(
                tickers=batch,
                period="5y",
                interval="1d",
                auto_adjust=True,
                group_by="ticker",
                progress=False,
                threads=False,
                repair=False,
                timeout=45
            )

            if raw is not None and not raw.empty:
                for ticker in batch:
                    try:
                        frame = extract_ticker_frame(raw, ticker)
                        frame = normalize_history(frame, ticker)

                        if not frame.empty:
                            history[ticker] = frame
                            log.info(
                                "Batch OK: %s (%d rows)",
                                ticker, len(frame)
                            )
                    except Exception as exc:
                        log.warning(
                            "Extraction failed for %s: %s",
                            ticker, exc
                        )

                batch_ok = True

        except Exception as exc:
            log.warning("Batch download failed: %s", exc)

        # Recover missing tickers individually.
        missing = [s for s in batch if s not in history]

        if missing:
            log.warning(
                "Individual fallback for %d tickers: %s",
                len(missing), ", ".join(missing)
            )

            for ticker in missing:
                frame = download_one(ticker)
                if not frame.empty:
                    history[ticker] = frame

        if not batch_ok:
            log.warning("Batch %d required individual recovery",
                        start // 10 + 1)

    log.info(
        "Download summary: %d of %d tickers retrieved",
        len(history), len(symbols)
    )

    return history

def weekly_bars(frame, cutoff):
    if frame is None or frame.empty:
        return pd.DataFrame()

    daily = frame.loc[frame.index <= cutoff].copy()
    if daily.empty:
        return pd.DataFrame()

    weekly = daily.resample("W-FRI").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    weekly = weekly.dropna(subset=["Close"])
    weekly = weekly.loc[weekly.index <= cutoff]

    return weekly


def history_status(count):
    if count >= 52:
        return "standard"
    if count >= 26:
        return "adaptive"
    if count >= 13:
        return "limited"
    if count >= 3:
        return "very_limited"
    return "insufficient"


def quadrant(rs, momentum):
    if rs is None or momentum is None:
        return "unavailable"

    if rs >= 100 and momentum >= 100:
        return "leading"
    if rs >= 100 and momentum < 100:
        return "weakening"
    if rs < 100 and momentum < 100:
        return "lagging"
    return "improving"


def rrg_series(asset, benchmark, volume=False):
    joined = pd.concat(
        [asset, benchmark],
        axis=1,
        keys=["asset", "benchmark"]
    ).dropna()

    if len(joined) < 3:
        return pd.DataFrame()

    if volume:
        # Weekly dollar turnover = weekly close * weekly summed volume.
        asset_turnover = (
            joined[("asset", "Close")]
            * joined[("asset", "Volume")]
        )
        benchmark_turnover = (
            joined[("benchmark", "Close")]
            * joined[("benchmark", "Volume")]
        )

        asset_participation = (
            asset_turnover /
            asset_turnover.rolling(52, min_periods=13).mean()
        )
        benchmark_participation = (
            benchmark_turnover /
            benchmark_turnover.rolling(52, min_periods=13).mean()
        )

        relative = (
            asset_participation /
            benchmark_participation
        ) * 100

        # The volume series is explicitly a relative participation measure.
        rs = relative
    else:
        relative = (
            joined[("asset", "Close")]
            / joined[("benchmark", "Close")]
        )

        baseline = relative.rolling(52, min_periods=26).mean()
        rs = (relative / baseline) * 100

    momentum = (rs / rs.shift(13)) * 100

    result = pd.DataFrame({
        "rs_ratio": rs,
        "rs_momentum": momentum
    }).replace([np.inf, -np.inf], np.nan).dropna()

    return result


def rrg_point(series, display_cap=None):
    if series is None or series.empty:
        return None

    trail = []
    for date, row in series.tail(12).iterrows():
        raw_rs = float(row["rs_ratio"])
        raw_mom = float(row["rs_momentum"])

        point = {
            "date": date.strftime("%Y-%m-%d"),
            "rs_ratio": round(raw_rs, 4),
            "rs_momentum": round(raw_mom, 4),
            "quadrant": quadrant(raw_rs, raw_mom)
        }

        if display_cap is not None:
            point["display_rs_ratio"] = min(raw_rs, display_cap)
            point["display_rs_momentum"] = min(raw_mom, display_cap)
            point["display_capped"] = (
                raw_rs > display_cap or raw_mom > display_cap
            )
            point["display_marker"] = (
                "↑" if point["display_capped"] else ""
            )
            point["display_warning"] = (
                "Value exceeds visual chart ceiling; raw value retained"
                if point["display_capped"] else ""
            )

        trail.append(point)

    latest = trail[-1]
    latest = dict(latest)
    latest["trail"] = trail

    return latest


def pivot_levels(previous):
    high = float(previous["High"])
    low = float(previous["Low"])
    close = float(previous["Close"])

    pivot = (high + low + close) / 3
    return {
        "pivot": round(pivot, 4),
        "s1": round(2 * pivot - high, 4),
        "s2": round(pivot - (high - low), 4),
        "r1": round(2 * pivot - low, 4),
        "r2": round(pivot + (high - low), 4)
    }


def build_item(
    symbol,
    name,
    asset,
    benchmark,
    benchmark_symbol,
    currency_warning=False
):
    common = {
        "symbol": symbol,
        "name": name,
        "benchmark": benchmark_symbol,
        "data_status": "available"
    }

    if asset is None or asset.empty:
        return {
            **common,
            "data_status": "missing_history",
            "return_status": "insufficient",
            "volume_status": "insufficient",
            "return_rrg": None,
            "volume_rrg": None
        }

    aligned = asset.join(
        benchmark[["Close"]].rename(
            columns={"Close": "Benchmark_Close"}
        ),
        how="inner"
    ) if benchmark is not None and not benchmark.empty else pd.DataFrame()

    if aligned.empty:
        return {
            **common,
            "data_status": "benchmark_unavailable",
            "return_status": "insufficient",
            "volume_status": "insufficient",
            "return_rrg": None,
            "volume_rrg": None
        }

    count = len(aligned)
    status = history_status(count)

    item = {
        **common,
        "data_status": "available",
        "return_status": status,
        "volume_status": status,
        "history_weeks": count,
        "history_mode": status,
        "history_caution": (
            None if status == "standard"
            else f"Only {count} aligned completed weekly observations"
        )
    }

    return_data = rrg_series(asset, benchmark, volume=False)
    volume_data = rrg_series(asset, benchmark, volume=True)

    item["return_rrg"] = rrg_point(return_data)
    item["volume_rrg"] = rrg_point(
        volume_data,
        display_cap=200
    )

    if item["volume_rrg"]:
        raw_points = item["volume_rrg"]["trail"]
        capped = any(p["display_capped"] for p in raw_points)
        item["volume_display_ceiling"] = 200
        item["volume_display_capped"] = capped
        item["volume_display_marker"] = "↑" if capped else ""
        item["volume_display_warning"] = (
            "Visual ceiling only; raw values and quadrant are unchanged"
            if capped else ""
        )

    latest_date = aligned.index[-1]
    item["last_week"] = {
        "date": latest_date.strftime("%Y-%m-%d"),
        "close": round(float(aligned["Close"].iloc[-1]), 4),
        "benchmark_close": round(
            float(aligned["Benchmark_Close"].iloc[-1]), 4
        )
    }

    item["weekly_ma18"] = (
        round(float(asset["Close"].tail(18).mean()), 4)
        if len(asset) >= 18 else None
    )

    item["weekly_ma18_position"] = (
        "Above MA18"
        if item["weekly_ma18"] is not None
        and item["last_week"]["close"] > item["weekly_ma18"]
        else "Below MA18"
        if item["weekly_ma18"] is not None
        else "Insufficient history"
    )

    if len(asset) >= 2:
        item["weekly_pivot"] = pivot_levels(asset.iloc[-2])
    else:
        item["weekly_pivot"] = None

    if currency_warning:
        item["currency_note"] = (
            "INR-denominated instrument; not FX-adjusted against "
            "the CAD-denominated commodity benchmark."
        )

    return item


def main():
    config = read_json(CONFIG)
    flat = read_json(FLAT)
    markets = get_market_symbols(config, flat)

    all_symbols = []
    for market in markets.values():
        all_symbols.extend(market["symbols"])
        all_symbols.append(market["benchmark"])

    all_symbols = list(dict.fromkeys(all_symbols))

    log.info("Total distinct tickers: %d", len(all_symbols))

    daily_history = download_history(all_symbols)

    cutoff = last_completed_friday()
    log.info("Last completed Friday: %s", cutoff.date())

    weekly_history = {
        symbol: weekly_bars(frame, cutoff)
        for symbol, frame in daily_history.items()
    }

    master = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "latest_completed_week": cutoff.strftime("%Y-%m-%d"),
        "methodology": config["methodology"],
        "markets": {}
    }

    errors = []

    flat_by_symbol = {
        row.get("symbol"): row
        for row in flat
        if row.get("symbol")
    }

    for key, market in markets.items():
        benchmark_symbol = market["benchmark"]
        benchmark = weekly_history.get(benchmark_symbol)

        benchmark_ok = (
            benchmark is not None and not benchmark.empty
        )

        items = []

        for symbol in market["symbols"]:
            source = flat_by_symbol.get(symbol, {})
            name = source.get("name", symbol)

            if key == "commodities":
                name = source.get("name", symbol)

            item = build_item(
                symbol=symbol,
                name=name,
                asset=weekly_history.get(symbol),
                benchmark=benchmark,
                benchmark_symbol=benchmark_symbol,
                currency_warning=(
                    symbol in market["config"].get(
                        "currency_warning_symbols", []
                    )
                )
            )
            items.append(item)

        output = {
            "market": key,
            "market_group": market["config"]["name"],
            "benchmark": benchmark_symbol,
            "benchmark_status": (
                "available" if benchmark_ok else "missing"
            ),
            "benchmark_latest_week": (
                benchmark.index[-1].strftime("%Y-%m-%d")
                if benchmark_ok else None
            ),
            "generated_at": master["generated_at"],
            "methodology": config["methodology"],
            "count": len(items),
            "items": items
        }

        write_json(OUT / f"{key}.json", output)

        master["markets"][key] = {
            "benchmark": benchmark_symbol,
            "benchmark_status": output["benchmark_status"],
            "count": len(items),
            "file": f"{key}.json"
        }

        log.info(
            "%s: %d constituents; benchmark %s",
            key, len(items), output["benchmark_status"]
        )

        if not benchmark_ok:
            errors.append(f"{key}: benchmark {benchmark_symbol} unavailable")

    write_json(OUT / "rotation_master.json", master)

    summary = {
        "generated_at": master["generated_at"],
        "latest_completed_week": cutoff.strftime("%Y-%m-%d"),
        "markets": master["markets"],
        "errors": errors
    }
    write_json(OUT / "validation_report.json", summary)

    if errors:
        log.error("One or more market benchmarks are unavailable")
        sys.exit(2)

    log.info("Rotation data generation completed")


if __name__ == "__main__":
    main()
