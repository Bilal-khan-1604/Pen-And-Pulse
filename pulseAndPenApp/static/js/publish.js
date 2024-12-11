document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('post-blog').reset()
    const allowedTypes = ['.jpg', '.jpeg'];
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
        const formData = new FormData(blogForm);
        const authToken = getCookie("authtoken");

        fetch(blogForm.action, {
            method: blogForm.method,
            body: formData,
            headers: {
                'Authorization': `Bearer ${authToken}` // Include JWT token
            }
        })
            .then(response => response.json())
            .then(data => {
                // Handle success
                console.log("Form submitted successfully:", data);
                alert("Blog posted successfully!");
            })
            .catch(error => {
                // Handle errors
                console.error("Error submitting the form:", error);
                alert("Failed to post the blog. Please try again.");
            });
    });
});

function getCookie(name) {
    const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}
