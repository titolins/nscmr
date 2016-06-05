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

  $('.edit-attribute').on('click', function() {
    $($(this).data('toggle')).toggleClass('hidden');
    $(this).closest('.field').toggleClass('hidden');
    return false;
  });

  $('.cancel-edit-attribute').on('click', function() {
    $($(this).data('toggle')).toggleClass('hidden');
    $(this).closest('.input').toggleClass('hidden');
    return false;
  });

  $('.confirm-edit-attribute').on('click', function() {
    var data = {
      'quantity': $(this).closest('.input').find('input').val(),
      'id': $(this).closest('.panel-body').find('.item-id').text()
    };
    $.ajax({
      url: editCartUri,
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(data),
      success: function(response) {
        console.log(response);
      },
      error: function(response) {
        console.log(response);
      }
    });
    return false;
  });

  $('.remove-item').on('click', function() {
    data = {
      'id': $(this).closest('.panel').find('.item-id').text(),
      'quantity': 0
    };
    console.log(data);
    $.ajax({
      url: editCartUri,
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(data),
      success: function(response) {
        console.log(response);
      },
      error: function(response) {
        console.log(response);
      }
    });
    return false;
  });
});

