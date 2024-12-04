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
  