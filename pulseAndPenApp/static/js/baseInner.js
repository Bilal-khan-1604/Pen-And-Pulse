function logoutAndRedirectHome() {
    document.cookie.split(";").forEach(cookie => {
        const cookieName = cookie.split("=")[0].trim();
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    });

    const homeUrl = window.location.origin + '/';
    if (window.location.href === homeUrl) {
        window.location.reload();
    } else {
        window.location.href = homeUrl;
    }
}

document.getElementById("logoutButton").addEventListener("click", logoutAndRedirectHome);