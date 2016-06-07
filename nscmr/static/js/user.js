$(document).ready(function() {
// function for changing user sections
  $('.list-group-item').on('click', function() {
    // get all items of the list, except the first one (which is always
    // kept active)
    var activeItem = $('a.list-group-item.active');
    $(activeItem.data('toggle')).addClass('hidden');
    $($(this).data('toggle')).removeClass('hidden');

    // lastly, deactivate the last active list-group-item and activated
    // the clicked one
    activeItem.removeClass('active');
    $(this).addClass('active');
  });
});

