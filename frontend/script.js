// Fetch reports from localStorage
function getReports() {
  return JSON.parse(localStorage.getItem("reports")) || [];
}

// Render reports with filter + sort
function renderReports() {
  let reports = getReports();

  // Filtering
  const filterType = document.getElementById("filterType").value;
  if (filterType !== "all") {
    reports = reports.filter(r => r.type === filterType);
  }

  // Sorting
  const sortOrder = document.getElementById("sortOrder").value;
  reports.sort((a, b) => {
    return sortOrder === "latest"
      ? new Date(b.time) - new Date(a.time)
      : new Date(a.time) - new Date(b.time);
  });

  // Display list
  const list = document.getElementById("reportItems");
  list.innerHTML = "";
  reports.forEach(r => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${r.type}</strong> - ${r.location} <br><small>${r.time}</small>`;
    list.appendChild(li);
  });

  // Update map pins (from your Day 2 code)
  updateMap(reports);
}

// Run filters + sorting
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("filterType").addEventListener("change", renderReports);
  document.getElementById("sortOrder").addEventListener("change", renderReports);
  renderReports();
});
