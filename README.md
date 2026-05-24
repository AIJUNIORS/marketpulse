# MarketPulse Frontend v3 — Old UI JSON Connected

This restores the old compact MarketPulse visual foundation while removing hardcoded MKTS/SECTS data.

Data source expected:

    data/market_pulse_combined.json

Included:
- Top market strip
- Pulse tab
- Combined return heatmap
- Drawdown analysis tab
- Support Zones / CPR / Pivot tab
- Group comparison tab
- Technical Analysis tab at the end
- Sortable table headers
- Search, sector filter, group tabs, timeframe toggle
- Mobile-friendly technical cards
- Calendar monthly fallback message

Current backend supports Annual, YTD, 6M, 3M, 1M, MTD, Weekly, Daily returns. True Jan-Dec calendar monthly history needs backend calendar_returns later.
