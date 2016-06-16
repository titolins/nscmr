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

}]);
