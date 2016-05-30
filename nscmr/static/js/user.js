$(document).ready(function() {
// function for changing user sections
  $('.list-group-item').on('click', function() {
    // get all items of the list, except the first one (which is always
    // kept active)
    var activeItem = $('a.list-group-item.active');
    console.log(activeItem);
    console.log(activeItem.data('toggle'));
    $(activeItem.data('toggle')).addClass('hidden');
    $($(this).data('toggle')).removeClass('hidden');

    // lastly, deactivate the last active list-group-item and activated
    // the clicked one
    activeItem.removeClass('active');
    $(this).addClass('active');
  });

  $('.edit-attribute').on('click', function() {
    console.log(this);
    $($(this).data('toggle')).toggleClass('hidden');
    $(this).closest('.field').toggleClass('hidden');
  });

  $('.cancel-edit-attribute').on('click', function() {
    $($(this).data('toggle')).toggleClass('hidden');
    $(this).closest('.input').toggleClass('hidden');
  });
});

