function signalClass(signal){if(!signal)return "signal-watch";return `signal-${String(signal).toLowerCase().replace(/\s+/g,"-")}`;}
function signalPill(signal){const s=signal||"Watch";return `<span class="signal-pill ${signalClass(s)}">${s}</span>`;}
