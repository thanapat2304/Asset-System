document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const h4Elements = document.querySelectorAll('.sidebar-links h4');

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });
});