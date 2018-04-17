var Migrations = artifacts.require("./Migrations.sol");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
};

var Utility = artifacts.require("./Utility.sol");

module.exports = function(deployer) {
  deployer.deploy(Utility);
};

var Product = artifacts.require("./Product.sol");

module.exports = function(deployer) {
  deployer.deploy(Product);
};

var Invoice = artifacts.require("./Invoice.sol");

module.exports = function(deployer) {
  deployer.deploy(Invoice);
};

var Transaction = artifacts.require("./Transaction.sol");

module.exports = function(deployer) {
  deployer.deploy(Transaction);
};

var Cashledger = artifacts.require("./Cashledger.sol");

module.exports = function(deployer) {
  deployer.deploy(Cashledger);
};

var Creditledger = artifacts.require("./Creditledger.sol");

module.exports = function(deployer) {
  deployer.deploy(Creditledger);
};

var Liabilityledger = artifacts.require("./Liabilityledger.sol");

module.exports = function(deployer) {
  deployer.deploy(Liabilityledger);
};

var Business = artifacts.require("./Business.sol");

module.exports = function(deployer) {
  deployer.deploy(Business);
};

