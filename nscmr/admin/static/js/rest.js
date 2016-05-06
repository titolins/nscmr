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
    var selection;
    try {
      selection = getDeleteData();
      var result = confirm("Tem certeza de que deseja deletar a seleção?");
      if (result) {
        $.ajax({
          type: "POST",
          url: deleteUri,
          data: JSON.stringify(selection, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(response) {
            alert(response);
            console.log(response);
            location.reload();
          },
          error: function(response) {
            alert(response.responseText);
            console.log(response.responseText);
          },
        });
      }
    } catch (e) {
      alert(e.message);
    }
  });
  $("#edit-btn").on('click', function() {
    var selection;
    try {
      selection = getEditData();
      var result = confirm("Tem certeza de que deseja fazer as edições indicadas?");
      if (result) {
        $.ajax({
          type: "POST",
          url: editUri,
          data: JSON.stringify(selection, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(response) {
            alert(response);
            console.log(response);
            location.reload();
          },
          error: function(response) {
            alert(response.responseText);
            console.log(response.responseText);
          },
        });
      }
    } catch (e) {
      alert(e.message);
    }
  });
});
