document.addEventListener("DOMContentLoaded", function() {
    var navbarTogglerBtn = document.getElementById("navbar-toggler-btn");
    navbarTogglerBtn.addEventListener("click", function() {
        var navbarNavAltMarkup = document.getElementById("navbarNavAltMarkup");
        var navbarSupportedContent = document.getElementById("navbarSupportedContent");
        if (navbarNavAltMarkup.classList.contains("show")) {
            navbarNavAltMarkup.classList.remove("show");
            navbarSupportedContent.classList.remove("show");
        } else {
            navbarNavAltMarkup.classList.add("show");
            navbarSupportedContent.classList.add("show");
        }
    });
});
