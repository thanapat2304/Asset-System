document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const h4Elements = document.querySelectorAll('.sidebar-links h4');

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });
});

document.getElementById('AS_Date').addEventListener('input', function() {
    const dateValue = this.value;
    if (dateValue) {
        const year = dateValue.split('-')[0];
        document.getElementById('YR').value = year;
    } else {
        document.getElementById('YR').value = '';
    }
});