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

function attachButtonAlerts(buttonIds) {
    buttonIds.forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener("click", () => {
                alert(`We are working on OAuth Verification. For now, please continue with email.`);
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const buttonIds = ["googleSignUp", "linkedinSignUp", "googleSignIn", "linkedinSignIn"];
    attachButtonAlerts(buttonIds);

    const newsletterForm = document.querySelector(".newsletter");
    newsletterForm.reset();
    newsletterForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const emailInput = document.querySelector('input[name="newsletter-email"]').value;

        fetch(newsletterForm.action || window.location.href, {
            method: "POST",
            body: JSON.stringify({
                email: emailInput
            }),
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie("csrftoken"),
            }
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Failed to submit the form");
                }
            })
            .then(data => {
                newsletterForm.reset();
                alert("Thank you for subscribing!");
            })
            .catch(error => {
                alert("Failed to subscribe. Please try again.");
            });
    });



});

