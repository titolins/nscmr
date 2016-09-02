angular.module('angularApp')
.service('paymentService', function() {
  var self = this;
  self.availableCards = null;
  self.availablePaymentOptions = null;
  self.initialCard = {
    'brandInfo': null,
    'number': '',
    'holderName': '',
    'cvv': '',
    'expMonth': '',
    'expYear': '',
    'installments': null,
  };
  self.card = angular.copy(self.initialCard);
  self.save = function() {
    self.initialCard = angular.copy(self.card);
  };
  self.reset = function() {
    self.card = angular.copy(self.initialCard);
  };
});

