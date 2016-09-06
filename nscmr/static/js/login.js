document.addEventListener("DOMContentLoaded", function(event) { 
  // listeners for the custom btns
  document.getElementById("fb").addEventListener('click', function() {
    fb();
  });
});

function fb() {
  FB.login(function(response) {
    console.log(response);
    statusChangeCallback(response);
  });
};

// Google login functions
function gSignIn(user) {
  var profile = user.getBasicProfile();
  console.log("ID: " + profile.getId()); // Don't send this directly to your server!
  console.log('Full Name: ' + profile.getName());
  console.log('Given Name: ' + profile.getGivenName());
  console.log('Family Name: ' + profile.getFamilyName());
  console.log("Image URL: " + profile.getImageUrl());
  console.log("Email: " + profile.getEmail());

  // The ID token you need to pass to your backend:
  var id_token = user.getAuthResponse().id_token;
  console.log("ID Token: " + id_token);
  user = {
    name: profile.getName(),
    email: profile.getEmail(),
    oauth: {
      userToken: user.getAuthResponse().id_token,
      provider: 'google',
    }
  };
  console.log(user);
  logOAuthUser(user);
};

// Facebook login functions

FB.getLoginStatus(function(response) {
  statusChangeCallback(response);
});

function statusChangeCallback(response) {
  console.log('fb statusChangeCallback');
  if (response.status === 'connected') {
    console.log("Logged in to fb and authorized");
    fbLogin();
  } else if (response.status === 'not_authorized') {
    console.log("Logged in to fb but not authorized");
  } else {
    console.log("Not logged in to fb");
  }
};

function fbLogin() {
  FB.api('/me', {fields:['name','email','picture']},function(response) {
    /*
    var welcomeEl = document.getElementById('fb-welcome');
    var loginEl = document.getElementById('login');
    var welcome = "<img src='" + response['picture'] + "'/>" +
      "<h5>Bem vindo, " + response['name'] + "!</h5>";
    welcomeEl.innerHtml = welcome;
    loginEl.classList.add('hidden');
    welcomeEl.classList.remove('hidden');
    */
    user = {
      name: response['name'],
      email: response['email'],
      oauth: {
        userToken: FB.getAuthResponse()['accessToken'],
        provider: 'fb',
      }
    };
    console.log(user);
    logOAuthUser(user);
  });
};

function logOAuthUser(user) {
  $.ajax({
    type: "POST",
    url: loginUri,
    data: JSON.stringify(user, null, '\t'),
    headers: {
      "Content-Type": 'application/json;charset=UTF-8',
      "X-CSRFToken": csrfToken
    },
    success: function(data) {
      console.log(data);
      window.location.href = data['redirect'];
    },
    error: function(data) {
      console.log(data);
      //FB.logout();
    },
  });
};
