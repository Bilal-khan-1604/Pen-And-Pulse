function toggleContainer(targetClass) {
    const container = document.querySelector(`.${targetClass}`);
    const autoHideDuration = 3000;
  
    if (!container) {
      console.error(`No element found with class: ${targetClass}`);
      return;
    }
  
    if (container.classList.contains('active')) {
      container.classList.remove('active');
      setTimeout(() => (container.style.display = 'none'), 500);
    } else {
      container.style.display = 'flex';
      setTimeout(() => container.classList.add('active'), 10);
  
      setTimeout(() => {
        container.classList.remove('active');
        setTimeout(() => (container.style.display = 'none'), 500);
      }, autoHideDuration);
    }
  }
  
//   document.getElementById('registrationForm').addEventListener('input', function () {
//     const password = document.querySelector('password-input').value;
//     const confirmPassword = document.querySelector('confirm-password-input').value;
//     const message = document.querySelector('incorrect-confirm-password-format');
//     const submitButton = document.getElementById('submitButton');
    
//     if (password !== confirmPassword) {
//         message.style.display = 'flex';
//         submitButton.disabled = true;
//     } else {
//       message.style.display = 'none';
//         submitButton.disabled = false;
//     }
// });
