pragma solidity ^0.4.4;

import "./Product.sol";
import "./Business.sol";

contract Utility{

	// all utility fns find information about Business/product
	// added in other transactions, i.e, already present on the 
	// blockchain. It's for quick global lookup from the blockchain.
	// Here, the utility fns can be used only after said Business/product
	// have been added. Ex: Utility.findGSTIN("HCL") can only be used 
	// only after HCL has been registered on the blockchain.

	//as opposed to given any Business/Product name, their
	//GSTIN/HSN is automatically found from a pre set list.
	// mappings required for business:
	// (name=>GSTIN), (GSTIN=>name) , (GSTIN=>statecode)
	// mappings required for product:
	// (name=>HSN) , (HSN=>name) , (HSN=>rate) 

    struct business{
        bytes16 name;
        bytes16 GSTIN;
        bytes16 statecode;
    }

    struct product{
        bytes16 name;
    	bytes16 hsn;
        uint rate;
        uint cgst;
		uint sgst;
		uint igst;
    }

	mapping(bytes16 => business) public businesslist;

	//list of all GSTINs registered 
	bytes16[] public GSTIN;

	mapping(bytes16 => product) public productlist;

	//mapping(name=>GSTIN)
	mapping(bytes16 => bytes16) public GSTINlist;

	//mapping(name=>hsn)
	mapping(bytes16 => bytes16) public HSNlist;
	
	business b;
	product p;

	function businessAdd(bytes16 _name, bytes16 _GSTIN, bytes16 _statecode) external{
		//uint id = GSTIN.length;
		//GSTIN.push(_GSTIN) -1;
		b.name = _name;
		b.GSTIN = _GSTIN;
		b.statecode = _statecode;
		businesslist[_GSTIN] = b;
		GSTINlist[_name] = _GSTIN;
	}

	function findGSTIN(bytes16 _name) public constant returns (bytes16){

		return GSTINlist[_name];
	}

	function findBusiness(bytes16 _GSTIN) public constant returns (bytes16){

		return businesslist[_GSTIN].name; 
	}

	function findState(bytes16 _GSTIN) public constant returns (bytes16){

		return businesslist[_GSTIN].statecode;
	}

	function productAdd(bytes16 _name, bytes16 _hsn, uint _rate, uint _igst, uint _cgst,uint _sgst) external {
		p.name = _name;
		p.hsn = _hsn;
		p.rate=_rate;
		p.igst = _igst;
		p.cgst = _cgst;
		p.sgst = _sgst;
		productlist[_hsn] = p;
	}

	function findHSN(bytes16 _name) public constant returns (bytes16){
		return HSNlist[_name];
	}

	function findProduct(bytes16 _hsn) public constant returns (bytes16){
		return productlist[_hsn].name;
	}

	function findRate(bytes16 _hsn) public constant returns(uint){
		return productlist[_hsn].rate;
	}

	function getIgstRate(bytes16 _hsn) public constant returns (uint){
		return productlist[_hsn].igst;
	}

	function getCgstRate(bytes16 _hsn) public constant returns (uint){
		return productlist[_hsn].igst;
	}

	function getSgstRate(bytes16 _hsn) public constant returns (uint){
		return productlist[_hsn].igst;
	}

	//gst[0] - igst, gst[1] - cgst, gst[2] - sgst
	function updateGstRates(bytes16 _hsn, uint[] GST) public{
		productlist[_hsn].igst = GST[0];
		productlist[_hsn].cgst = GST[1];
		productlist[_hsn].sgst = GST[2];
	}

}