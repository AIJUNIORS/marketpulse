
function filterItems(items) {
  return items.filter(item => {
    const groupMatch = state.selectedGroup === "all" || item.market_group === state.selectedGroup;
    const searchMatch =
      item.symbol.toLowerCase().includes(state.searchText.toLowerCase()) ||
      (item.sector || "").toLowerCase().includes(state.searchText.toLowerCase());

    return groupMatch && searchMatch;
  });
}
