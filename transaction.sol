pragma solidity ^0.4.18;

contract Transactions{
    
	struct Business{
		bytes16 name;
		uint category;
	}

	mapping(bytes16 => Business) businesses;
	bytes16[] public GSTIN;

	struct Product{
		bytes16 hsn;
		bytes16 name;
		uint rate;
	}
	mapping(bytes16 => Product) products;
	bytes16[] public productid;

	struct Transaction{
		bytes16 from;
		bytes16 to; 
		bytes16 p;
		uint quantity;
	}
	mapping(uint => Transaction) transactions;
	uint nexttransid;

	function Transactions() public{
       nexttransid = 0;
   }

	function setBusiness(bytes16 _GSTIN, bytes16 _name, uint _category){
		var business = businesses[_GSTIN];

		business.name = _name;
		business.category = _category;

		GSTIN.push(_GSTIN) -1;
	}

	function setProduct(bytes16 _productid, bytes16 _hsn, bytes16 _name, uint _rate){
		var product = products[_productid];
		product.hsn = _hsn;
		product.name = _name;
		product.rate = _rate;

		productid.push(_productid) -1;
	}	

	function setTransaction(bytes16 from_GSTIN, bytes16 to_GSTIN, bytes16 _productid, uint _quantity) returns (uint id){
		var transaction = transactions[nexttransid];
		transaction.from = from_GSTIN;
		transaction.to = to_GSTIN;
		transaction.p = _productid;
		transaction.quantity = _quantity;

		id = nexttransid;
		nexttransid++;

		return id;
	}

	function getBusinesses() public view returns (bytes16[]){
		return GSTIN;
	}

	function getProducts() public view returns (bytes16[]) {
		return productid;
	}

	function getBusiness(bytes16 gstin) public view returns(bytes16, uint, bytes16){
		return (businesses[gstin].name, businesses[gstin].category, gstin);
	}

	function getProduct(bytes16 prodid) public view returns(bytes16, bytes16, uint, bytes16){
		return (products[prodid].hsn, products[prodid].name, products[prodid].rate, prodid);
	}

	function getTransactions() public view returns(uint){
		return nexttransid;
	}

	function getTransaction(uint transactionid) public view returns (bytes16, bytes16, bytes16, uint, uint){
		return (transactions[transactionid].from, transactions[transactionid].to, transactions[transactionid].p, transactions[transactionid].quantity, transactionid);
	}

}