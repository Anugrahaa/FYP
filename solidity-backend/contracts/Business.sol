import "./Invoice.sol";
import "./Utility.sol";
import "./Cashledger.sol";
import "./Creditledger.sol";
import "./Liabilityledger.sol";

contract Business{

	bytes16 name;
	bytes16 GSTIN;
	bytes16 statecode;

	//mapping(bytes16 => entity) businesslist;
	//bytes16[] public GSTIN;
	struct Tax{
		uint integratedtax;
		uint centraltax;
		uint statetax;
	}

	Tax public itc;
	Tax public liability;
	Tax public cash;

	Invoice[] public salesbills;
	Invoice[] public purchasebills;
	
	Creditledger credit;
	Liabilityledger liability_l;
	Cashledger cash_l;
	
	Utility u;

	function Business(bytes16 _name, bytes16 _GSTIN, bytes16 _statecode) public {
		name = _name;
		GSTIN = _GSTIN;
		statecode = _statecode;
		u.businessAdd(_name,_GSTIN,_statecode);
	}

	function addInvoice(bytes16 _billtype, uint _daysafter, bytes16 _gstin) public returns (uint){
		if(_billtype == "sales"){
			Invoice _bill = new Invoice();
			uint id = salesbills.length;
			//enter the number of days issue date differs from due date
			_bill.setDueDate(_daysafter);
			_bill.billed(GSTIN,_gstin);
		    salesbills.push(_bill) -1;
		    return id;
		}
		else{
			Invoice _bill_ = new Invoice();
			uint _id = purchasebills.length;
			_bill_.setDueDate(_daysafter);		    
		    _bill_.billed(GSTIN,_gstin);
		    purchasebills.push(_bill_) -1;
		    return _id;
		}
	}

	function salesAddProd(uint _id,bytes16 _prname, bytes16 _hsn, bytes16 _prcategory, uint _rate, uint _quantity,uint _igst, uint _cgst, uint _sgst) public{
		salesbills[_id].addProduct(_prname,_hsn,_prcategory,_rate,_quantity,_igst,_cgst,_sgst);
		s_updateTotals(_id);
	}

	function purchaseAddProd(uint _id,bytes16 _prname, bytes16 _hsn, bytes16 _prcategory, uint _rate, uint _quantity,uint _igst, uint _cgst, uint _sgst)public{
		purchasebills[_id].addProduct(_prname,_hsn,_prcategory,_rate,_quantity,_igst,_cgst,_sgst);
		p_updateTotals(_id);
	}

	function s_updateTotals(uint _id) public{
		salesbills[_id].getInvoiceTotal();
		salesbills[_id].updateGSTTotals();
	}

	function p_updateTotals(uint _id) public{
		purchasebills[_id].getInvoiceTotal();
		purchasebills[_id].updateGSTTotals();
	}

	function updateCreditLedger(bytes16 _desp) public{
		for(uint i=1;i<=purchasebills.length;i++){
			itc.integratedtax += purchasebills[i].getIGSTTotal();
			itc.centraltax += purchasebills[i].getCGSTTotal();
			itc.statetax += purchasebills[i].getSGSTTotal();
		}
		credit.addTransaction("credit",_desp,itc.integratedtax,itc.centraltax,itc.statetax);
		credit.updatebalance();

	}

	function updateLiabilityLedger(bytes16 _desp) public{
		for(uint i=1;i<=salesbills.length;i++){
			liability.integratedtax += salesbills[i].getIGSTTotal();
			liability.centraltax += salesbills[i].getCGSTTotal();
			liability.statetax += salesbills[i].getSGSTTotal();
		}
		liability_l.addTransaction("debit",_desp,"-",liability.integratedtax,liability.centraltax,liability.statetax);
		liability_l.updatebalance();
	}

	function updateCashLedger(bytes16 _transtype, bytes16 _desp, uint _i, uint _c,uint _s) public {
		cash_l.addTransaction(_transtype,_desp,_i,_c,_s);
		cash_l.updatebalance();
	}


	// taxtotal for all purchasebills is ITC (+)
	// taxtotal for all salesbills is Liability (-)
	// leftover to make everything zero, stuff loaded into cash ledger

	function getBusiness(bytes16 GSTIN) public constant returns (bytes16,bytes16,bytes16,Invoice[], Invoice[]){
		return (name,GSTIN,statecode, salesbills, purchasebills);
	}
}
