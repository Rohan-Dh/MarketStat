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


// Close with ESC key
document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    closeUpdateForm();
  }
});
// update collection ends


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
// pop up error message ends


// profile form starts
function openProfileForm() {
  const form = document.getElementById('profile-form');
  form.style.display = 'flex';
}

function cancelCodeForm() {
  const container = document.querySelector(".show-code-form");
  if (container) {
    container.style.display = "none";
  }
}
// profile form ends


// Close when clicking outside
window.addEventListener('click', function (event) {
  if (event.target === document.getElementById(`updateModel-${collectionId}`)) {
    closeUpdateForm();
  }
});


window.addEventListener('click', function (event) {
  const form = document.getElementById('profile-form');
  if (!form.contains(event.target)) {
    form.style.display = 'none';
  }
});



// review js starts
// Dark Mode Toggle
function toggleDarkMode() {
  document.documentElement.classList.toggle('dark-mode');
  localStorage.setItem('darkMode', document.documentElement.classList.contains('dark-mode'));
}

// Initialize dark mode
if (localStorage.getItem('darkMode') === 'true') {
  document.documentElement.classList.add('dark-mode');
}

// Filter Interactions
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    if (this.dataset.interval) {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('time_interval').value = this.dataset.interval;
    }
  });
});

// Date Input Handling
document.querySelectorAll('.date-input').forEach(input => {
  input.addEventListener('change', function () {
    document.getElementById('time_interval').value = 'custom';
  });
});
// review js ends



document.addEventListener('DOMContentLoaded', function () {

  // Time filtering code handling
  // Time Filter Buttons
  document.querySelectorAll('.time-filter').forEach(button => {
    button.addEventListener('click', function () {
      // Remove active class from all buttons
      document.querySelectorAll('.time-filter').forEach(btn => btn.classList.remove('active'));

      // Add active class to clicked button
      this.classList.add('active');

      // Set hidden input value
      document.getElementById('time_interval').value = this.dataset.interval;

      // Clear date inputs
      document.getElementById('start_date').value = '';
      document.getElementById('end_date').value = '';
    });
  });
  // Date Input Handling
  const dateInputs = document.querySelectorAll('input[type="date"]');
  dateInputs.forEach(input => {
    input.addEventListener('change', function () {
      // Clear time interval when dates are selected
      document.getElementById('time_interval').value = 'custom';
      document.querySelectorAll('.time-filter').forEach(btn => btn.classList.remove('active'));
    });
  });



  // chart handling code
  let salesChart = null;
  // Graph display handler
  document.querySelectorAll('.show-graph-link').forEach(link => {
    link.addEventListener('click', async function (e) {
      e.preventDefault();

      const form = this.closest('form');
      const collectionId = this.dataset.collectionId;
      const userCollectionId = this.dataset.userCollectionId;

      try {
        const response = await fetch(`${form.action}?collectionId=${collectionId}&userCollectionId=${userCollectionId}`, {
          headers: {
            'X-Requested-With': 'XMLHttpRequest', // This is crucial
            'Accept': 'application/json'
          }
        });
        console.log(response);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        console.log(data.quantities);

        if (salesChart) salesChart.destroy();

        const ctx = document.getElementById('salesChart').getContext('2d');

        salesChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              label: 'Quantity Sold',
              data: data.quantities,
              backgroundColor: '#02aab0',
              borderColor: '#00ffff',
              borderWidth: 1,
              borderRadius: 4,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              datalabels: {
                anchor: 'end',
                align: 'top',
                color: '#fff',
                formatter: (value, context) => {
                  return data.prices[context.dataIndex];
                }
              },
              legend: {
                labels: { color: '#fff' }
              }
            },
            scales: {
              x: {
                title: {
                  text: 'Time Period',
                  display: true,
                  color: '#fff'
                },
                grid: { color: '#004756' },
                ticks: { color: '#fff' }
              },
              y: {
                title: {
                  text: 'Quantity Sold',
                  display: true,
                  color: '#fff',
                },
                grid: { color: '#004756' },
                ticks: { color: '#fff' }
              }
            }
          },
          plugins: [ChartDataLabels]
        });

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('graphModal'));
        modal.show();
      } catch (error) {
        console.error('Error loading graph data:', error);
      }
    });
  });
});