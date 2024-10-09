document.addEventListener('DOMContentLoaded', function() {


    /* video: https://www.youtube.com/watch?v=2j_kBqpFK-g */


    if (localStorage.getItem('mode') === null){
        localStorage.setItem('mode', 'dark');
    }
    var mode = localStorage.getItem('mode');
    const body = document.querySelector('body');

    body.setAttribute('data-bs-theme', mode);

    const icon = document.querySelector('#theme-img');

    if (mode === 'light'){
        icon.src = 'dark-mode.png';
        body.setAttribute('data-bs-theme', 'light');
    } else if (mode === 'dark'){
        icon.src = 'light-mode.png';
        body.setAttribute('data-bs-theme', 'dark');
    };

    icon.addEventListener('click', function() {
        console.log('click');
        console.log(mode);

        if (body.getAttribute('data-bs-theme') == 'light'){
            icon.src = 'light-mode.png';
            localStorage.setItem('mode', 'dark');
            body.setAttribute('data-bs-theme', 'dark');
            console.log(mode);
        } else if (body.getAttribute('data-bs-theme') === 'dark'){
            icon.src = 'dark-mode.png';
            localStorage.setItem('mode', 'light');
            body.setAttribute('data-bs-theme', 'light');
            console.log(mode);
        };
    });
});
