var table;

function getDeleteData() {
    var selectedCategories = $.map(table.rows('.selected').data(), function (item) {
        return item[1];
    });
    console.log(selectedCategories);
    if (selectedCategories.length == 0) throw new Error('Não há nenhum item selecionado');
    return { categories: selectedCategories };
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
