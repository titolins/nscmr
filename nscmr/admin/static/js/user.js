var table;

function getDeleteData() {
    var selectedCategories = $.map(table.rows('.selected').data(), function (item) {
        return item[1];
    });
    if (selectedCategories.length == 0) throw new Error('Não há nenhum item selecionado');
    return { users: selectedCategories };
}

function getEditData() {
  var edited = $('.edited');
  var users = [];
  edited.each(function() {
    buildUserData($(this).closest('tr'), $(this), users);
  });
  console.log(users);
  var form = new FormData();
  form.append('users', JSON.stringify(users));
  return form;
};

function buildUserData(row, cell, data) {
    var colName = cell.attr('id');
    var value;
    if (colName == 'dob') value = new Date( cell.find('input')[0].valueAsDate ).toISOString().substr(0,10);
    else value = cell.find('input').first().val()
    var uId = table.row(row).data()[1];
    var inserted = false;
    for (i = 0; i < data.length; i++) {
      if (data[i].id == uId) {
        data[i][colName] = value;
        inserted = true;
      }
    }
    if (!inserted) {
      var user = {
        id: uId,
      };
      user[colName] = value;
      data.push(user);
    }
}

$(document).ready(function() {
  $("#is_admin").change(function() {
    if ($(this).is(':checked')) {
      $(this).val("true");
    } else {
      $(this).val("false");
    }
  });

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
