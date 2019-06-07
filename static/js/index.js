$(document).ready(function() {
    $('#sign_up_btn').click(function() {
        window.location.replace("/account/signup")
    });

    $('#create_acc').click(function() {
        window.location.replace("/account/create")
    });
    $('#login_btn').click(function() {
        window.location.replace("/account/login")
    });
});