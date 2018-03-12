pragma solidity ^0.4.18



Contract Transaction{
	struct business{
		bytes16 name;
		uint category;
	}

	mapping(bytes16 => business) businesses;
	bytes16[] public GSTIN;

	struct product{
		bytes16 hsn;
		bytes16 name;
		uint rate;
	}
	mapping(bytes16 => product) products;
	bytes16[] public productid;

	struct transaction{
		business from;
		business to; 
		product p;
		uint quantity;
	}
	mapping(uint => transaction) transactions;
	uint[] public transid;

	function setBusiness(bytes16 _GSTIN, bytes16 _name, uint _category){
		
	}

}