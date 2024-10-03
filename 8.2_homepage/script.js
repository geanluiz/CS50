document.addEventListener('DOMContentLoaded', function() {
    localStorage.setItem('mode', 'dark');
    let mode = localStorage.getItem('mode');

    let icon = document.querySelector('#theme-img');
    let body = document.querySelector('body');

    body.setAttribute('data-bs-theme', mode);

    icon.addEventListener('click', function() {
        if (mode === 'dark'){
            localStorage.setItem('mode', 'light');

            body.setAttribute('data-bs-theme', mode);
            icon.setAttribute('src', 'light-mode.png'); // Black-icon
        } else {
            localStorage.setItem('mode', 'light');

            body.setAttribute('data-bs-theme', mode);
            icon.setAttribute('src', 'dark-mode.png'); // Clear-icon
        }
    });
});
