function checkPassword() {
  var password = $("#password-txt").val();
  var confirmPassword = $("#confirm-password").val();
  if (password != confirmPassword) {
    $("#check-passwords-match").html("Passwords do not match!");
  } else {
    $("#check-passwords-match").html("Passwords match.");
  }
};

$(document).ready(function() {
  $("#confirm-password").keyup(checkPassword);
});
