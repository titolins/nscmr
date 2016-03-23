function checkPassword() {
  var password = $("#password-txt").val();
  var confirmPassword = $("#confirm-password").val();
  if (password != confirmPassword) {
    $("#check-passwords-match").html("As senhas não são iguais!");
  } else {
    $("#check-passwords-match").html("As senhas são iguais.");
  }
};

$(document).ready(function() {
  $("#confirm-password").change(checkPassword);
});
