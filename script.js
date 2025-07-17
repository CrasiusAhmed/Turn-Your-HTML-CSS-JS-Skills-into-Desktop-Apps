// JavaScript function to call a Python function
async function callPython() {
    // Access the 'pywebview' object which bridges JS and Python
    // 'pywebview.api' exposes the Python functions defined in the API
    const response = await pywebview.api.say_hello_from_python('JavaScript');
    document.getElementById('message').innerText = response;
}

// JavaScript function that Python can call
// This function is exposed to Python via the 'expose' method in Python
function updateMessage(msg) {
    document.getElementById('message').innerText = msg;
}

// When the window is loaded, expose the JavaScript function to Python
// This makes 'updateMessage' available for Python to call
window.addEventListener('pywebviewready', function() {
    pywebview.api.init_js_ready(); // Notify Python that JS is ready
});
