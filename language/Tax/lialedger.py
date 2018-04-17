from transaction import *
from invoice import *
import os.path

def create_lialedger():
	write_txn()
	write_invoice()

	return '''pragma solidity ^0.4.4;
import "./Transaction.sol";

contract Liabilityledger{

	bytes16 GSTIN;

	struct LiabilityTrans{
		Transaction trans;
		bytes16 ledgerused;
	}
	
	LiabilityTrans[] transactions;

	uint i_balance = 0;
	uint c_balance = 0;
	uint s_balance = 0;
	uint totalbal = 0;

	function addTransaction(bytes16 _ledgerused, bytes16 _transtype, bytes16 _desp, uint _i, uint _c,uint _s) public{
		uint id = transactions.length++;
		var ltrans = transactions[id];
		Transaction t = new Transaction(now,this,_desp,_transtype,_i,_c,_s);
		ltrans.trans = t;
		ltrans.trans.total();
		ltrans.ledgerused = _ledgerused;
		transactions.push(ltrans) -1;
	}

	function updatebalance() public returns (uint){
		for(uint i=0;i<transactions.length;i++){
			if(transactions[i].trans.transtype() == "credit"){
				totalbal+= transactions[i].trans.getItotal() + transactions[i].trans.getCtotal() + transactions[i].trans.getStotal();
			} 
			else{
				totalbal-= transactions[i].trans.getItotal() + transactions[i].trans.getCtotal() + transactions[i].trans.getStotal();
			}
		}
		return totalbal;
	} 
	

}'''


def write_txn():
	output = './Helpers/transaction.sol'
	if os.path.isfile(output):
		return
	outputfile = open(output)
	outputfile.write(create_transaction)
	outputfile.close()


def write_invoice():
	output = './Helpers/invoice.sol'
	if os.path.isfile(output):
		return
	outputfile = open(output)
	outputfile.write(create_transaction)
	outputfile.close()