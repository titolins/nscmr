function validateEmail() {
  var email = $("#email");
  var err = $("#email-error");
  var re = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/
  if (re.test(email.val())) {
    if (!err.hasClass("hidden")) {
      err.addClass("hidden");
    }
  } else {
    if (err.hasClass("hidden")) {
      err.removeClass("hidden");
      $("#email-error li").html("Email inválido!");
    }
  }
};

$(document).ready(function() {
  $("#email").keyup(validateEmail);
});

