/**
 * Scroll to top button
 */

window.addEventListener('load', function () {
    var stickyNav = $('#sticky-top');
    var stickNavWrapper = $('#sticky-nav-wrapper');
    var currStickyPos = stickyNav.offset().top + window.pageYOffset;
    var navHeight = stickyNav.height();
    $(document).scroll(handleScroll);
    
    function handleScroll() {
        var scrollToTopBtn = $('.move-top');
        var rootElement = $(':root')[0];
        var scrollTotal = rootElement.scrollHeight - rootElement.clientHeight;

        if ((rootElement.scrollTop / scrollTotal) > 0.30) {
                // Show button
            scrollToTopBtn.addClass('showBtn');
                } else {
                // Hide button
            scrollToTopBtn.removeClass('showBtn');
        }

        // fix header to the top
         if(window.pageYOffset > currStickyPos) {
             stickyNav.addClass('fixed-top');
             stickNavWrapper.css({marginBottom: `${navHeight}px`})
         } else {
             if ((window.pageYOffset + navHeight) > currStickyPos) {
                 stickNavWrapper.css({ marginBottom: 0 });
              }
             stickyNav.removeClass('fixed-top');
             stickNavWrapper.css({ marginBottom: 0 });
        }
    }
});