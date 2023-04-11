document.addEventListener('DOMContentLoaded', () => {
    var message = document.getElementById("messageAlert").textContent;
    if (message !== null || message !== "") {
        alert(message);
    }
});


