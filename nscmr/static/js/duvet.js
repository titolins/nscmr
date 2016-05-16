$(document).ready(function() {
  $(".trigger-menu").on('click', function() {
    var target = $($(this).data('target'));
    if (this.id == "sidebar-btn") {
      $(this).toggleClass('fixed');
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
});
