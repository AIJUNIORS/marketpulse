
document.addEventListener("DOMContentLoaded", async () => {
  await loadMarketPulseData();
  initializeControls();
  renderApp();
});
