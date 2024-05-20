document.addEventListener('DOMContentLoaded', function () {
    var showPasswordCheckbox = document.querySelector('.show-password-checkbox');
    var passwordField = document.querySelector('.password-field');

    if (showPasswordCheckbox && passwordField) {
        showPasswordCheckbox.addEventListener('change', function () {
            if (this.checked) {
                passwordField.type = 'text';
            } else {
                passwordField.type = 'password';
            }
        });
    }
});