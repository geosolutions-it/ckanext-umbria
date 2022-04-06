/**
 * Scroll to top button
 */

window.addEventListener('load', function () {
    $(document).scroll(handleScroll)
    
    function handleScroll() {
        var scrollToTopBtn = $('.move-top');
        var rootElement = $(':root')[0];
        var scrollTotal = rootElement.scrollHeight - rootElement.clientHeight;
        var header = $('header.masthead');
        var headerHeight = header.height();
        if ((rootElement.scrollTop / scrollTotal) > 0.30) {
                // Show button
            scrollToTopBtn.addClass("showBtn");
                } else {
                // Hide button
            scrollToTopBtn.removeClass("showBtn");
        }
        if ((rootElement.scrollTop / headerHeight) > 1) {
            $('div.collapse.navbar-collapse').addClass('fixed-top');
        } else {
            $('div.collapse.navbar-collapse').removeClass('fixed-top');
        }
    }
});