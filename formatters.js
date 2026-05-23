*{box-sizing:border-box;margin:0;padding:0}
body{background:#f3f4f6;color:#111827;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:14px}
.topbar{background:#111827;color:#fff;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.logo{font-size:25px;font-weight:900;letter-spacing:-.7px}.logo span{color:#60a5fa}.subtitle{color:#cbd5e1;font-size:12px;margin-top:3px}
.status-bar{font-size:12px;color:#e5e7eb;text-align:right;line-height:1.5}
.summary-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;padding:14px 16px;background:#e5e7eb}
.summary-card{background:#fff;border-radius:12px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.summary-label{font-size:11px;color:#6b7280;text-transform:uppercase;font-weight:800;letter-spacing:.04em}.summary-value{font-size:20px;font-weight:900;margin-top:4px}
.controls{display:flex;gap:10px;padding:12px 16px;background:#fff;flex-wrap:wrap;border-bottom:1px solid #e5e7eb}
.controls input,.controls select{padding:9px 10px;border:1px solid #d1d5db;border-radius:8px;background:#fff;min-width:150px}.controls input{flex:1;min-width:220px}
.timeframe-toggle{display:flex;gap:6px;margin-left:auto}.timeframe-toggle button,.tabs button{padding:9px 13px;border:none;border-radius:8px;cursor:pointer;background:#e5e7eb;color:#111827;font-weight:700}
.timeframe-toggle button.active,.tabs button.active{background:#2563eb;color:#fff}
.tabs{display:flex;gap:8px;padding:12px 16px;background:#fff;flex-wrap:wrap;border-bottom:1px solid #e5e7eb;position:sticky;top:0;z-index:2}
.app{padding:16px}.group-card{background:#fff;margin-bottom:16px;padding:16px;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.09);overflow:hidden}
.group-header{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:12px;flex-wrap:wrap}.group-title{font-size:20px;font-weight:900}.group-meta{font-size:12px;color:#6b7280;margin-top:4px}
.group-signal{padding:6px 10px;border-radius:999px;background:#f3f4f6;font-weight:900}.table-wrap{overflow-x:auto}.instrument-table{width:100%;border-collapse:collapse;min-width:920px}
.instrument-table th,.instrument-table td{padding:10px;border-bottom:1px solid #e5e7eb;text-align:left;vertical-align:top}.instrument-table th{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.04em;background:#f9fafb}
.instrument-table tr:hover{background:#f9fafb}.benchmark-row{background:#dbeafe!important;font-weight:800}.role-pill{font-size:11px;border-radius:999px;padding:3px 7px;background:#eef2ff;color:#3730a3;font-weight:800}
.signal-pill{border-radius:999px;padding:4px 8px;font-weight:900;display:inline-block;font-size:12px}.signal-risk-on{background:#dcfce7;color:#166534}.signal-watch{background:#fef3c7;color:#92400e}.signal-good-buy{background:#e0f2fe;color:#075985}.signal-better-buy{background:#ede9fe;color:#5b21b6}.signal-best-buy{background:#dbeafe;color:#1d4ed8}.signal-risk-off{background:#fee2e2;color:#991b1b}
.positive{color:#15803d;font-weight:800}.negative{color:#b91c1c;font-weight:800}.neutral{color:#374151;font-weight:800}.small{font-size:12px;color:#6b7280}
.details-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}.metric{background:#f9fafb;border-radius:10px;padding:10px}.metric-label{font-size:11px;color:#6b7280;text-transform:uppercase;font-weight:800}.metric-value{font-size:16px;font-weight:900;margin-top:4px}
.empty{background:#fff;border-radius:14px;padding:30px;text-align:center;color:#6b7280}.health-box{background:#fff;border-radius:14px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}pre{white-space:pre-wrap;background:#111827;color:#e5e7eb;border-radius:12px;padding:14px;overflow:auto}
@media(max-width:768px){.topbar{text-align:left}.status-bar{text-align:left}.timeframe-toggle{margin-left:0;width:100%}.timeframe-toggle button{flex:1}.instrument-table{min-width:0}.instrument-table thead{display:none}.instrument-table,.instrument-table tbody,.instrument-table tr,.instrument-table td{display:block;width:100%}.instrument-table tr{border:1px solid #e5e7eb;border-radius:12px;margin-bottom:12px;padding:10px}.instrument-table td{border:none;padding:6px 4px}.instrument-table td::before{content:attr(data-label);display:block;font-size:11px;color:#6b7280;font-weight:900;text-transform:uppercase}}
