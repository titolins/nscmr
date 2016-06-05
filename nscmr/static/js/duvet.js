$(document).ready(function() {
  $(".trigger-menu").on('click', function() {
    var target = $($(this).data('target'));
    if (target.hasClass('open')) $('.open').removeClass('open');
    else target.toggleClass('open');
    return false;
  });
  $(".item-dropdown-toggle").on('click', function() {
    var target = document.getElementById($(this).data('toggle'));
    /*
    var rect = this.getBoundingClientRect();
    var left = rect.left - (target.offsetWidth - (rect.right - rect.left));
    target.style.right = "" + rect.right + "px";
    target.style.left = "" + left + "px";
    */
    //$('.open').removeClass('open');
    $(target).toggleClass('open');
  });
});
