# MarketPulse Frontend v2 Schema Fixed

This frontend is aligned with the MarketPulse backend v4 JSON schema.

Main data file:
data/market_pulse_combined.json

Expected backend fields:
- group.market_group
- group.display_name
- group.benchmark_symbol
- group.group_signals.weekly/monthly/annual
- item.last_close
- item.price_source = close
- item.returns.daily/weekly/monthly/annual/mtd/ytd/r1m/r3m/r6m/r1y
- item.technicals.weekly/monthly/annual
- item.signals.weekly/monthly/annual.combined_signal

Run locally:
python -m http.server 8080
