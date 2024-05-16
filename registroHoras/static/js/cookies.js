document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("modal");
    const acceptCookiesBtn = document.getElementById("accept-cookies");
    const rejectCookiesBtn = document.getElementById("reject-cookies");

    // Verificar si el usuario ya ha aceptado las cookies previamente
    if (!getCookie("cookiesAccepted")) {
        // Mostrar el modal solo si no ha aceptado las cookies previamente
        modal.style.display = "block";
    }

    // Manejar el clic en el botón "Aceptar cookies"
    acceptCookiesBtn.addEventListener("click", function() {
        setCookie("cookiesAccepted", "true", 365 * 10); // Establecer cookie de aceptación válida por 10 años
        modal.style.display = "none";
    });

    // Manejar el clic en el botón "Rechazar cookies"
    rejectCookiesBtn.addEventListener("click", function() {
        setCookie("cookiesRejected", "true", 365 * 10); // Establecer cookie de rechazo válida por 10 años
        deleteCookie("cookiesAccepted"); // Eliminar la cookie de aceptación
        modal.style.display = "none";
    });

    // Función para establecer una cookie
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + "=" + value + ";expires=" + expires.toUTCString() + ";path=/";
    }

    // Función para obtener el valor de una cookie
    function getCookie(name) {
        const cookieName = name + "=";
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.indexOf(cookieName) === 0) {
                return cookie.substring(cookieName.length, cookie.length);
            }
        }
        return null;
    }

    // Función para eliminar una cookie
    function deleteCookie(name) {
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
    }
});
