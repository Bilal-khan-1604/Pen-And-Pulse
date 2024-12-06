document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".form-box");
    const loadingOverlay = document.querySelector(".loading-overlay");
    
    clearFields();
    hideLoadingOverlay(loadingOverlay);

    enableEnterKeyNavigation(form, loadingOverlay)
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        submitForm(form, loadingOverlay);
    });
});

function hideLoadingOverlay() {
    const loadingOverlay = document.querySelector(".loading-overlay");
    if (loadingOverlay) loadingOverlay.style.display = "none";
}

function clearFields() {
    const inputFields = document.querySelectorAll("input");
    const textAreas = document.querySelectorAll("textarea");
    const focusableElements = [...inputFields, ...textAreas]; 
    focusableElements.forEach((field) => {
        field.value = "";
    });
}

function enableEnterKeyNavigation(form, loadingOverlay) {
    const inputFields = document.querySelectorAll("input");
    const textAreas = document.querySelectorAll("textarea");
    const focusableElements = [...inputFields, ...textAreas];

    focusableElements.forEach((element, index) => {
        element.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();

                if (index < focusableElements.length - 1) {
                    focusableElements[index + 1].focus();
                } else {
                    submitForm(form, loadingOverlay);
                }
            }
        });
    });
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

async function submitForm(form, overlay) {
    overlay.style.display = 'flex';
    const formData = new FormData(form);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    try {
        const response = await fetch(form.action, {
            method: form.method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(jsonData),
        });

        const result = await response.json();

        hideLoadingOverlay();

        if (response.ok) {
            clearFields();
            displayModal("Success", result.message || "Your form was submitted successfully.")
        } else {
            displayModal("Error", result[Object.keys(result)[0]][0] || "An error occurred while submitting the form.")
        }

    } catch (error) {
        console.error("Error:", error);
        displayModal("Error", "An unexpected error occurred. Please try again later.");
    }
}

function displayModal(title, body) {
    const modalTitle = document.querySelector('#responseModal .modal-title');
    const modalBody = document.querySelector('#responseModal .modal-body');
    modalTitle.innerHTML = title;
    modalBody.innerHTML = body;
    const modal = new bootstrap.Modal(document.getElementById('responseModal'));
    modal.show();
}