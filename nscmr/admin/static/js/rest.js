$(document).ready(function() {
  // preparing csrf for future ajax requests
  var csrftoken = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });

  $("#delete-btn").on("click", function() {
    var selectedProducts = [];
    $("input[data-toggle=row-selection]:checked").each(function() {
      var parent = $(this).closest("tr");
      selectedProducts.push($(parent).find(".id").text());
    });
    $.ajax({
      type: "POST",
      url: deleteUri,
      data: JSON.stringify(selectedProducts, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(response) {
        console.log(response);
        location.reload();
      },
    });
  });
});
