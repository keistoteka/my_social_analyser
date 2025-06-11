function openModal(platform) {
  document.getElementById('connectModal').classList.remove('hidden');
  document.getElementById('modalPlatformTitle').textContent = 'Connect to ' + platform.charAt(0).toUpperCase() + platform.slice(1);
  document.getElementById('modalPlatformInput').value = platform.toLowerCase();
}

function closeModal() {
  document.getElementById('connectModal').classList.add('hidden');
}

document.querySelectorAll('.connect-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    openModal(this.dataset.platform);
  });
});

document.getElementById('connectForm').addEventListener('submit', function(e) {
  if (document.getElementById('modalPlatformInput').value === 'facebook') {
    const rememberCheckbox = document.querySelector('input[name="remember_facebook_creds"]');
    if (rememberCheckbox && rememberCheckbox.checked) {
      sessionStorage.setItem('remember_facebook_creds', 'true');
    }
  }
}); 