from product import * 
import os.path

def create_invoice():
	write_product()
	return '''import "./Product.sol";
import "./Utility.sol";

contract Invoice{

	//input Invoice_no
	bytes16 Invoice_no;

	uint public date = now;

	bytes16 public billed_by_GSTIN;
	bytes16 public bill_to_GSTIN;

	uint due_date;
	uint total;
	uint taxtotal;
	uint igst_total;
	uint cgst_total;
	uint sgst_total;
	uint invoice_total;

	struct productdetails{
		Product pr;
		uint quantity;
		uint amount;
		uint IGST;
		uint CGST;
		uint SGST;
	}

	mapping(uint => productdetails) productlist;
	uint[] public productids;

    Utility u = new Utility();
	//no of products(?)
	// p is input for product details; 0 - name, 1- hsn, 2- category,3 -rate, 4 - quantity
 	function addProduct(bytes16 _name,bytes16 _hsn, bytes16 _category, uint _rate, uint _quantity, uint _igst, uint _cgst, uint _sgst) public {
 		uint prId = productids.length++;
	    var _product = productlist[prId]; 		
	    Product prod = new Product(_name,_hsn,_category,_rate,_igst,_cgst,_sgst);
	    _product.pr = prod;
	    _product.quantity = _quantity;
	    _product.amount = getAmount(prId);
	    productids.push(prId) -1;
	    // getTaxAmount();
	    // getInvoiceTotal();
 	}

 	function billed(bytes16 _gstin, bytes16 _gstin_){
 		billed_by_GSTIN = _gstin;
 		bill_to_GSTIN = _gstin_;
 	}

 	function getProduct(uint _prId) public {
 		productlist[_prId].pr.getProduct();
 	}

 	function getProducts() public constant returns (uint[]){
 		return productids;
 	}

	function setQuantity(uint _productid, uint _quantity) public {
		productlist[_productid].quantity = _quantity;
		// getTaxAmount();
		// getInvoiceTotal();
	}

	function getQuantity(uint _productid) public constant returns (uint){
		return productlist[_productid].quantity;
	}

	function getAmount(uint _prId) returns (uint){
		productlist[_prId].amount= productlist[_prId].pr.rate() * productlist[_prId].quantity;
			
		return productlist[_prId].amount;
	}

	function getTaxAmount(uint _prId) returns (uint){
		uint taxAmount =0;
		if(u.findState(billed_by_GSTIN) == u.findState(bill_to_GSTIN)){
				productlist[_prId].CGST = (productlist[_prId].amount * productlist[_prId].pr.cgst())/100;
				productlist[_prId].SGST = (productlist[_prId].amount * productlist[_prId].pr.sgst())/100;
				productlist[_prId].IGST = 0;	
			}
			else{
				productlist[_prId].CGST = 0;
				productlist[_prId].SGST = 0;
				productlist[_prId].IGST = (productlist[_prId].amount * productlist[_prId].pr.igst())/100;
			}
		taxAmount = productlist[_prId].IGST+ productlist[_prId].CGST + productlist[_prId].SGST;
		return taxAmount;
	}

	function getIGSTamount(uint _prId) returns (uint){
		if(u.findState(billed_by_GSTIN) == u.findState(bill_to_GSTIN)){
			return 0;
		}
		else{
			productlist[_prId].IGST = (productlist[_prId].amount * productlist[_prId].pr.igst())/100;
			return productlist[_prId].IGST;
		}
	}

	function getCGSTamount(uint _prId) returns (uint){
		if(u.findState(billed_by_GSTIN) == u.findState(bill_to_GSTIN)){
			productlist[_prId].CGST = (productlist[_prId].amount * productlist[_prId].pr.cgst())/100;
			return productlist[_prId].CGST;
		}
		else{
			return 0;
		}
	}

	function getSGSTamount(uint _prId) returns (uint){
		if(u.findState(billed_by_GSTIN) == u.findState(bill_to_GSTIN)){
			productlist[_prId].SGST = (productlist[_prId].amount * productlist[_prId].pr.cgst())/100;
			return productlist[_prId].SGST;
		}
		else{
			return 0;
		}
	}

 	function setDueDate(uint daysafter) public {
 		due_date = now + daysafter * 1 days;
 	}

 	function getIGSTTotal() public constant returns (uint){
 		for(uint i=1;i<=productids.length;i++){
 			igst_total += getIGSTamount(productids[i]);
 		}
 		return igst_total;
 	}

 	function getCGSTTotal() public constant returns (uint){
 		for(uint i=1;i<=productids.length;i++){
 			cgst_total += getCGSTamount(productids[i]);
 		}
 		return cgst_total;
 	}

 	function getSGSTTotal() public constant returns (uint){
 		for(uint i=1;i<=productids.length;i++){
 			sgst_total += getSGSTamount(productids[i]);
 		}
 		return sgst_total;
 	}

 	function getTaxTotal() public constant returns (uint){
 		for(uint i=1;i<=productids.length;i++){
 			taxtotal += getTaxAmount(productids[i]);
 		}
 		return taxtotal;
 	}

 	function getInvoiceTotal() public constant returns (uint){
 		for(uint i=1;i<=productids.length;i++){
 			total += getAmount(productids[i]);
 			taxtotal += getTaxAmount(productids[i]);
 		}
 		invoice_total = total + taxtotal; 
 		return invoice_total;
 	}

}
'''


def write_product():
	output = './Helpers/product.sol'
	if os.path.isfile(output):
		return
	outputfile = open(output, "w+")
	outputfile.write(create_product())
	outputfile.close()