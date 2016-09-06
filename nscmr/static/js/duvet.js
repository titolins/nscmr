$(document).ready(function(e) {
  $(".logout-btn").on('click', function(e) {
    e.preventDefault();
    var logoutBtn = $(this);
    FB.getLoginStatus(function(response) {
      if(response['status'] === "connected") {
        console.log('connected. disconnecting');
        FB.logout(function(response) {
          console.log('inside fb logout callback');
          console.log(response);
          window.location.href = logoutBtn.prop('href');
        });
      } else {
        console.log('not connected to fb. going for google.');
        try {
          var auth2 = gapi.auth2.getAuthInstance();
          auth2.signOut().then(function() {
            window.location.href = logoutBtn.prop('href');
          });
        } catch(e) {
          window.location.href = logoutBtn.prop('href');
        }
      }
    });
  });
  $(".trigger-menu").on('click', function() {
    var target = $($(this).data('target'));
    if (target.hasClass('open')) $('.open').removeClass('open');
    else target.toggleClass('open');
    return false;
  });

  $(".item-dropdown-toggle").on('click', function() {
    var target = document.getElementById($(this).data('toggle'));
    var closeSelection;
    if (target.id.startsWith('categories')) {
      closeSelection = $('.open:not(#'+target.id+'):not(#navbar-menu)');
      if (window.innerWidth < 768) target.style.left = 0;
      else {
        var rect = this.getBoundingClientRect();
        var left = rect.right - (target.offsetWidth - (rect.left - rect.right));
        target.style.left = "" + (rect.left - (rect.width/2)) + "px";
        target.style.right = "" + (rect.right - (rect.width/2)) + "px";
      }
    }
    else {
      closeSelection = $('.open:not(#'+target.id+')');
      if (window.innerWidth < 768) target.style.right = 0;
      else {
        var rect = this.getBoundingClientRect();
        var left = rect.left - (target.offsetWidth - (rect.right - rect.left));
        target.style.right = "" + rect.right + "px";
        target.style.left = "" + left + "px";
      }
    }
    closeSelection.removeClass('open');
    $(target).toggleClass('open');
    return false;
  });

  $(document).click(function(event) { 
      if(!$(event.target).closest('.item-dropdown').length) {
        document.getElementsByClassName('item-dropdown open')[0].classList.remove('open');
      }
  });
});
