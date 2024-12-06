document.querySelectorAll('.cover-sign-in-btn, .join-btn').forEach(button => {
  button.addEventListener('click', function () {
    const coverElement = document.querySelector('.cover');

    coverElement.classList.add('animate-move-up-fade');

    coverElement.addEventListener('animationend', function () {
      coverElement.style.visibility = 'hidden';
      coverElement.style.pointerEvents = 'none';
      
      if (button.classList.contains('cover-sign-in-btn')) {
        window.location.href = "/sign-in";
      } else if (button.classList.contains('join-btn')) {
        window.location.href = "/sign-up";
      }
    }, { once: true });
  });
});

window.addEventListener('pageshow', (event) => {
  const coverElement = document.querySelector('.cover');
  if (event.persisted && coverElement) {
    coverElement.style.visibility = 'visible';
    coverElement.style.pointerEvents = 'auto';
    coverElement.style.display = 'grid';
    coverElement.classList.remove('animate-move-up-fade');
  }
});
