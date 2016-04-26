var validEmail = false

function validateEmail() {
  // get the email field and the error element
  var email = $("#email");
  var err = $("#email-error");
  // regex for emails
  var re = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/
  // if email is valid, set variable to true (used in validateForm)
  if (re.test(email.val())) {
    validEmail = true
    // avoid adding the same class twice, which could leed us to difficulty to
    // remove it afterwards
    if (!err.hasClass("hidden")) {
      err.addClass("hidden");
    }
  // if it isn't, set to false
  } else {
    validEmail = false
    // remove hidden if exists and writes error msg
    if (err.hasClass("hidden")) {
      err.removeClass("hidden");
      $("#email-error li").html("Email inválido!");
    }
  }
  // tries to validate the form (we do not check the password field in this
  // method)
  validateForm();
};

function validateForm() {
  // simple required validator
  var blankPass = $("#password").val() == "";
  if (validEmail && !blankPass) {
    $("#login-btn").removeAttr("disabled");
  } else {
    $("#login-btn").attr("disabled", "disabled");
  }
}

/*
$(document).ready(function() {
  $("#email").change(validateEmail);
});

$(document).ready(function() {
  $("#password").change(validateForm);
});
*/
