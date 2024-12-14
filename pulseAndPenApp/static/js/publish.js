function getCookie(name) {
    const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
    for (const cookie of cookies) {
        console.log(cookie);
        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}

// const loadingOverlay = document.querySelector(".loading-overlay");

// function hideLoadingOverlay() {
//     if (loadingOverlay) loadingOverlay.style.display = "none";
// }

const authToken = getCookie("authToken");
console.log(authToken);

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('post-blog').reset()
    const allowedTypes = ['.jpg', '.jpeg', '.avif'];
    const thumbnailInput = document.getElementById('blog-thumbnail');

    thumbnailInput.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
            if (!allowedTypes.includes(fileExtension)) {
                this.value = '';

                const popover = new bootstrap.Popover(this, {
                    trigger: 'focus',
                    placement: 'top',
                    content: 'Only .jpg and .jpeg files are allowed.',
                    title: 'Invalid File',
                    customClass: 'custom-popover'
                });

                this.setAttribute('data-bs-toggle', 'popover');
                this.focus();
            }
        }
    });
    const blogForm = document.getElementById("post-blog");

    blogForm.addEventListener("submit", function (event) {
        event.preventDefault();
        // loadingOverlay.style.display = "flex"
        const formData = new FormData(blogForm);
        const authToken = getCookie("authToken");
        console.log(authToken);

        fetch(blogForm.action, {
            method: blogForm.method,
            body: formData,
            headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Authorization': `Bearer ${authToken}` // Include JWT token
            }
        })
            .then(response => response.json())
            .then(data => {
                // hideLoadingOverlay()
                alert("Blog posted successfully!");

            })
            .catch(error => {
                alert("Failed to post the blog.\n" + error + "\nPlease try again.");
            });
    });
});

