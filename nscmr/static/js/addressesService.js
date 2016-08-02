angular.module('angularApp')
.service('addressesService', ["$http", function($http) {
  var self = this;
  this.initialAddresses = [];
  this.addresses = [];

  this.update = function(getAddressesUri) {
    $http({
      url: getAddressesUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      self.initialAddresses = response.data;
      self.addresses = angular.copy(self.initialAddresses);
    }, function errorCallback(response) {
      console.log(response);
    });
  };
  this.reset = function() {
    self.addresses = angular.copy(self.initialAddresses);
  };

  this.deleteAddress = function(addressId) {
    var data = { 'address_id': addressId };
    $http({
      method: 'POST',
      url: removeAddressUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      self.update(getAddressesUri);
      alert(response.data);
    }, function errorCallback(response) {
      alert(response.data);
    });
  };

}]);
