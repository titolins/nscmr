$(document).ready(function() {
  var selects = document.getElementsByTagName('select');
  var variantId = window.location.pathname.split('/').pop();
  for (var n = 0; n < selects.length; n++) {
    var select = selects[n];
    var options = select.getElementsByTagName('option');
    for (var i = 0; i < options.length; i++) {
      var value = options[i].value;
      if (value.startsWith(variantId)) {
        select.value = value;
      }
    }
  }

  $("select").change(function(){
    console.log('ok');
    var newLocation = window.location.pathname.split('/');
    newLocation.pop();
    newLocation.push($(this).find('option:selected').val());
    window.location = newLocation.join('/');
  });
});

