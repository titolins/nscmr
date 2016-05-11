$(document).ready(function() {
  $("#datatable tbody").on('click', 'td', function(e) {
    if ($(e.target).hasClass('edit-attribute')) {
      var cell = $(e.target).closest('td');
      var value = cell.find('.value').text();
      var row = cell.closest('tr');
      cell.addClass('edited');
      // hide current cell content
      cell.children().toggleClass('hidden');
      if (cell.find('input').length === 0 && cell.find('select').length === 0) {
        if (cell.hasClass('parent') || cell.hasClass('category')) {
          editField = editCategoryField.clone();
          // get all select options and disable itself
          var cId = row.find('#id').text();
          var options = $.map(editField.find("option"), function(item) {
            if ($(item).attr('value').split('_')[0] === cId) $(item).attr('disabled', true);
            return $(item).attr('value');
          });
          // find the current category and set it
          var choice = null;
          options.some(function(option) {
            if (option.split('_')[1] === value) {
              choice = option;
            }
          });
        } else if (cell.hasClass('name')) {
          editField = editNameField.clone();
        } else if (cell.hasClass('base_img')) {
          editField = editBaseImgField.clone();
        } else if (cell.hasClass('meta_description')) {
          editField = editMetaField.clone();
        } else if (cell.hasClass('email')) {
          editField = editEmailField.clone();
        } else if (cell.hasClass('dob')) {
          editField = editDobField.clone();
        }
        cell.append(editField);
        cell.append($('<a href="#"><span class="undo-edit glyphicon glyphicon-remove"></span></a>'));
        if (cell.hasClass('parent') || cell.hasClass('category')) editField.select2({}).val(choice).trigger('change');
        else if (!cell.hasClass('base_img')) editField.val(value);
      }
      return false;
    } else if ($(e.target).hasClass('undo-edit')) {
      var cell = $(e.target).closest('td');
      cell.removeClass('edited');
      cell.children().toggleClass('hidden');
      return false;
      }
  });


});
