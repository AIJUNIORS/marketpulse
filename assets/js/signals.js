
function signalClass(signal){
  if(!signal) return "";
  return `signal-${signal.toLowerCase().replace(/\s+/g,'-')}`;
}
