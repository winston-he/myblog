AJAX_HOST = "http://127.0.0.1"
AJAX_PORT = "5001"

function renderLoginPage() {
    window.location = AJAX_HOST + ":" + AJAX_PORT + "/accounts/login";
}