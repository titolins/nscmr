var table;

function getDeleteData() {
    var selectedCategories = $.map(table.rows('.selected').data(), function (item) {
        return item[1];
    });
    if (selectedCategories.length == 0) throw new Error('Não há nenhum item selecionado');
    return { users: selectedCategories };
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
