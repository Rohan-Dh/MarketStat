function toggleForm() {
  const popup = document.getElementById('popupForm');
  popup.style.display = popup.style.display === 'none' ? 'flex' : 'none';
}


function openSellForm(formId) {
  const form = document.getElementById(`sellForm-${formId}`);
  form.parentElement.style.display = 'flex';
}

function closeSellForm(formId) {
  const form = document.getElementById(`sellForm-${formId}`);
  form.parentElement.style.display = 'none';
}

window.addEventListener('click', function (event) {
  if (event.target.classList.contains('modal-overlay')) {
    event.target.style.display = 'none';
  }
});

document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    const modals = document.querySelectorAll('.modal-overlay');
    modals.forEach(modal => modal.style.display = 'none');
  }
});

window.addEventListener('click', function (event) {
  const popup = document.getElementById('popupForm');
  if (event.target === popup) {
    popup.style.display = 'none';
  }
});

document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    document.getElementById('popupForm').style.display = 'none';
  }
});

// delete are you sure form starts
function showDeleteModal(collectionId, collectionName) {
  const modal = document.getElementById(`deleteModal-${collectionId}`);
  modal.style.display = 'flex';
  modal.querySelector('#collectionNameSpan').textContent = collectionName;
}

function closeDeleteModal(collectionId) {
  document.getElementById(`deleteModal-${collectionId}`).style.display = 'none';
}

window.addEventListener('click', function (event) {
  if (event.target === document.getElementById('deleteModal')) {
    closeDeleteModal();
  }
});

document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    closeDeleteModal();
  }
});
// delete are you sure form ends


// update collection starts
function openUpdateForm(formId) {
  const form = document.getElementById(`updateForm-${formId}`);
  form.parentElement.style.display = 'flex';
}

function closeUpdateForm(formId) {
  const form = document.getElementById(`updateForm-${formId}`);
  form.parentElement.style.display = 'none';
}

// Close when clicking outside
window.addEventListener('click', function (event) {
  if (event.target === document.getElementById(`updateModel-${collectionId}`)) {
    closeUpdateForm();
  }
});

// Close with ESC key
document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    closeUpdateForm();
  }
});
// update collection starts