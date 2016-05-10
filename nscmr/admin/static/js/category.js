var table;

function getDeleteData() {
    var selectedCategories = $.map(table.rows('.selected').data(), function (item) {
        return item[1];
    });
    if (selectedCategories.length == 0) throw new Error('Não há nenhum item selecionado');
    return { categories: selectedCategories };
}

function getEditData() {
  var edited = $('.edited');
  var categories = [];
  edited.each(function() {
    buildCategoryData($(this).closest('tr'), $(this), categories);
  });
  var form = new FormData();
  for (var i = 0; i < categories.length; i++) {
    if (categories[i].hasOwnProperty('base_img')) {
      form.append(categories[i]['id'], categories[i]['base_img']['img']);
      categories[i]['base_img'] = categories[i]['base_img']['name'];
    }
  }
  form.append('categories', JSON.stringify(categories));
  return form;
};

function buildCategoryData(row, cell, data) {
    var colName = cell.attr('id');
    var value;
    var cName = $($(table.row(row).data()[2])[0]).text();
    if (colName == 'parent') value = cell.find('select').first().val();
    else if (colName == 'base_img') value = { name: cName, img: cell.find('input')[0].files[0] };
    else value = cell.find('input').first().val();
    var cId = table.row(row).data()[1];
    var inserted = false;
    for (i = 0; i < data.length; i++) {
      if (data[i].id == cId) {
        data[i][colName] = value;
        inserted = true;
      }
    }
    if (!inserted) {
      var category = {
        id: cId,
      };
      category[colName] = value;
      data.push(category);
    }
}
$(document).ready(function() {
// datatable
  table = $('#datatable').DataTable({
    order: [],
    columnDefs: [{
      className: 'select',
      orderable: false,
      width: "3%",
      targets: 0
    }],
    select: {
      style: 'multi',
      selector: 'input[data-toggle=select-row]'
    },
  });

  $("#datatable tbody").on('click', 'td', function(e) {
    if ($(e.target).hasClass('edit-attribute')) {
      var cell = $(e.target).closest('td');
      var value = cell.find('.value').text();
      var row = cell.closest('tr');
      cell.addClass('edited');
      // hide current cell content
      cell.children().toggleClass('hidden');
      if (cell.find('input').length === 0 && cell.find('select').length === 0) {
        if (cell.hasClass('parent')) {
          editField = editParentField.clone();
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
        }
        cell.append(editField);
        cell.append($('<a href="#"><span class="undo-edit glyphicon glyphicon-remove"></span></a>'));
        if (cell.hasClass('parent')) editField.select2({}).val(choice).trigger('change');
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
