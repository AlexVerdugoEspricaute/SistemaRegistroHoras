document.addEventListener("DOMContentLoaded", function() {
    var passwordChangeLink = document.getElementById("password-change-link");
    var passwordChangeWarning = document.getElementById("password-change-warning");

    passwordChangeLink.addEventListener("click", function(event) {
        event.preventDefault();
        passwordChangeWarning.style.display = "block";
    });
});