document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            console.log('Hamburger clicked');
        });
    } else {
        console.log('Elements not found');
    }

    const dropdown = document.querySelector('.dropdown');
    if (dropdown){
        dropdown.addEventListener('click', () => {
            const dropdownMenu = dropdown.querySelector('.dropdown-menu');
            if(dropdownMenu){
                dropdownMenu.classList.toggle('show');
            }
        });
    }
});