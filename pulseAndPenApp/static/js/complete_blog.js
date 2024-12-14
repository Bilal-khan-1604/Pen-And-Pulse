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

const loadingOverlay = document.querySelector(".loading-overlay");

function hideLoadingOverlay() {
    if (loadingOverlay) loadingOverlay.style.display = "none";
}

const commentForm = document.getElementById("commentForm");
commentForm.addEventListener("submit", function (event) {
    event.preventDefault();
    loadingOverlay.style.display = "flex"
    const authToken = getCookie("authToken");
    const commentText = document.querySelector('#comment-text').value;
    const blogId = document.querySelector('.blog-id').value;

    fetch(commentForm.action, {
        method: commentForm.method,
        body: JSON.stringify({
            text: commentText,
            blog_id: blogId
        }),
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie("csrftoken"),
            'Authorization': `Bearer ${authToken}`
        }
    })
        .then((response) => {
            hideLoadingOverlay()
            if (response.ok) {
                commentForm.reset();
            } else {
                return response.json();
            }
        })
        .catch(error => {
            hideLoadingOverlay()
            // Handle errors
            console.error("Error submitting the form:", error);
            alert("Failed to post. Please try again.");
        });
});

document.addEventListener('DOMContentLoaded', function (){
    commentForm.reset();
})