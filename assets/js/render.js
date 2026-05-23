
function initializeControls() {
  document.querySelectorAll("[data-tf]").forEach(btn => {
    btn.addEventListener("click", () => {
      state.selectedTimeframe = btn.dataset.tf;
      document.querySelectorAll("[data-tf]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderApp();
    });
  });

  document.getElementById("groupSelect").addEventListener("change", e => {
    state.selectedGroup = e.target.value;
    renderApp();
  });

  document.getElementById("searchBox").addEventListener("input", e => {
    state.searchText = e.target.value;
    renderApp();
  });

  document.querySelectorAll("[data-tab]").forEach(btn => {
    btn.addEventListener("click", () => {
      state.activeTab = btn.dataset.tab;
      document.querySelectorAll("[data-tab]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderApp();
    });
  });
}

function renderApp() {
  const app = document.getElementById("app");
  app.innerHTML = "";

  if(!state.data) return;

  state.data.groups.forEach(group => {
    if(state.selectedGroup !== "all" && group.group_name !== state.selectedGroup) return;

    const card = document.createElement("section");
    card.className = "group-card";

    card.innerHTML = `
      <div class="group-title">
        ${group.group_name} | Benchmark: ${group.benchmark_symbol}
      </div>
      <table class="instrument-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Close</th>
            <th>Return</th>
            <th>Signal</th>
          </tr>
        </thead>
        <tbody>
          ${renderRows(group.items)}
        </tbody>
      </table>
    `;

    app.appendChild(card);
  });
}

function renderRows(items) {
  return filterItems(items).map(item => {
    const tf = state.selectedTimeframe;
    const ret = item.returns?.[tf]?.return_pct || 0;
    const signal = item.signals?.[tf]?.signal || "Watch";

    return `
      <tr class="${item.role === 'benchmark' ? 'benchmark-row' : ''}">
        <td>${item.symbol}</td>
        <td>${item.name || '-'}</td>
        <td>${fmtPrice(item.last_close)}</td>
        <td class="${ret >= 0 ? 'positive' : 'negative'}">${fmtPct(ret)}</td>
        <td class="${signalClass(signal)}">${signal}</td>
      </tr>
    `;
  }).join("");
}
