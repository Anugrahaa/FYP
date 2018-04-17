def create_transaction():
	return '''pragma solidity ^0.4.4;

contract Transaction{
	uint date;
	address ref;
	//type may be debit or credit
	bytes16 public transtype;
	bytes16 description;

	struct integrated{
		uint i_tax;
		uint i_interest;
		uint i_penalty;
		uint i_fee;
		uint i_others;
		uint i_total;
	}

	struct central{
		uint c_tax;
		uint c_interest;
		uint c_penalty;
		uint c_fee;
		uint c_others;
		uint c_total;
	}

	struct state{
		uint s_tax;
		uint s_interest;
		uint s_penalty;
		uint s_fee;
		uint s_others;
		uint s_total;
	}

    integrated public i;
	central public c;
	state public s;
	
	function fillintegrated(uint[] _i) public {
		i.i_tax = _i[0];
		i.i_interest = _i[1];
		i.i_penalty = _i[2];
		i.i_fee = _i[3];
		i.i_others = _i[4];
	}

	function fillcentral(uint[] _c) public {
		c.c_tax = _c[0];
		c.c_interest = _c[1];
		c.c_penalty = _c[2];
		c.c_fee = _c[3];
		c.c_others = _c[4];
	}

	function fillstate(uint[] _s) public{
		s.s_tax = _s[0];
		s.s_interest = _s[1];
		s.s_penalty = _s[2];
		s.s_fee = _s[3];
		s.s_others = _s[4];
	}

	function total() public{
		i.i_total = i.i_others + i.i_fee + i.i_penalty + i.i_interest + i.i_tax;
		c.c_total = c.c_others + c.c_fee + c.c_penalty + c.c_interest + c.c_tax;
		s.s_total = s.s_others + s.s_fee + s.s_penalty + s.s_interest + s.s_tax;
	}

    function getItotal() returns (uint){
    	return i.i_total;
    }

    function getCtotal() returns (uint){
    	return c.c_total;
    }

    function getStotal() returns (uint){
    	return s.s_total;
    }

	function Transaction(uint _date,address _ref,bytes16 _transtype, bytes16 _desp,uint _i, uint _c,uint _s) {
		i.i_tax = _i;
		i.i_interest = 0;
		i.i_penalty = 0;
		i.i_fee = 0;
		i.i_others = 0;
		c.c_tax = _c;
		c.c_interest = 0;
		c.c_penalty = 0;
		c.c_fee = 0;
		c.c_others = 0;
		s.s_tax = _s;
		s.s_interest = 0;
		s.s_penalty = 0;
		s.s_fee = 0;
		s.s_others = 0;
		date = _date;
		ref = _ref;
		transtype = _transtype;
		description =_desp;
	}

}'''