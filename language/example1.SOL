import "" // all the 8 things

Business a = new Business("ballarpur","07AAACB5343E1Z3","07");
Business b = new Business("murugappan","32AAACB5343E1ZA","32");
Business c = new Business("biocorp","23AAACB5343E1Z9","23");
Business d = new Business("Bheem","07AADCB2230M1ZV","07");

#params are : 
#0- billtype (sales invoice / purchase invoice)
#1- daysafter (due date) 
#2- gstin(of the buyer/biller)
#returns: invoice id

uint id = a.addInvoice("sales",15,"07AADCB2230M1ZV");

#params are:
0- product name
1- hsn of the product
2- product category
3- Price per unit (rate)
4- quantity of product
5- igst percentage on product
6- cgst percentage on product
7- sgst percentage on product

a.salesAddProd(id,"Soaps","34031100","Sanitary",30,400,18,9,9);
a.salesAddProd(id,"BeautyProduct","33051010","Cosmetics",100,40,18,9,9);
a.salesAddProd(id,"Jutebags","42022240","Utility",100,500,12,6,6);


uint _id = a.addInvoice("purchase",15,"23AAACB5343E1Z9");

a.purchaseAddProd(_id,"Printed Circuits","85340000","Electronics",800,20,18,9,9);
a.purchaseAddProd(_id,"Tooling machinery","85340000","Industrial machinery",2500,4,18,9,9);

a.updateCreditLedger("Fortnightly returns");

a.updateLiabilityLedger("Fortnightly liabilities");



