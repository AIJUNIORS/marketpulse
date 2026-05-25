# MarketPulse Frontend Index Update

Replace your frontend `index.html` with this file.

Expected data files in the frontend repo:
- `data/market_pulse_combined.json`
- `data/market_pulse_flat.json`
- `data/return_summary.json`
- `data/technical_summary.json`
- `data/last_updated.json`

The dashboard primarily reads `market_pulse_combined.json` and `last_updated.json`.

Included UI:
- Pulse summary page with six blocks
- Broad Markets page with benchmark table, combined heatmap, drawdown, support zones
- Detailed Group Analysis page with group selector, relative strength, heatmap, drawdown, support zones
- Technical Analysis tab at the end
- Sortable table headers
- Close price shown throughout
- Fallback display for missing backend fields
