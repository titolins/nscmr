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
      if (response.data['dob'] !== null) {
        var splitDob = response.data['dob'].split('-');
        response.data['dob'] = new Date(splitDob[0], splitDob[1]-1, splitDob[2]);
      }
      $scope.initialUser = response.data;
      $scope.user = angular.copy($scope.initialUser);
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  function getWishlist() {
    $http({ url: getWishlistUri }).then(function success(response) {
      $scope.wishlist = response.data;
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.toggleEditUser = function() {
    var userFields = ['name', 'email', 'dob'];
    var relevantEls;
    var i;
    $scope.user = angular.copy($scope.initialUser);
    userFields.forEach(function(fieldName) {
      relevantEls = document.querySelectorAll('div[id*='+fieldName+'-]');
      relevantEls.forEach(function(el) {
        el.classList.toggle('hidden');
      });
    });
    var editBtns = document.getElementsByClassName('edit-user-btn');
    for(i = 0; i < editBtns.length; i++) {
      editBtns[i].classList.toggle('hidden');
    }
  };

  $scope.removeFromWishlist = function(var_id) {
    data = { 'id': var_id };
    $http({
      method: 'POST',
      url: removeFromWishlistUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      alert(response.data);
      getWishlist();
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.editAddress = function(addr, index) {
    var originalAddr = $scope.addressesService.initialAddresses[index];
    var addrData = {};
    for(p in addr) {
      if(addr[p] !== originalAddr[p] || p == '_id') addrData[p] = addr[p];
    }
    console.log(addrData);
    if(Object.keys(addrData).length > 1) {
      sendPost(editAddressUri, addrData, function(response) {
        $scope.addressesService.update(getAddressesUri);
        alert(response.data);
      });
    } else {
      alert('Você não fez nenhuma alteração no endereço');
    }
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
      alert(response.data);
    }, errorCallback || function errorCallback(response) {
      alert(response.data);
    });
  };

  $scope.editUser = function() {
    var userFields = [ 'name', 'email', 'dob' ];
    var user = {};
    userFields.forEach(function(field) {
      if ($scope.user[field] != $scope.initialUser[field]) user[field] = $scope.user[field];
      if (field === 'dob') user[field] = $scope.parseDate(user[field]);
    });
    sendPost(editUserUri, user, function(response) {
      alert(response.data);
      getUser();
      $scope.toggleEditUser();
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

