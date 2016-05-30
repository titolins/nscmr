function renderEdit(data) {
  return '<td><div class="value">' + data +
    '</div><a href="#"><span class="edit-attribute glyphicon glyphicon-edit"' +
    ' aria-hidden="true"></span></a></td>';
};
var table;
var tableColumns = [
  {
    data: null,
    render: function (data, type, row) {
      if ( type === 'display' ) {
        return '<div class="checkbox3 checkbox-inline checkbox-check checkbox-light">' +
          '<input type="checkbox" data-toggle="select-row" id="select-'+data.id+'">' +
          '<label for="select-'+data.id+'"></label></div>';
      }
      return data;
    },
    className: "dt-body-center",
  },
  { data: 'id' },
  {
    data: 'name',
    render: function(data, type, row) {
      if ( type === 'display') {
        return renderEdit(data);
      }
      return data;
    }
  },
  {
    data: 'description',
    render: function(data, type, row) {
      if ( type === 'display') {
        return renderEdit(data);
      }
      return data;
    }
  },
  { data: 'category',
    render: function(data, type, row) {
      if ( type === 'display') {
        return renderEdit(data);
      }
      return data;
    }
  },
  { data: 'attributes' },
  { data: 'meta_description',
    render: function(data, type, row) {
      if ( type === 'display') {
        return renderEdit(data);
      }
      return data;
    }
  },
  { data: 'permalink' },
];

function getColName(row, cell) {
  var cols = {
    nome: 'name',
    descrição: 'description',
    categoria: 'category',
    atributos: 'atributos',
    'meta-description': 'meta_description',
    permalink: 'permalink',
    preço: 'price',
    sku: 'sku',
    imagens: 'images',
    quantidade: 'quantity'
  };
  var colName;
  if (row.hasClass('child')) {
    var column = cell.parent().children().index(cell);
    colName = cell.closest('table').find('th')[column].innerHTML.toLowerCase();
  } else {
    var column = table.column(cell.index());
    colName = $(column.header()).text().toLowerCase();
  }
  return cols[colName];
}

function getDeleteData() {
    var selectedProducts = $.map(table.rows('.selected').data(), function (item) {
        return item.id;
    });
    var selectedVariants = $.map($('.child-row-table tr.selected'), function(row) {
      return $(row).find('input').first().attr('id').split('-')[1];
    });
    if ((selectedProducts.length + selectedVariants.length) == 0) throw new Error('Não há nenhum item selecionado');
    return { variants: selectedVariants, products: selectedProducts };
}

function buildProductData(row, cell, data) {
    var colName = getColName(row, cell);
    var value;
    if (colName == 'category') value = cell.find('select').first().val();
    else value = cell.find('input').first().val();
    var products;
    var pId;
    if (row.hasClass('child')) {
      products = data['variants'];
      pId = row.find('input').first().attr('id').split('-')[1];
    } else {
      products = data['products'];
      pId = table.row(row).data().id;
    }
    var inserted = false;
    for (i = 0; i < products.length; i++) {
      if (products[i].id == pId) {
        products[i][colName] = value;
        inserted = true;
      }
    }
    if (!inserted) {
      var product = {
        id: pId,
      };
      product[colName] = value;
      products.push(product);
    }
}

function getEditData() {
  var edited = $('.edited');
  var data = {
    products: [],
    variants: [],
  }
  edited.each(function() {
    buildProductData($(this).closest('tr'), $(this), data);
  });
  form = new FormData();
  form.append('data', JSON.stringify(data));
  return form;
};

function toggleVariants(variants) {
  if ($(variants).is(':checked')) {
    $(variants).val("true");
    $($(variants).data("enable")).show();
    $($(variants).data("disable")).hide();
  }
}

