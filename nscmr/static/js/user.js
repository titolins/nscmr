// function for changing user sections
$('.list-group-item').on('click', function() {
  // get all items of the list, except the first one (which is always
  // kept active)
  items = $('.list-group-item:not(:first-child)');
  // grab the id of the content relative to the calling element
  // we have to do this outside the each loop, as the this argument
  // refers to the loop item in the each loop scope.
  show_id = $(this).attr("data-toggle");

  // iterate though all selected items
  items.each(function(index) {
    // if item is active, we found which one we have to hide
    if ($(this).hasClass("active")) {
      // hide the last active element content and show the
      // clicked element content
      $($(this).attr("data-toggle")).css('display','none');
      // the button to confirm logout has to be individually
      // handled, as it is not influenced by it's parent
      // visibility
      $("#logout-confirm-btn").css('display', 'none');
      $(show_id).css('display', 'inline');
      // in the case of the logout btn, we have to activate it
      // manually, as per the above.
      if (show_id == "#logout") {
        $("#logout-confirm-btn").css('display', 'inline');
      }
      // breaks the loop
      return false;
    }
  });
  // lastly, deactivate the last active list-group-item and activated
  // the clicked one
  items.removeClass('active');
  $(this).addClass('active');
});

