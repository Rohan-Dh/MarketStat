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


// pop up error message starts
function showNotification(message, type = 'error', duration = 5000) {
  const container = document.getElementById('notificationContainer');
  
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  
  const progress = document.createElement('div');
  progress.className = 'notification-progress';
  
  const content = `
      <button class="notification-close"></button>
      <div class="notification-content">
          <div class="notification-icon">
              ${type === 'error' ? '⚠️' : 
               type === 'success' ? '✓' :
               type === 'warning' ? '⚠️' : 'i'}
          </div>
          <div class="notification-text">
              <div class="notification-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
              <div class="notification-message">${message}</div>
          </div>
      </div>
  `;
  
  notification.innerHTML = content;
  notification.appendChild(progress);
  container.appendChild(notification);
  
  // Trigger animation
  setTimeout(() => notification.classList.add('active'), 10);
  
  // Progress bar animation
  progress.style.width = '100%';
  progress.style.transitionDuration = `${duration}ms`;
  setTimeout(() => progress.style.width = '0%', 10);
  
  // Auto-remove after duration
  setTimeout(() => {
      notification.classList.remove('active');
      setTimeout(() => notification.remove(), 300);
  }, duration);
  
  // Close button handler
  notification.querySelector('.notification-close').addEventListener('click', () => {
      notification.classList.remove('active');
      setTimeout(() => notification.remove(), 300);
  });
}

// Example usage:
// showNotification('Invalid email address', 'error', 5000);
// showNotification('Payment successful!', 'success', 3000);
// showNotification('System update available', 'info', 4000);
// showNotification('Low disk space', 'warning', 5000);
// pop up error message ends