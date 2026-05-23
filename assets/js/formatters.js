
function fmtPrice(v){
  return v?.toFixed ? `$${v.toFixed(2)}` : "-";
}
function fmtPct(v){
  if(v === null || v === undefined) return "-";
  return `${v.toFixed(2)}%`;
}
