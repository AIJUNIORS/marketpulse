
async function loadMarketPulseData() {
  const response = await fetch("data/market_pulse_combined.json");
  const data = await response.json();
  state.data = data;

  const select = document.getElementById("groupSelect");
  data.groups.forEach(group => {
    const option = document.createElement("option");
    option.value = group.group_name;
    option.textContent = group.group_name;
    select.appendChild(option);
  });

  document.getElementById("statusBar").textContent =
    `Updated: ${data.generated_at} | Universe: ${data.universe_count}`;
}
