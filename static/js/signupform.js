document.addEventListener("DOMContentLoaded", function () {
    const loadingOverlay = document.querySelector('.loading-overlay')
    const inputFields = document.querySelectorAll("input");
    const form = document.querySelector(".sign-up-info");
    const firstNameField = document.querySelector(".first-name-input");
    const lastNameField = document.querySelector(".last-name-input");
    const emailField = document.querySelector(".email-input");
    const passwordField = document.querySelector(".password-input");
    const confirmPasswordField = document.querySelector(".confirm-password-input");

    const passwordError = document.querySelector(".incorrect-password-format");
    const confirmPasswordError = document.querySelector(".incorrect-confirm-password-format");
    const emailError = document.querySelector(".incorrect-email-format");
    const nameError = document.querySelector(".incorrect-name-format");

    const passwordPara = passwordError.querySelector("p");
    const confirmPasswordPara = confirmPasswordError.querySelector("p");
    const emailPara = emailError.querySelector("p");
    const namePara = nameError.querySelector("p");

    const passwordCriteriaRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?#^&])[A-Za-z\d@$!%*?&]{8,}$/;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    loadingOverlay.style.display = 'none';

    inputFields.forEach(function (field) {
        field.value = "";
    });

    inputFields.forEach((input, index) => {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();

                if (index < inputFields.length - 1) {
                    inputFields[index + 1].focus();
                } else {
                    event.preventDefault();
                    validateAndSubmitForm(form, finalValidate);
                }
            }
        });
    });

    [firstNameField, lastNameField, emailField, passwordField, confirmPasswordField].forEach((field) =>
        field.addEventListener("input", inlineValidate)
    );

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        validateAndSubmitForm(form, finalValidate);
    });

    function validateAndSubmitForm(form, finalValidate) {
        const allValid = finalValidate();
        if (allValid) {
            loadingOverlay.style.display = 'flex';
            submitForm(form, inputFields, loadingOverlay);
        } else {
            return;
        }
    }

    function inlineValidate() {
        validateField("password", false);
        validateField("confirmPassword", false);
        validateField("email", false);
        validateField("name", false);
    }

    function finalValidate() {
        let isValid = true;

        isValid = validateField("name", true) && isValid;
        isValid = validateField("email", true) && isValid;
        isValid = validateField("password", true) && isValid;
        isValid = validateField("confirmPassword", true) && isValid;

        return isValid;
    }

    function validateField(type, finalValidation) {
        let isValid = true;

        if (type === "name") {
            const firstName = firstNameField.value.trim();
            const lastName = lastNameField.value.trim();

            if ((firstName === "" || lastName === "") && finalValidation) {
                toggleContainer(nameError, true);
                namePara.textContent = "First name and last name cannot be empty.";
                namePara.style.color = "red";
                isValid = false;
            } else {
                toggleContainer(nameError, false);
            }
        }

        if (type === "email") {
            const email = emailField.value.trim();

            if (email === "") {
                if (!finalValidation) {
                    toggleContainer(emailError, false);
                }
                if (finalValidation) {
                    toggleContainer(emailError, true);
                    emailPara.textContent = "Please enter a valid email address.";
                    emailPara.style.color = "red";
                    isValid = false;
                }
            }
            else if (!emailRegex.test(email)) {
                toggleContainer(emailError, true);
                emailPara.textContent = "Please enter a valid email address.";
                emailPara.style.color = "red";
                isValid = false;
            } else {
                toggleContainer(emailError, false);
            }
        }

        if (type === "password") {
            const password = passwordField.value.trim();

            if (password === "") {
                if (!finalValidation) {
                    toggleContainer(passwordError, false);
                }
                if (finalValidation) {
                    toggleContainer(passwordError, true);
                    passwordPara.textContent =
                        "Password must be at least 8 characters long and include at least one letter, one number, and one symbol.";
                    passwordPara.style.color = "red";
                    isValid = false;
                }
            } else if (!passwordCriteriaRegex.test(password)) {
                toggleContainer(passwordError, true);
                passwordPara.textContent =
                    "Password must be at least 8 characters long and include at least one letter, one number, and one symbol.";
                passwordPara.style.color = "red";
                isValid = false;
            } else {
                toggleContainer(passwordError, true);
                passwordPara.textContent = "Password meets the criteria.";
                passwordPara.style.color = "green";
            }
        }

        if (type === "confirmPassword") {
            const confirmPassword = confirmPasswordField.value.trim();
            const password = passwordField.value.trim();

            if (confirmPassword === "") {
                if (!finalValidation) {
                    toggleContainer(confirmPasswordError, false);
                }
                if (finalValidation) {
                    toggleContainer(confirmPasswordError, true);
                    confirmPasswordPara.textContent = "Please enter a password.";
                    confirmPasswordPara.style.color = "red";
                    isValid = false;
                }
            } else if (confirmPassword !== password) {
                toggleContainer(confirmPasswordError, true);
                confirmPasswordPara.textContent = "Passwords do not match.";
                confirmPasswordPara.style.color = "red";
                isValid = false;
            } else {
                toggleContainer(confirmPasswordError, true);
                confirmPasswordPara.textContent = "Passwords match.";
                confirmPasswordPara.style.color = "green";
            }
        }

        return isValid;
    }

    function toggleContainer(targetElement, show) {
        if (!targetElement) {
            return;
        }

        if (show) {
            targetElement.classList.add("active");
        } else {
            targetElement.classList.remove("active");
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitForm(form, inputFields, loadingOverlay) {
    const csrfToken = getCookie('csrftoken');

    const formData = {};
    inputFields.forEach(function (field) {
        formData[field.name] = field.value;
    });

    fetch(form.action, {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => {
            if (response.ok) {
                inputFields.forEach(function (field) {
                    field.value = "";
                });
                window.location.href = '/sign-in'; 
            } else {
                loadingOverlay.style.display = 'none';
            }
        })
        .catch((error) => console.error("Error:", error));
}
