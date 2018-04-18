from utility import * 
from product import * 
from invoice import * 
from transaction import * 
from lialedger import *
from cashledger import * 
from creditledger import * 
from business import * 

import os.path

def create_files(p):

	if not os.path.exists('./Helpers'):
		os.makedirs('./Helpers')

	output = './Helpers/'+p+'.sol'
	
	if os.path.isfile(output):
		return
	outputfile = open(output, "w+")

	if p=="utility":
		result = create_utility() 

	elif p == "product":
		result = create_product()

	elif p == "invoice":
		result = create_invoice()

	elif p == "business":
		result = create_business()

	elif p == "liability_ledger":
		result = create_lialedger()

	elif p == "cash_ledger":
		result = create_cashledger()

	elif p == "credit_ledger":
		result = create_creditledger()

	elif p == "transaction":
		result = create_transaction()

	elif p == "ledgers":
		write_ledgers()
		return

	else:
		return

	outputfile.write(result)
	outputfile.close()	


