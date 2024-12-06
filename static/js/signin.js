document.addEventListener("DOMContentLoaded", function () {
    const loadingOverlay = document.querySelector(".loading-overlay");
    const inputFields = document.querySelectorAll("input");
    const form = document.querySelector(".sign-in-info");
    const emailField = document.querySelector(".email-input");
    const emailPasswordError = document.querySelector(".incorrect-email-password");

    hideLoadingOverlay();

    clearFields(inputFields);

    enableEnterKeyNavigation(inputFields, form, loadingOverlay, emailField, emailPasswordError);

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        submitForm(form, inputFields, loadingOverlay, emailField, emailPasswordError);
    });

    emailField.addEventListener("input", function () {
        const email = emailField.value.trim();
        emailPasswordError.querySelector('p').textContent = "Email is incorrect."
        toggleContainer(emailPasswordError, email && !isValidEmail(email));
    });
});

function hideLoadingOverlay() {
    const loadingOverlay = document.querySelector(".loading-overlay");
    if (loadingOverlay) loadingOverlay.style.display = "none";
}

function clearFields(fields) {
    fields.forEach((field) => {
        field.value = "";
    });
}

function enableEnterKeyNavigation(fields, form, loadingOverlay, emailField, emailPasswordError) {
    fields.forEach((input, index) => {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                if (index < fields.length - 1) {
                    fields[index + 1].focus();
                } else {
                    submitForm(form, fields, loadingOverlay, emailField, emailPasswordError);
                }
            }
        });
    });
}

function toggleContainer(targetElement, show) {
    if (!targetElement) {
        return;
    }
    targetElement.classList.toggle("active", show);
}

function isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return emailRegex.test(email);
}

function getCookie(name) {
    const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}

function submitForm(form, inputFields, loadingOverlay, emailField, emailPasswordError) {
    const email = emailField.value.trim();
    const csrfToken = getCookie("csrftoken");

    loadingOverlay.style.display = "flex";

    if (!email || !isValidEmail(email)) {
        toggleContainer(emailPasswordError, true);
        hideLoadingOverlay();
        return;
    }

    const formData = {
        email,
        password: document.querySelector(".password-input").value,
    };

    fetch(form.action, {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
    })
        .then((response) => response.json())
        .then((responseData) => {
            if (responseData.submitted === "true") {
                clearFields(inputFields);
                hideLoadingOverlay();
                window.location.href = "/user-home";
            } else {
                hideLoadingOverlay();
                toggleContainer(emailPasswordError, true);

                if (responseData.errors) {
                    const errorContainer = emailPasswordError.querySelector("p");
                    const errorMessages = Object.entries(responseData.errors)
                    .map(([_, message]) => message)
                    .join("");
                    errorContainer.textContent = errorMessages;
                }
            }
        })
        .catch((error) => {
            hideLoadingOverlay();
            console.error("Error:", error);
            hideLoadingOverlay();
        });
}
