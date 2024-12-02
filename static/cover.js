document.querySelectorAll('.cover-sign-in-btn, .join-btn').forEach(button => {
  button.addEventListener('click', function () {
    const coverElement = document.querySelector('.cover');

    coverElement.classList.add('animate-move-up-fade');

    coverElement.addEventListener('animationend', function () {
      coverElement.style.display = 'none';
    }, { once: true });
  });
});
