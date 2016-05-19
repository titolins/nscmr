$(document).ready(function() {
  $(".trigger-menu").on('click', function() {
    var target = $($(this).data('target'));
    if (this.id == "sidebar-btn") {
      //$(this).toggleClass('fixed');
      var buyMenu = $("#buy-menu");
      if (buyMenu.hasClass('open')) {
        buyMenu.removeClass('open');
        $("#buy-btn").removeClass('active');
      }
    }
    $(this).toggleClass('active');
    target.toggleClass('open');
    return false;
  });
  $(".item-dropdown-toggle").on('click', function() {
    var target = document.getElementById($(this).data('toggle'));
    var rect = this.getBoundingClientRect();
    var left = rect.left - (target.offsetWidth - (rect.right - rect.left));
    target.style.right = "" + rect.right + "px";
    target.style.left = "" + left + "px";
    $(target).toggleClass('open');
  });
});
