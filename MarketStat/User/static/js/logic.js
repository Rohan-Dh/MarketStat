function toggleForm() {
  var form = document.getElementById("popupForm");
  form.style.display = (form.style.display === "block") ? "none" : "block";
}

function toggleSellForm(id) {
  const form = document.getElementById(`sellForm-${id}`);
  form.style.display = (form.style.display === "block") ? "none" : "block";
}