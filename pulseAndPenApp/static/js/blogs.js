document.querySelectorAll('.blog-nav-item a').forEach(link => {
    link.addEventListener('mouseover', function () {
        if (this.parentElement != document.querySelector('.blog-active')) {
            this.parentElement.style.backgroundColor = '#2c474d';
            this.parentElement.style.border = '1px solid white';
            this.style.color = '#FFA500'
        }

    });
    link.addEventListener('mouseout', function () {
        this.parentElement.style.backgroundColor = 'transparent';
        this.parentElement.style.border = 'none';
        this.style.color = 'white';
    });
});
