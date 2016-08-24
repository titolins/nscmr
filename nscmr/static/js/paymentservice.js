angular.module('angularApp')
.service('paymentService', function() {
  var self = this;
  self.availableCards = null;
  self.availablePaymentOptions = null;
  self.initialCard = {
    'brandInfo': {},
    'number': '',
    'holderName': '',
    'cvv': '',
    'expMonth': '',
    'expYear': ''
  };
  self.card = angular.copy(self.initialCard);
  self.save = function() {
    self.initialCard = angular.copy(self.card);
  };
  self.reset = function() {
    self.card = angular.copy(self.initialCard);
  };
});

