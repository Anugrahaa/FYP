import os

def prettify(filename):
	ipfile = open(filename)
	data = ipfile.read()
	opfile = open("temp_"+filename, "w+")


	i=0
	lineno=1
	indentation = []
	semicolons = 0
	linebreaks = 0
	indent = 0

	while True:

		try:

			if data[i] == ";":
				semicolons += 1
				if semicolons>1:
					pass
				else:
					opfile.write(";\n")
					linebreaks += 1

			elif data[i] == "\n":
				linebreaks += 1
				if linebreaks>1:
					if data[i-1]!=";":
						pass
					else:
						lineno+=1
						indentation.append(indent)
				else:
					lineno+=1
					indentation.append(indent)
					if data[i+1]==";":
						pass
					else:
						opfile.write("\n")
				if data[i+1]==";":
					opfile.write("")

			elif data[i] == "{":
				semicolons = 0
				linebreaks = 0
				indent += 1
				opfile.write("{")

			elif data[i] == "}":
				semicolons = 0
				linebreaks = 0
				indent -= 1
				opfile.write("}")

			else:
				semicolons = 0
				linebreaks = 0
				opfile.write(data[i])

			i+=1
		except IndexError:
			break

	ipfile.close()
	opfile.close()
	os.remove(filename)
	ipfile = open("temp_"+filename)
	data = ipfile.read()
	opfile = open(filename, "w+")

	print indentation
	print lineno
	i=0
	ln = 1
	while True:
		try:
			if data[i]==";" and data[i-1]=="\n" and data[i+1]=="\n":
				pass
			elif data[i]=='\n':
				ln += 1
				opfile.write("\n")
			elif data[i-1]=='\n' and i!=0:
				indent = 0
				while indent<indentation[ln-1]:
					opfile.write("\t")
					indent+=1
				opfile.write(data[i])
			else:
				opfile.write(data[i])
			if data[i] == ";" or data[i]=="\n":
				print str(i)+": "+data[i]+", i-1:"+data[i-1]
			i += 1
		except IndexError:
			break

	opfile.close()
	ipfile.close()
	os.remove("temp_"+filename)





