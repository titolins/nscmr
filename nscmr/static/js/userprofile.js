angular.module('angularApp', ['ui.mask'])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]).controller("UserProfileController", ["$scope","$http", function($scope, $http) {
  getUser();
  getCart();

  $scope.addToWishlist = function(variantId) {
    var data = { 'variant_id': variantId };
    sendPost(addToWishlistUri, data);
  }

  $scope.addToCart = function(variantId) {
    var data = { 'variant_id': variantId };
    sendPost(addToCartUri, data, function(response) {
      console.log(response);
      alert(response.data);
      getCart();
    });
  }

  function getCart() {
    $http({
      url: getCartUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      $scope.initialCart = response.data;
      $scope.cart = angular.copy($scope.initialCart);
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  function getAddresses() {
    $http({
      url: getAddressesUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      $scope.initialAddresses = response.data;
      $scope.addresses = angular.copy($scope.initialAddresses);
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  function getUser() {
    $http({
      url: getUserUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      $scope.initialUser = response.data;
      $scope.user = angular.copy($scope.initialUser);
      $scope.initialAddresses = response.data['addresses'];
      $scope.addresses = angular.copy($scope.initialAddresses);
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  $scope.toggleEdit = function($event) {
    var target = $event.currentTarget;
    // if we are cancelling the edit, we simply reset the cart (redrawing the
    // template)
    if (target.classList.contains('cancel-cart')) $scope.cart = angular.copy($scope.initialCart);
    else if (target.classList.contains('cancel-name')) $scope.user['name'] = $scope.initialUser['name'];
    else if (target.classList.contains('cancel-email')) $scope.user['email'] = $scope.initialUser['email'];
    else if (target.classList.contains('cancel-dob')) $scope.user['dob'] = $scope.initialUser['dob'];
    else if (target.classList.contains('cancel-addresses')) $scope.addresses = angular.copy($scope.initialAddresses);
    else {
      var field = target.parentNode;
      while (!field.classList.contains('field')) field = field.parentNode;
      field.getElementsByClassName('field-value')[0].classList.toggle('hidden');
      field.getElementsByClassName('field-input')[0].classList.toggle('hidden');
    }
  }

  $scope.removeItem = function(var_id) {
    data = {
      'id': var_id,
      'quantity': 0
    }
    edit(data);
  };

  $scope.confirmEdit = function(item) {
    var data = {
      'id': item['_id'],
      'quantity': item['quantity']
    }
    edit(data);
  };

  function edit(data) {
    console.log(data);
    $http({
      method: 'POST',
      url: editCartUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
      alert(response.data);
      getCart();
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  };

  $scope.deleteAddress = function(addressId) {
    var data = { 'address_id': addressId };
    sendPost(removeAddressUri, data, function(response) {
      console.log(response);
      alert(response.data);
      getAddresses();
    });
  };

  function sendPost(uri, data, successCallback, errorCallback) {
    $http({
      method: 'POST',
      url: uri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(successCallback || function successCallback(response) {
      console.log(response);
      alert(response.data);
    }, errorCallback || function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  };

  $scope.editUser = function() {
    var userFields = [ 'name', 'email', 'dob' ];
    var user = {};
    userFields.forEach(function(field) {
      if ($scope.user[field] != $scope.initialUser[field]) user[field] = $scope.user[field];
    });
    console.log(user);
    sendPost(editUserUri, user, function(response) {
      console.log(response);
      alert(response.data);
      getUser();
    });
  };

  $scope.form = {};
  $scope.form_errors = {};
  $scope.form_success = '';

  $scope.addAddress = function() {
    $http({
      method: 'POST',
      url: addAddressUri,
      data: $.param($scope.form),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        "X-CSRFToken": csrfToken
      }
    }).then(function successCallback(response) {
      console.log(response);
      $scope.form_errors = {};
      $scope.form_success = response.data;
      getAddresses();
    }, function errorCallback(response) {
      console.log(response);
      $scope.form_success = '';
      $scope.form_errors = response.data;
      console.log($scope.form_errors);
    });
  }

  $scope.getAddressByCep = function() {
    var apiUri = 'http://api.postmon.com.br/v1/cep/' + $scope.form.zip_code;
    $http({url:apiUri}).then(function success(response) {
      $scope.form.street_address_1 = response.data['logradouro'];
      $scope.form.street_address_2 = response.data['bairro'];
      $scope.form.city = response.data['cidade'];
      $scope.form.state = response.data['estado'];
    }, function error(response) {});

  }

}]);

