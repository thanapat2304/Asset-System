function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

window.onload = function() {
    const error = getUrlParameter('error');
    if (error) {
        document.querySelector('.popup-overlay').style.display = 'block';
        document.getElementById('errorPopup').style.display = 'block';

        setTimeout(() => {
            document.querySelector('.popup-overlay').style.display = 'none';
            document.getElementById('errorPopup').style.display = 'none';
        }, 500);
    }
};

const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');
        
togglePassword.addEventListener('click', function (e) {
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;

    const icon = type === 'password' ? 'visibility' : 'visibility_off';
    togglePassword.innerHTML = `<i class="material-icons">${icon}</i>`;
});