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

});
