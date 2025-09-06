// Backend base URL
const API_BASE = "https://marine-minds-backend-t6yh.onrender.com";

// ----------------------
// Submit Report (Form)
// ----------------------
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("hazardForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(form);

      try {
        const res = await fetch(`${API_BASE}/submit_report/`, {
          method: "POST",
          body: formData
        });

        if (res.ok) {
          alert("Report submitted successfully ✅");
          form.reset();
        } else {
          alert("Failed to submit ❌");
        }
      } catch (err) {
        console.error("Error while submitting", err);
        alert("Error while submitting ❌");
      }
    });
  }
});

// ----------------------
// Fetch + Render Reports (Dashboard)
// ----------------------
async function getReports() {
  try {
    const res = await fetch(`${API_BASE}/reports/`);
    return await res.json();
  } catch (err) {
    console.error("Error fetching reports", err);
    return [];
  }
}

async function renderReports() {
  let reports = await getReports();

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

  // Update map pins
  updateMap(reports);
}

// Run filters + sorting
document.addEventListener("DOMContentLoaded", () => {
  const filterType = document.getElementById("filterType");
  const sortOrder = document.getElementById("sortOrder");

  if (filterType && sortOrder) {
    filterType.addEventListener("change", renderReports);
    sortOrder.addEventListener("change", renderReports);
    renderReports();
  }
});
