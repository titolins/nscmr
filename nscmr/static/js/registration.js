function checkPassword() {
  var password = $("#password-txt").val();
  var confirmPassword = $("#confirm-password").val();
  if (password != confirmPassword) {
    $("#check-passwords-match").html("As senhas não são iguais!");
  } else {
    $("#check-passwords-match").html("As senhas são iguais.");
  }
};

function toggleAddress(checkbox) {
  if ($(checkbox).is(':checked')) {
    $(checkbox).val("true");
    $($(checkbox).data('toggle')).removeClass('hidden');
  }
};


$(document).ready(function() {
  $("#confirm-password").change(checkPassword);

  $("#has_address").change(function() {
    if ($(this).is(':checked')) $(this).val("true");
    else $(this).val("false");
    $($(this).data('toggle')).toggleClass('hidden');
  });

  toggleAddress(document.getElementById('has_address'));
});
