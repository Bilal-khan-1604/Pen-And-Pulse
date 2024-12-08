document.addEventListener('DOMContentLoaded', function () {
    const pageTitle = document.title;
    const button = document.querySelector('.cover-sign-in-btn');

    if (pageTitle === 'Pulse & Pen') {
        button.onclick = function () {
            return false;
        };
    } else {
        button.onclick = function () {
            window.location.href = '/login/';
        };
    }
});
