# MarketPulse Price RRG + VSA update

## Design
- Weekly Price RRG: sector leadership and established relative strength.
- Daily Price RRG: emerging relative-strength rotation.
- Daily VSA and Weekly VSA: separate volume-spread evidence used to confirm or question the price rotation.
- Volume RRG has been removed from the rotation calculation and Technical Summary presentation.
- `return_rrg` remains as a backward-compatible alias for `weekly_price_rrg`.

## Calculation methodology
- Daily Price RRG: relative close / benchmark close; 126-observation rolling baseline (minimum 63); 20-observation relative-momentum comparison.
- Weekly Price RRG: completed W-FRI bars; 52-week rolling baseline (minimum 26); 13-week relative-momentum comparison. Incomplete current week excluded.
- VSA: 20-period average volume and spread, volume/spread ratios, candle close location, candle direction and wick behaviour. Daily and weekly outputs are calculated independently.
- VSA classifications are descriptive context, not automatic entry signals. Stopping Volume requires subsequent confirmation.

## Updated backend files
- `scripts/rotation/build_rotation.py`
- `scripts/calculate_vsa.py` (new)
- `scripts/build_frontend_json.py`
- `scripts/validate_rotation_integration.py`
- `.github/workflows/marketpulse_update_west_others_publish.yml`

## Updated frontend files
- `index.html`
- `rotation.html`
- `data/technical_summary.json`

## Workflow
After normalized OHLCV and technical data are available:
1. Build Daily and Weekly Price RRG.
2. Calculate Daily and Weekly VSA for east, west_us, west_canada_global and west_others.
3. Build frontend JSON / Technical Summary.
4. Validate coverage.
5. Commit and sync JSON to the frontend repository.

## Validation snapshot (uploaded data as of 2026-11-25)
- Technical Summary instruments: 206
- Daily Price RRG: 180
- Weekly Price RRG: 178
- Daily VSA valid classifications: 192
- Weekly VSA valid classifications: 201
- Missing Daily/Weekly technical records: 0
- Missing Daily/Weekly VSA objects: 0
- Rotation integration validator: PASS

Some instruments have no explicit benchmark or insufficient history. Their RRG/VSA values remain unavailable rather than being inferred.
