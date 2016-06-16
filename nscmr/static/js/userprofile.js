angular.module('angularApp', ['ui.mask'])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]).controller("UserProfileController", ["$scope","$http","addressesService", "cartService", function($scope, $http, addressesService, cartService) {
  $scope.addressesService = addressesService;
  $scope.cartService = cartService;
  $scope.user = {},
  $scope.wishlist = [];
  getUser();
  getWishlist();
  $scope.addressesService.update(getAddressesUri);

  $scope.addToWishlist = function(variantId) {
    var data = { 'variant_id': variantId };
    sendPost(addToWishlistUri, data);
  }

  function getUser() {
    $http({
      url: getUserUri,
    }).then(function successCallback(response) {
      if (response.data['dob'] !== null) response.data['dob'] = new Date(response.data['dob']);
      $scope.initialUser = response.data;
      $scope.user = angular.copy($scope.initialUser);
      console.log(response.data['addresses']);
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  function getWishlist() {
    $http({ url: getWishlistUri }).then(function success(response) {
      $scope.wishlist = response.data;
      console.log($scope.wishlist);
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.toggleEdit = function($event) {
    var target = $event.currentTarget;
    // if we are cancelling the edit, we simply reset the cart (redrawing the
    // template)
    if (target.classList.contains('cancel-cart')) $scope.cartService.reset();
    else if (target.classList.contains('cancel-name')) $scope.user['name'] = $scope.initialUser['name'];
    else if (target.classList.contains('cancel-email')) $scope.user['email'] = $scope.initialUser['email'];
    else if (target.classList.contains('cancel-dob')) $scope.user['dob'] = $scope.initialUser['dob'];
    else if (target.classList.contains('cancel-addresses')) { $scope.addressesService.reset(); }
    var field = target.parentNode;
    while (!field.classList.contains('field')) field = field.parentNode;
    field.getElementsByClassName('field-value')[0].classList.toggle('hidden');
    field.getElementsByClassName('field-input')[0].classList.toggle('hidden');
  }


  $scope.removeFromWishlist = function(var_id) {
    data = { 'id': var_id };
    console.log(data);
    $http({
      method: 'POST',
      url: removeFromWishlistUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      console.log(response);
      alert(response.data);
      getWishlist();
    }, function error(response) {
      console.log(response);
      alert(response.data);
    });
  };

  $scope.deleteAddress = function(addressId) {
    var data = { 'address_id': addressId };
    sendPost(removeAddressUri, data, function(response) {
      $scope.addressesService.update(getAddressesUri);
      alert(response.data);
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
      console.log($scope.initialUser[field]);
      console.log($scope.user[field]);
      if ($scope.user[field] != $scope.initialUser[field]) user[field] = $scope.user[field];
      if (field === 'dob') user[field] = $scope.parseDate(user[field]);
    });
    console.log(user);
    sendPost(editUserUri, user, function(response) {
      console.log(response);
      alert(response.data);
      getUser();
    });
  };


  $scope.parseDate = function(date) {
    if (date !== undefined) {
      var year  = date.getFullYear().toString(),
          month = (date.getMonth()+1).toString(),
          day   = date.getDate().toString();
      return (day[1]?day:'0'+day[0])+'/'+(month[1]?month:'0'+month[0])+'/'+year;
    }
    return "";
  };

  $scope.buildLink = function(catPermalink, prodPermalink, varId) {
    var baseUrl = '/catalogo/';
    return baseUrl + catPermalink + '/' + prodPermalink + '/' + varId;
  };

}]);