$(document).ready(function() {
  // this code hides or shows the variants attributes (on the creation form)
  // and correctly sets it's value, as used by our backend
  $("#has_variants").change(function() {
    if ($(this).is(':checked')) {
      $(this).val("true");
      $($(this).data("enable")).show();
      $($(this).data("disable")).hide();
    } else {
      $(this).val("false");
      $($(this).data("enable")).hide();
      $($(this).data("disable")).show();
    }
  });
  toggleVariants(document.getElementById('has_variants'));

  // add remove fields functionality (for product images and variants)
  $("div[data-toggle=fieldset]").each(function() {
    var $this = $(this);
    //Add new entry
    $this.find("button[data-toggle=fieldset-add-row]").on('click', function() {
      var target = $($(this).data("target"));
      var oldrow = target.find("[data-toggle=fieldset-entry]:last");
      // destroy select2 before cloning
      oldrow.find("select").select2('destroy');
      var row = oldrow.clone(true, true);
      var elem_num = parseInt(row.attr("data-id")) + 1;
      row.attr('data-id', elem_num);
      row.find(":input").each(function() {
        var id = $(this).attr('id').replace('-' + (elem_num - 1), '-' + (elem_num));
        $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
      });
      oldrow.after(row);
      // re-enable select2 after insertion
      oldrow.find("select").select2();
      row.find("select").select2();
    }); //End add new entry

    //Remove row
    $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
      if($this.find("[data-toggle=fieldset-entry]").length > 1) {
        var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
        var entries = thisRow.nextAll();
        var elem_num = parseInt(thisRow.attr('data-id'));
        thisRow.remove();
        entries.each(function() {
          $(this).attr('data-id', elem_num);
          $(this).find(":input").each(function() {
            var id = $(this).attr('id').replace(/-(\d{1,4})/m, '-' + elem_num);
            $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
          });
          elem_num += 1;
        });
      }
    }); //End remove row
  });

  // datatable
  table = $('#datatable').DataTable({
    dom: 'Bfrtip',
    ajax: getUri,
    paging: true,
    order: [],
    columns: tableColumns,
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
    bProcessing: true
  });

  // detailed info (variants) on child rows and edit functionality on btn click
  $("#datatable tbody").on('click', 'td', function(e) {
    if (e.target == this) {
      var row = table.row($(this).closest('tr'));
      if (row.child.isShown()) {
        row.child.hide();
        $(this).removeClass('shown');
      } else {
        var childRow = $(formatVariants(row.data().variants));
        row.child(childRow).show();
        $(".child-row-table .checkbox3 label").click(function() {
          var row = $(this).closest('tr');
          if (!$(this).prev().is(':checked')) row.addClass('selected');
          else row.removeClass('selected');
        });
        $(this).addClass('shown');
      }
      return false;
    } else if ($(e.target).hasClass('edit-attribute')) {
      var cell = $(e.target).closest('td');
      var value = cell.find('.value').text();
      var row = cell.closest('tr');
      cell.addClass('edited');
      // hide current cell content
      cell.children().toggleClass('hidden');
      if (cell.find('input').length === 0 && cell.find('select').length === 0) {
        var colName = getColName(row, cell);
        if (colName == 'category') {
          editField = editCategoryField.clone();
          // get all select options
          var options = $.map($("select#category:first option"), function(item) {
            return $(item).attr('value');
          });
          // find the current category and set it
          var choice;
          options.some(function(option) {
            if (option.split('_')[1] === value) {
              choice = option;
              return true;
            }
          });
        } else if (colName == 'name') {
          editField = editNameField.clone();
        } else if (colName == 'description') {
          editField = editDescriptionField.clone();
        } else if (colName == 'sku') {
          editField = editSKUField.clone();
        } else if (colName == 'price') {
          editField = editPriceField.clone();
          value = parseFloat(value.split(' ')[1]);
        } else if (colName == 'quantity') {
          editField = editQtyField.clone();
        } else if (colName == 'meta_description') {
          editField = editMetaField.clone();
        }
        cell.append(editField);
        cell.append($('<a href="#"><span class="undo-edit glyphicon glyphicon-remove"></span></a>'));
        if (colName == 'category') editField.select2({}).val(choice).trigger('change');
        else editField.val(value);
      }
      return false;
    } else if ($(e.target).hasClass('undo-edit')) {
      var cell = $(e.target).closest('td');
      cell.removeClass('edited');
      cell.children().toggleClass('hidden');
      return false;
    }
  });

  $('#select-all').on('click', function() {
    if ($(this).is(':checked')) {
      $('[data-toggle=select-row]').each(function() {
        $(this).closest('tr').addClass('selected');
        if (!$(this).is(':checked')) $(this).next().click();
      });
    } else {
      $('[data-toggle=select-row]').each(function() {
        $(this).closest('tr').removeClass('selected');
        if ($(this).is(':checked')) $(this).next().click();
      });
    }
  });


  // function used to format variants data to be used in datatable child rows
  var formatVariants = function( variants ) {
    var variantsInfo = '<table class="child-row-table">' +
      '<thead><tr role="row" class="child">' +
        '<th></th>' +
        '<th>SKU</th>' +
        '<th>Preço</th>' +
        '<th>Quantidade</th>' +
        '<th>Atributos</th>' +
        '<th>Imagens</th>' +
      '</tr></thead>' +
      '<tfoot><tr role="row" class="child">' +
        '<th></th>' +
        '<th>SKU</th>' +
        '<th>Preço</th>' +
        '<th>Quantidade</th>' +
        '<th>Atributos</th>' +
        '<th>Imagens</th>' +
      '</tr></tfoot>';
    variants.forEach(function(variant) {
      var variantImages = '';
      variant.images.forEach(function(img) {
        variantImages += '<a href="' + img['big'] + '">imagem</a> ';
      });
      var variantAttributes = '';
      if (variant.attributes != null) {
        for (var attr in variant.attributes) {
          variantAttributes += '<div><span>' + attr + ': </span><span>' + variant.attributes[attr] + '</span></div>';
        }
      }
      variantsInfo += '<tr class="child">' +
          '<td>' +
            '<div class="checkbox3 checkbox-inline checkbox-check checkbox-light">' +
              '<input type="checkbox" data-toggle="select-row" id="select-' + variant.id + '">' +
              '<label for="select-' + variant.id + '"></label>' + 
            '</div>' +
          '</td>' +
          '<td>' +
            '<div class="value">' + variant.sku + '</div>' +
            '<a href="#">' +
              '<span class="edit-attribute glyphicon glyphicon-edit" aria-hidden="true"></span>' +
            '</a>' +
          '</td>' +
          '<td>' +
            '<div class="value">' + variant.price + '</div>' +
            '<a href="#">' +
              '<span class="edit-attribute glyphicon glyphicon-edit" aria-hidden="true"></span>' +
            '</a>' +
          '</td>' +
          '<td>' +
            '<div class="value">' + variant.quantity + '</div>' +
            '<a href="#">' +
              '<span class="edit-attribute glyphicon glyphicon-edit" aria-hidden="true"></span>' +
            '</a>' +
          '</td>' +
          '<td>' + variantAttributes + '</td>' +
          '<td>' + variantImages + '</td>' +
        '</tr>';
    });
    variantsInfo += '</table>';
    return variantsInfo;
  };
});

