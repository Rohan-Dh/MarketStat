function toggleForm() {
  var form = document.getElementById("popupForm");
  form.style.display = (form.style.display === "block") ? "none" : "block";
}

function openSellForm(formId) {
  const form = document.getElementById(`sellForm-${formId}`);
  form.parentElement.style.display = 'flex';
}

function closeSellForm(formId) {
  const form = document.getElementById(`sellForm-${formId}`);
  form.parentElement.style.display = 'none';
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
  if (event.target.classList.contains('modal-overlay')) {
      event.target.style.display = 'none';
  }
});

// Close modal with ESC key
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
      const modals = document.querySelectorAll('.modal-overlay');
      modals.forEach(modal => modal.style.display = 'none');
  }
});