document.addEventListener('DOMContentLoaded', function() {

    if (localStorage.getItem('mode') === null){
        localStorage.setItem('mode', 'dark');
    }
    var mode = localStorage.getItem('mode');
    const body = document.querySelector('body');

    body.setAttribute('data-bs-theme', mode);

    const icon = document.querySelector('.material-symbols-outlined');

    if (mode === 'light'){
        icon.innerHTML = 'mode_night';
        body.setAttribute('data-bs-theme', 'light');
    } else if (mode === 'dark'){
        icon.innerHTML = 'sunny';
        body.setAttribute('data-bs-theme', 'dark');
    };

    icon.addEventListener('click', function() {
        if (body.getAttribute('data-bs-theme') == 'light'){
            icon.innerHTML = 'sunny';
            localStorage.setItem('mode', 'dark');
            body.setAttribute('data-bs-theme', 'dark');
        } else if (body.getAttribute('data-bs-theme') === 'dark'){
            icon.innerHTML = 'mode_night';
            localStorage.setItem('mode', 'light');
            body.setAttribute('data-bs-theme', 'light');
        };
    });
});
