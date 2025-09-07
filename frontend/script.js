document.getElementById("hazardForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("name", document.getElementById("name").value);
  formData.append("location", document.getElementById("location").value);
  formData.append("disaster", document.getElementById("hazard").value);
  formData.append("description", document.getElementById("description").value);
  
  const fileInput = document.querySelector("input[type='file']");
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }

  try {
    const response = await fetch("https://marine-minds-backend-t6yh.onrender.com/submit_report/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Server error");
    const data = await response.json();

    alert("✅ Report submitted: " + JSON.stringify(data));
  } catch (error) {
    alert("❌ Request failed: " + error.message);
  }
});
