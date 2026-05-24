function fmtPrice(v,currency){if(v===null||v===undefined||Number.isNaN(Number(v)))return "-";const n=Number(v);const prefix=currency==="CAD"?"C$":currency==="INR"?"₹":currency==="USD"?"$":"";return `${prefix}${n.toLocaleString(undefined,{maximumFractionDigits:2})}`;}
function fmtPct(v){if(v===null||v===undefined||Number.isNaN(Number(v)))return "-";return `${Number(v).toFixed(2)}%`;}
function fmtNum(v){if(v===null||v===undefined||Number.isNaN(Number(v)))return "-";return Number(v).toLocaleString(undefined,{maximumFractionDigits:4});}
function fmtDate(v){if(!v)return "-";return String(v).replace("T"," ").replace("+00:00"," UTC");}
function pctClass(v){if(v===null||v===undefined||Number.isNaN(Number(v)))return "neutral";return Number(v)>0?"positive":Number(v)<0?"negative":"neutral";}
