/**
 * Scroll to top button
 */

$(document).load(function () {
    $(document).scroll(handleScroll)
    
    function handleScroll() {
        var scrollToTopBtn = $('.move-top');
        var rootElement = $(':root')[0];
        var scrollTotal = rootElement.scrollHeight - rootElement.clientHeight;
        if ((rootElement.scrollTop / scrollTotal) > 0.30) {
                // Show button
            scrollToTopBtn.addClass("showBtn");
                } else {
                // Hide button
            scrollToTopBtn.removeClass("showBtn");
            }
    }
});