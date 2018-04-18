pragma solidity ^0.4.4;
import "./Transaction.sol";

contract Creditledger{

	bytes16 GSTIN;
	
	Transaction[] trans;

	uint i_balance = 0;
	uint c_balance = 0;
	uint s_balance = 0;
	uint totalbal = 0;

	// function addTransaction(bytes16 _transtype, string _desp, uint[] _i, uint[] _c,uint[] _s) public{
	// 	Transaction t;
	// 	t.date = now;
	// 	t.ref = this;
	// 	t.transtype = _transtype;
	// 	t.description = _desp;
	// 	t.fillintegrated(_i); // filling entire arrays
	// 	t.fillcentral(_c);
	// 	t.fillstate(_s);
	// 	t.total();
	// }

	function addTransaction(bytes16 _transtype, bytes16 _desp, uint _i, uint _c,uint _s) public{
		Transaction t = new Transaction(now,this,_desp,_transtype,_i,_c,_s);
		t.total();
		trans.push(t) -1;
	}	

	function updatebalance() public returns (uint){
		for(uint i=0;i<trans.length;i++){
			if(trans[i].transtype() == "credit"){
				totalbal+= trans[i].getItotal() + trans[i].getCtotal() + trans[i].getStotal();
			} 
			else{
				totalbal-= trans[i].getItotal() + trans[i].getCtotal() + trans[i].getStotal();
			}
		}
		return totalbal;
	} 

}