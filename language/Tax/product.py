from utility import *
import os.path

def create_product():
	write_utility()
	return '''pragma solidity ^0.4.4;

import "./Utility.sol";

contract Product{
	bytes16 public name;
	bytes16 public hsn;
	bytes16 public category;
	uint public rate;
	uint public cgst;
	uint public sgst;
	uint public igst;

	function Product(bytes16 _name, bytes16 _hsn, bytes16 _category, uint _rate, uint _igst, uint _cgst,uint _sgst) public{
		name = _name;
		hsn = _hsn;
		category = _category;
		rate = _rate;
		igst = _igst;
		cgst = _cgst;
		sgst = _sgst;
		Utility u = new Utility();
		u.productAdd(_name,_hsn,_rate,_igst,_cgst,_sgst);
	}

	function getProduct() public constant returns (bytes16,bytes16,bytes16,uint,uint,uint,uint){
		return (name,hsn,category,rate,igst,cgst,sgst);
	}

}
'''


def write_utility():
	output = './Helpers/utility.sol'
	if os.path.isfile(output):
		return
	outputfile = open(output)
	outputfile.write(create_transaction)
	outputfile.close()