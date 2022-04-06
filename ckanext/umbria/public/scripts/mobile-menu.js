/**
 * Mobile menu
 */

window.addEventListener('load', function () {
    var menuButton = $('button.navbar-toggle');
    var checkBox = $('#show-menu-main');
    var mobileMenu = $('.mobile-menu');
    var closeButton = $('.show-menu-main');
    menuButton.on('click', function () { return handleMobileMenu(true) });
    closeButton.on('click', function () { return handleMobileMenu(false) });
    
    function handleMobileMenu(value) {

        checkBox.prop('checked', value);

        if (checkBox.prop('checked')) {
            menuButton.hide();
            mobileMenu.css({
                display: 'block'
            })
        } else {
            menuButton.show();
            mobileMenu.css({
                display: 'none'
            })
        }
    }
});