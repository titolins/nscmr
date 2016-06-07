$(document).ready(function() {
  $(".trigger-menu").on('click', function() {
    var target = $($(this).data('target'));
    if (target.hasClass('open')) $('.open').removeClass('open');
    else target.toggleClass('open');
    return false;
  });
  $(".item-dropdown-toggle").on('click', function() {
    var target = document.getElementById($(this).data('toggle'));
    if (target.id.startsWith('categories')) {
      $('.item-dropdown').removeClass('open');
      if (window.innerWidth < 768) target.style.left = 0;
      else {
        var rect = this.getBoundingClientRect();
        var left = rect.right - (target.offsetWidth - (rect.left - rect.right));
        target.style.left = "" + rect.left + "px";
        target.style.right = "" + rect.right + "px";
        //$('.open').removeClass('open');
      }
    }
    else {
      if (target.id.startsWith('cart') && !target.classList.contains('open')) {
        if (window.innerWidth < 768) $('#navbar-menu-btn').click();
        else $('.item-dropdown').removeClass('open');
      } else if (target.id.startsWith('user') || target.id.startsWith('login')) {
        document.getElementById('categories-dropdown').classList.remove('open');
      }
      if (window.innerWidth < 768) target.style.right = 0;
      else {
        var rect = this.getBoundingClientRect();
        var left = rect.left - (target.offsetWidth - (rect.right - rect.left));
        target.style.right = "" + rect.right + "px";
        target.style.left = "" + left + "px";
        console.log(target.id);
      }
    }
    $(target).toggleClass('open');
  });
});
