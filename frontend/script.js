document.getElementById("hazardForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("name", document.getElementById("name").value);
  formData.append("location", document.getElementById("location").value);
  formData.append("disaster", document.getElementById("disaster").value); // 👈 backend ke field ke sath match
  formData.append("description", document.getElementById("description").value);

  const fileInput = document.getElementById("file");
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }

  try {
    const response = await fetch("https://marine-minds-backend-t6yh.onrender.com/submit_report/", {
      method: "POST",
      body: formData
    });

    if (response.ok) {
      alert("✅ Report submitted successfully!");
      document.getElementById("hazardForm").reset();
    } else {
      const errorData = await response.json();
      alert("❌ Error while submitting: " + JSON.stringify(errorData));
    }
  } catch (error) {
    alert("⚠️ Request failed: " + error);
  }
});
