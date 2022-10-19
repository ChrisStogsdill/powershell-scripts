from datetime import datetime 
import json
import os
import sys
import pathlib
import subprocess
import shutil
import re
import weasyprint
from time import sleep
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import ocrmypdf

parent_app_location = '/map/iq/IQHelper/'
#parent_app_location = '/map/iq/testenv_iqHelper/'

def ocr_the_pdf(filePath):
	path = pathlib.PurePath(filePath)
	base = path.name
	#result['StoreName'] = path.parts[3]
	#result['DocType'] = path.parts[4]
	parent = str(path.parent)
	renameFolder = parent_app_location + 'assets/rename/'
	renamedFile = str(renameFolder + path.stem + '_ocr'+ path.suffix)
	try:
		ocrmypdf.ocr(filePath, renamedFile,language="eng", force_ocr=False, skip_text=True, rotate_pages=True, progress_bar=False, deskew=True ,remove_background=False, rotate_pages_threshold=1.5)
		print("File was ocr'ed -", renamedFile)
		return renamedFile
	except:
		print("File failed to ocr -", filePath)
		return filePath

def printed_page_splitter(filePath, oldParent):
	path = pathlib.PurePath(filePath)
	base = path.name
	parent = str(path.parent)
	print('imported file parent:', parent)
	fileList = []
	argInput_1 = ["pdfgrep","-nio","<p\\s?h\\s?y\\s?p\\s?a\\s?g\\s?e\\s?s\\s?p\\s?l\\s?i\\s?t\\s?t\\s?e\\s?r\\s?>",str(filePath)]
	consoleOut_1 = subprocess.run(argInput_1, stdout=subprocess.PIPE)
	output_1 = consoleOut_1.stdout.decode('utf-8')
	foundPageSplitList = re.findall("(\\d{0,3}):", output_1)
	try:
		if (foundPageSplitList):
			argInput_2 = ["pdfgrep","-nio","<D\\s?O\\s?U\\s?B\\s?L\\s?E\\s?S\\s?I\\s?D\\s?E\\s?P\\s?A\\s?G\\s?E\\s?D\\s?E\\s?T\\s?E\\s?C\\s?T\\s?I\\s?O\\s?N>",str(filePath)]
			consoleOut_2 = subprocess.run(argInput_2, stdout=subprocess.PIPE)
			output_2 = consoleOut_2.stdout.decode('utf-8')
			foundDoubleSideDetection = re.findall("(\\d{0,3}):", output_2)
			lastset = 0
			if (foundDoubleSideDetection):
				firstpage = 0
				counter = 1
				for i in foundPageSplitList:
					with open (filePath, 'rb') as file:
						r = PdfFileReader(file, strict=False)
						w = PdfFileWriter()
						if firstpage - (int(i)-1) != 0:
							for x in range(firstpage, (int(i)-1)):
								w.addPage(r.getPage(x))
						else:
							w.addPage(r.getPage(firstpage))
						seperateFiles = oldParent + '/s'+ str(counter) +'_' + base
						counter += 1
						firstpage = int(i) + 1
						with open(seperateFiles, 'wb') as outfile:
							w.write(outfile)
							fileList.append(seperateFiles)
							print( 'new outfile', seperateFiles)

			else:
				firstpage = 0
				counter = 1
				for i in foundPageSplitList:
					with open (filePath, 'rb') as file:
						r = PdfFileReader(file, strict=False)
						w = PdfFileWriter()
						for x in range(firstpage, (int(i)-1)):
							w.addPage(r.getPage(x))
						seperateFiles = oldParent + '/s'+ str(counter) +'_' + base
						counter += 1
						firstpage = int(i)
						lastset = firstpage
						with open(seperateFiles, 'wb') as outfile:
							w.write(outfile)
							fileList.append(seperateFiles)
							print( 'new outfile', seperateFiles)

			with open (filePath, 'rb') as file:
				r = PdfFileReader(file, strict=False)
				w = PdfFileWriter()
				endpage = r.getNumPages()
				if firstpage - (endpage-1) != 0:
					for x in range(firstpage, (endpage-1)):
						w.addPage(r.getPage(x))
				else:
					w.addPage(r.getPage(firstpage))

				seperateFiles = oldParent + '/s'+ str(counter) +'_' + base
				with open(seperateFiles, 'wb') as outfile:
					w.write(outfile)
					fileList.append(seperateFiles)
					print( 'new outfile', seperateFiles)
				
			returnCode = 0
			print('returnCode :',str(returnCode))
			return returnCode
		else:
			returnCode = 1
			print('returnCode :',str(returnCode))
			print('No Split Found!')
			return returnCode
	except: 
		returnCode = 1
		print('returnCode :',str(returnCode))
		print('No Split Found!')
		return returnCode
	




def getConfig(filePath):
	#PASSED, MC, 2JUN2021
	with open(filePath, "r") as read_file:
		data = json.load(read_file)
		config = data
	return config


def getTime():
	#PASSED, MC, 28MAY2021
	now = datetime.now()
	currentTime = now.strftime("%Y%m%d_%H%M%s%f")
	#test
	return currentTime


def moveAndRename(filePath):
	#PASSED, MC, 28MAY2021
	#RECONFIGURE: MC, 01JUNE2021
	result={}
	path = pathlib.PurePath(filePath)
	#
	base = path.name
	result['StoreName'] = path.parts[3]
	result['DocType'] = path.parts[4]
	starting_doc = 'DOCUMENT FROM : '+ result['StoreName']+ ' DOC TYPE : '+result['DocType']+ ' path of : '+ str(path)
	parent = str(path.parent)
	oldParent = str(path.parent)
	os.chdir(parent)
	#
	renameFolder = parent_app_location + 'assets/rename/'
	time = getTime()
	newFile = str(renameFolder+result['StoreName']+'_'+time+path.suffix)
	shutil.move (str(path), newFile)
	#
	print('INFO -',starting_doc)
	return newFile, result, oldParent, starting_doc

def putFile(upFile, bucket):
	#https://dariancabot.com/2017/05/07/aws-s3-uploading-and-downloading-from-linux-command-line/
	#PASSED, MC, 28MAY2021
	path = pathlib.Path(upFile)
	base = path.name
	parent = str(path.parent)
	bucketFileName = bucket+'/'+base
	argInput = ["aws", "s3", "cp", upFile, bucketFileName]
	consoleOut=subprocess.run(argInput, stdout=subprocess.PIPE)
	print(consoleOut.stdout)
	return bucketFileName


def getAWSData(bucketFileName, bucket):
		import time
		print(bucketFileName, bucket)
		bucketFileName = bucketFileName.replace('s3://iqhelper/','')
		print(bucketFileName, bucket)
		bucketJSON= '{"S3Object":{"Bucket":'+'"'+bucket+'"'+',"Name":'+'"'+bucketFileName+'"'+'}}'
		featureJSON = '["FORMS"]'
		argInput_1 = ["aws", "textract", "start-document-analysis", "--feature-types", str(featureJSON), "--document-location", bucketJSON]
		consoleOut_1=subprocess.run(argInput_1, stdout=subprocess.PIPE)
		argOutput_1 = consoleOut_1.stdout
		argOutput_1 = argOutput_1.decode("utf-8")
		final=json.loads(argOutput_1)
		time.sleep(5)
		print(final)
		#
		jobstatus = ''
		#Added MC, 07-16-2021
		i = 1
		#End
		while jobstatus != 'SUCCEEDED':
			#Added MC, 07-16-2021
			if i > 48:
				print("Failed to get any AWS Data")
				emptydict = {}
				return emptydict
			#
			print("Attempt Count:", i)
			#End
			jsonFileName = parent_app_location + "assets/upload/"+ bucketFileName + ".json"
			argInput_2 = "bash /map/iq/IQHelper/assets/getAWSData.sh '"+final['JobId']+ "' '"+jsonFileName+ "'"
			print(argInput_2)
			os.system(argInput_2)
			time.sleep(5)
			i += 1
			#
			with open(jsonFileName, "r") as read_file:
				data = json.load(read_file)
				final2 = data
				jobstatus = final2['JobStatus']
			time.sleep(5)
		return final2

def splitPages(filePath):
	#PASSED, MC, 28MAY2021
	path = pathlib.PurePath(filePath)
	base = path.name
	parent = str(path.parents[1])
	with open (filePath, 'rb') as file:
		r = PdfFileReader(file, strict=False)
		w = PdfFileWriter()
		w.addPage(r.getPage(0))
		firstPageName = parent + '/upload/0_' + base
		with open (firstPageName, 'wb') as outfile:
			w.write(outfile)
	return firstPageName

def addCoverPage(xFile, yFile, config, docCode):
	import time
	merge = PdfFileMerger(strict=False)
	xFilePath = pathlib.PurePath(xFile)
	merge.append(xFile, 'rb')
	merge.append(yFile, 'rb')
	newFile2 = config["FINAL DUMPS"][str(docCode)]["DUMP"] + str(xFilePath.name).replace('cover_', '')
	newFile = str(xFilePath.parents[1]) + '/output/final/' + str(xFilePath.name).replace('cover_', '')
	#
	merge.write(newFile)
	time.sleep(2)
	try:
		ocrmypdf.ocr(newFile, newFile2,language="eng", force_ocr=False, skip_text=True, rotate_pages=True, progress_bar=False,remove_background=False, rotate_pages_threshold=1.5)
		time.sleep(5)
		print(newFile2,'\n', newFile)	
	except:
		print(newFile2,'\n', newFile)
	return newFile

def createCoverPage(inputDict, allPagesFileName, kvs):
	inputDictCopy = dict(inputDict)
	filePath = pathlib.PurePath(allPagesFileName)
	filename = str(filePath.parents[1]) + "/output/cover_" + str(filePath.name)
	if inputDict['Document Type'] != 'INVOICE - EXPENSES':
		HTMLString = """<html><link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700;1,800&family=Roboto+Mono:wght@100;300&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,900&family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,600;1,700;1,900&display=swap" rel="stylesheet"><style>h2{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:30px}h6{font-family:'Source Sans Pro',sans-serif;font-weight:700}.Date{font-family:'Source Sans Pro',sans-serif;font-weight:700, font-size:12px}h3{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:20px}td{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:14px}footer, .other_header{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:12px}table{border-spacing:30px 10px}.data{font-family:'Source Sans Pro', sans-serif;font-weight:300}.other{font-family:'Source Code Pro',monospace;font-size: 8px}.other_data{font-family:'Source Code Pro',monospace;font-size: 8px}</style><body><h2>Midwest Hose DocVault</h2> <pre class="Date"> <i>COVER PAGE CREATED ON:&#9;&#9;""" + datetime.now().strftime("%Y/%m/%d at %H:%M:%s UTC") + """</i></pre><h3>"""+str(inputDictCopy['Document Type'])+""" SUMMARY<br>"""+str(inputDictCopy['LOCATION'])+"""<br>---</h3><table>"""

	else:
		HTMLString = """<html><link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700;1,800&family=Roboto+Mono:wght@100;300;500&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,900&family=Azeret+Mono:wght@300;500&family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,600;1,700;1,900&family=Anonymous+Pro:wght@400;700&family=Padauk:wght@400;700&family=Signika&family=Monda&family=Roboto:wght@300;400;500;700;900&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet"><style>h2{font-family:'Source Sans Pro',sans-serif; font-weight:700; font-size:30px}h6{font-family:'Source Sans Pro',sans-serif; font-weight:700}.Date{font-family:'Source Sans Pro',sans-serif; font-weight:700, font-size:12px}h3{font-family:'Source Sans Pro',sans-serif; font-weight:700; font-size:20px}td{font-family:'Source Sans Pro',sans-serif; font-weight:500; font-size:14px}footer, .other_header{font-family:'Source Sans Pro',sans-serif; font-weight:500; font-size:12px}table{border-spacing:30px 10px}.data{font-family:'Monda', sans-serif;font-weight:400; letter-spacing:0.1rem}.data2{font-family: 'Signika', sans-serif; font-weight:400; letter-spacing:0.1rem}.other{font-family:'Source Code Pro',monospace; font-size: 8px}.other_data{font-family:'Source Code Pro',monospace; font-size: 8px}</style><body><h2>Midwest Hose DocVault</h2><pre class="Date"><i>COVER PAGE CREATED ON:&#9;&#9;""" + datetime.now().strftime("%Y/%m/%d at %H:%M:%s UTC") + """</i></pre><h3>"""+str(inputDictCopy['Document Type'])+""" SUMMARY<br>"""+str(inputDictCopy['LOCATION'])+"""<br>---</h3><table>"""
		#HTMLString = """<html><link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700;1,800&family=Roboto+Mono:wght@100;300;500&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,900&family=Azeret+Mono:wght@300;500&family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,600;1,700;1,900&display=swap" rel="stylesheet"><style>h2{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:30px}h6{font-family:'Source Sans Pro',sans-serif;font-weight:700}.Date{font-family:'Source Sans Pro',sans-serif;font-weight:700, font-size:12px}h3{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:20px}td{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:14px}footer, .other_header{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:12px}table{border-spacing:30px 10px}.data{font-family: 'Azeret Mono', monospace;font-weight:300}.other{font-family:'Source Code Pro',monospace;font-size: 8px}.other_data{font-family:'Source Code Pro',monospace;font-size: 8px}</style><body><h2>Midwest Hose DocVault</h2> <pre class="Date"> <i>COVER PAGE CREATED ON:&#9;&#9;""" + datetime.now().strftime("%Y/%m/%d at %H:%M:%s UTC") + """</i></pre><h3>"""+str(inputDictCopy['Document Type'])+""" SUMMARY<br>"""+str(inputDictCopy['LOCATION'])+"""<br>---</h3><table>"""
	#HTMLString = """<html><link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700;1,800&family=Roboto+Mono:wght@100;300&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,900&family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,600;1,700;1,900&display=swap" rel="stylesheet"><style>h2{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:30px}h6{font-family:'Source Sans Pro',sans-serif;font-weight:700}.Date{font-family:'Source Sans Pro',sans-serif;font-weight:700, font-size:12px}h3{font-family:'Source Sans Pro',sans-serif;font-weight:700;font-size:20px}td{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:14px}footer, .other_header{font-family:'Source Sans Pro',sans-serif;font-weight:500;font-size:12px}table{border-spacing:30px 10px}.data{font-family:'Open Sans', sans-serif;;font-weight:300}.other{font-family:'Source Code Pro',monospace;font-size: 8px}.other_data{font-family:'Source Code Pro',monospace;font-size: 8px}</style><body><h2>Midwest Hose DocVault</h2> <pre class="Date"> <i>COVER PAGE CREATED ON:&#9;&#9;""" + datetime.now().strftime("%Y/%m/%d at %H:%M:%s UTC") + """</i></pre><h3>"""+str(inputDictCopy['Document Type'])+""" SUMMARY<br>"""+str(inputDictCopy['LOCATION'])+"""<br>---</h3><table>"""
	inputDictCopy.pop('Document Type')
	inputDictCopy.pop('LOCATION')
	for a in inputDictCopy:
		HTMLString += """<tr><td>"""+ str(a) + """:</td><td class="data">"""+str(inputDictCopy[a])[:40]+"""</td></tr>"""
	
	HTMLString += """</table><br><p class="other_header">--- OTHER VALUES --- </p><table>"""
	for b in kvs:
		HTMLString +="""<tr><td class="other">"""+ str(b) +"""--</td><td class="other_data">"""+ str(kvs[b]) + """</td></tr>"""

	#HTMLString +="""</table><br><br><footer>MWH IT DEPARTMENT, MC 06/2021. FOR HELP REACH THE IT DEPARTMENT AT helpdesk@midwesthose.com</footer></body></html>"""
	#
	HTMLName = allPagesFileName + '.html'
	PDFName = filename 
	#
	with open(HTMLName, 'w') as f:
		f.write(HTMLString)
	#
	pdf = weasyprint.HTML(HTMLName).write_pdf()
	len(pdf)
	open(filename, 'wb').write(pdf)
	return PDFName

def getText(input):
	#GEt RAW TEXT
	plainText = ""
	for x in input["Blocks"]:
		y = x
		if "Text" in y:
				plainText += (y["Text"]) + '\n'
	
	#GET KEYS AND VALUES
	blocks=input['Blocks']
	#1
	#1
	# get key and value maps
	key_map = {}
	value_map = {}
	block_map = {}
	for block in blocks:
		block_id = block['Id']
		block_map[block_id] = block
		if block['BlockType'] == "KEY_VALUE_SET":
			if 'KEY' in block['EntityTypes']:
				key_map[block_id] = block
			else:
				value_map[block_id] = block
		#
	return key_map, value_map, block_map, plainText

def get_kv_relationship(key_map, value_map, block_map):
	kvs = {}
	for block_id, key_block in key_map.items():
		value_block = find_value_block(key_block, value_map)
		key = get_text(key_block, block_map)
		val = get_text(value_block, block_map)
		kvs[key] = val
	return kvs

def find_value_block(key_block, value_map):
	for relationship in key_block['Relationships']:
		if relationship['Type'] == 'VALUE':
			for value_id in relationship['Ids']:
				value_block = value_map[value_id]
	return value_block

def get_text(result, blocks_map):
	text = ''
	if 'Relationships' in result:
		for relationship in result['Relationships']:
			if relationship['Type'] == 'CHILD':
				for child_id in relationship['Ids']:
					word = blocks_map[child_id]
					if word['BlockType'] == 'WORD':
						text += word['Text'] + ' '
					if word['BlockType'] == 'SELECTION_ELEMENT':
						if word['SelectionStatus'] == 'SELECTED':
							text += 'X '
	return text

def cleanJSON(jsonInput):
	cleanedJSON= {}
	for a in jsonInput:
		if a == '':
			cleanedJSON['EmptyKey'+str(i)]='EmptyValue'+str(i)
		else:
			cleanedJSON[a] = jsonInput[a]
	return cleanedJSON

def searchReturn(configJSON=None, keyValueSet=None, plainText=None, StoreName=None, DocType=None):
		#Establish Return Dict
		#DocType is doctype folder
		#WARNING : DEBUG
		#import pdb; pdb.set_trace()
		result = {}
		# Get Store Name 
		result['LOCATION'] = configJSON['STORES'][StoreName]['Name']
		# Get Type of Document Processed 
		result['Document Type'] = configJSON['DOC_TYPE_TO_NICENAME'][DocType]
		#Set DocType Code as outlind in the json
		doctypeCode = configJSON['FOLDER_TO_DOC_TYPE'][DocType]
		
		#Try Block 
		foundKeyword = ''
		# Get and Iterate through list of KEYWORDS for DocTypeCode
		for a in configJSON[doctypeCode]['KEYWORDS']:
			# Create String for RegEx 
			a_regex =  '(?i)' + a
			findKeyword = re.findall(a_regex, plainText)
			#DEBUG
			#print('foundKeyword (only taking the first match):',findKeyword, '\non regex pattern: "'+a+'"')
			# Search for regex until first match
			if findKeyword != []:
				foundKeyword = a
				#DEBUG
				result ['VENDOR OR KEYWORD'] = findKeyword[0]
				
				break
		#DEBUG
		print(foundKeyword)
		if foundKeyword in configJSON[doctypeCode].keys():
			searchDict = configJSON[doctypeCode][foundKeyword]
			print("foundKeyword", a, "and BREAKING!")

			#Get Nice Name if not empty
			nice = ''
			if str(searchDict['INFO']['NICE_NAME']) != "":
				nice = str(searchDict['INFO']['NICE_NAME'])

			#get list of required fields
			searchDict.pop('INFO')
			printedFields = []
			for printkeys in configJSON['PRINTEDFIELDS'][doctypeCode].keys():
				printedFields.append(str(printkeys))

			if printedFields != []:
				for b in printedFields:
					#DEBUG
					print(b)
					if str(configJSON['PRINTEDFIELDS'][doctypeCode][b]) == 'PO NUMBER':
						result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = '999999'
					else:
						result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = '--'
					try:
						if b in searchDict.keys():
							for c in searchDict[b].keys():
								#DEBUG
								#print(c)
								print('b:',b,'matched')
								if str(c) == 'KEY':
									for key_regex in searchDict[b][c]:
										findItem = '(?i)' + str(key_regex)
										print('regex 367', findItem)
										#print('kvs:', keyValueSet.keys())
										for k in keyValueSet.keys():
											findKey = re.findall(findItem, k)
											if findKey != []:
												print('findkey line 379',findKey)
												if b == 'PO_SEARCH':
													findPOPattern = re.findall(configJSON['GENERIC_PO'], keyValueSet[k])
													print('findPOPattern:',findPOPattern)
													if findPOPattern != []:
														result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(findPOPattern[0])
													else:
														print("Does not match!!")
												elif b == 'TOTAL_SEARCH':
													findMoneyPattern = re.findall(configJSON['MONEY_PATTERN'], keyValueSet[k])
													print('findMoneyPattern:',findMoneyPattern)
													if findMoneyPattern != []:
														result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(findMoneyPattern[0])
												else:
													result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(keyValueSet[k])
												print('b is:', b)
												print("result is:", result)


								if str(c) == 'TXT':
									for key_regex in searchDict[b][c]:
										findItem = '(?i)' + str(key_regex)
										print('regex 367', findItem)
										findKey = re.findall(findItem, plainText)
										if findKey != []:
											print('findkey line 384',findKey)
											result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(findKey[0])

								if str(c) == 'TXTG':
									for key_regex in searchDict[b][c]:
										findItem = '(?is)' + str(key_regex)
										print('regex 406', findItem)
										#print('plainText\n---\n', plainText, '\n---\n')
										findKey = re.search(findItem, plainText)
										if findKey != None:
											group_no = searchDict[b]['GROUP_NO']
											print('findkey line 411',findKey.group(group_no))
											result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(findKey.group(group_no))

								if str(c) == 'ERPCODE1':
											result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(configJSON['STORES'][StoreName]['ERP_Name'])

								if str(c) == 'INVTYPE':
											result[configJSON['PRINTEDFIELDS'][doctypeCode][b]] = str(searchDict[b][c])

							if b == 'PO_SEARCH':
								if result['PO NUMBER'] == '999999':
									print('Triggered Generic PO Search')
									dx = '(?i)' + configJSON['GENERIC_PO']
									findGenericPO = re.findall(dx, plainText)
									print(findGenericPO)
									if findGenericPO != None:
										result['PO NUMBER'] = str(findGenericPO[0])
					except:
						print('Failed Search -- Moving On')

			#Check if document is INVEXP
			if doctypeCode == 'INVEXP':
				result['ERP Location Code']=configJSON['STORES'][StoreName]['ERP_Name']
				result['Invoice Type']=configJSON['DOC_TYPE_TO_INVEXP_TYPE'][DocType]
			
			if nice != '':
				result['VENDOR OR KEYWORD'] = nice

			#Check if 'Invoice-Expense'
			#Find 'PO Regardless' Clause

		else:
			print("Keyword was not found in Keys -- Likely Entry Detail was not added")

		return result, doctypeCode

def searchKeys(configJSON=None, keyValueSet=None, plainText=None, StoreName=None, DocType=None):
	#import pdb; pdb.set_trace()
	result={}
	result['LOCATION'] = configJSON['STORES'][StoreName]['Name']
	result['Document Type'] = configJSON['DOC_TYPE_TO_NICENAME'][DocType]
	doctypeCode = configJSON['FOLDER_TO_DOC_TYPE'][DocType]
	try:
		for a in configJSON[doctypeCode]:
			#print("a:",a.keys())
			ax = '(?i)' + a['VENDOR_KEYWORD_SEARCH']
			findKeyword = re.findall(ax, plainText)
			#print("DEBUG ---- \n----\nfound match for pattern:", str(a['VENDOR_KEYWORD_SEARCH']), "match:", str(findKeyword),"\nEND DEBUG\n-----")
			for foundKeyword in findKeyword:
				#print(foundKeyword)
				if findKeyword != []:
					result['VENDOR OR KEYWORD'] = foundKeyword
					for configPrintedFields in configJSON['PRINTEDFIELDS'][doctypeCode]:
						for currentKeys in a.keys():
							#print(currentKeys)
							#result[currentKeys] = None
							#FOR DEBUG: 
							#print('keys & fields', currentKeys, "=", configPrintedFields)
							if currentKeys == configPrintedFields:
								for regex_values in a[currentKeys]:
									cx = '(?i)' + regex_values
									for k in keyValueSet:
										find_field = re.findall(cx, k)
										for g in find_field:
											print("configPrintedFields:", configPrintedFields)
											if configPrintedFields == 'PO_SEARCH':
												findPOPattern = re.findall(configJSON[GENERIC_PO], keyValueSet[g])
												if findPOPattern != []:
													result[configJSON['PRINTEDFIELDS'][str(doctypeCode)][str(configPrintedFields)]] = keyValueSet[g]
												print("PO Check debug:", findPOPattern[0])
											else:
												result[configJSON['PRINTEDFIELDS'][str(doctypeCode)][str(configPrintedFields)]] = keyValueSet[g]			
											#print("field :", configPrintedFields , "value:" ,keyValueSet[g])
								break
							else:
								#print('New Loop', configJSON['PRINTEDFIELDS'][str(doctypeCode)][str(configPrintedFields)])
								if configJSON['PRINTEDFIELDS'][str(doctypeCode)][str(configPrintedFields)] == 'PO NUMBER':
									#try:
									if ('PO NUMBER' in result) == False:
										#print("Here")
										#PLACEHOLDER FOR PO PLAINTEXT FULL SEARCH
										dx = '(?im)' + configJSON['GENERIC_PO']
										findGenericPO = re.findall(dx, plainText)
										#print(findGenericPO)
										if findGenericPO != None:
											d = findGenericPO
											result['PO NUMBER'] = str(d[0])
											#break

									# except TypeError:
									# 	print("Here Inner")
									# 	print(result)
								else:
										result[configJSON['PRINTEDFIELDS'][str(doctypeCode)][str(configPrintedFields)]] = 'N/A'
					return result, doctypeCode
	except:
		#print(result)
		try:
			resulttry = str(result['PO NUMBER'])
			#print("result try", resulttry)
			if resulttry == "None":
				#print("Here")
				dx = '(?i)' + configJSON['GENERIC_PO']
				findGenericPO = re.findall(dx, plainText)
				#print(findGenericPO)
				if findGenericPO != None:
					for d in findGenericPO:
						result['PO NUMBER'] = str(d)
		except TypeError:
			print("Here")
			print(result)
			return result, doctypeCode

def deleteAWSUpload(fileKey, bucket):
		import time
		bucketFileName = fileKey.replace('s3://iqhelper/','')
		argInput_1 = "bash /map/iq/IQHelper/assets/deleteAWSObject.sh '"+str(bucket)+ "' '"+str(bucketFileName)+ "'"
		print(argInput_1)
		os.system(argInput_1)
		time.sleep(5)
		print(argInput_1, "...deleted from aws. done...")

def cleanFiles():
	import time
	now = time.time()
	paths=["/map/iq/IQHelper/assets/upload",  "/map/iq/IQHelper/assets/rename", "/map/iq/IQHelper/assets/output", "/map/iq/backups", "/map/iq/IQHelper/assets/output/final"]
	for a in paths:
		for b in os.listdir(a):
			rmvfile =  a + '/'+ b
			counter = 0
			if b.endswith(('.pdf', '.html', '.json', '.PDF', '.txt')):
				if os.stat(rmvfile).st_mtime < now - 4 * 86400:
					#print("removing... ", rmvfile, "...its now older than four days.")
					counter += 1
					os.remove(rmvfile)
			else:
				print("CLEANING FILES - INFO - Removed",counter,'Files...', rmvfile,"This file did not meet the requirements.")
	print("done cleaning two day old files...\n----\nEND\n")

def saveThePlainText(plainText, renamedFile):
	path = pathlib.PurePath(renamedFile)
	base = path.name
	pathname = parent_app_location + "assets/upload/"+base + ".txt"
	with open(pathname, "w+") as text:
		text.write(plainText)
	print("File Saved:", pathname)

def main(x):
	print("starting iqHelper v0.5\n")
	start_time = datetime.now()
	#configPath = parent_app_location + 'assets/json/config.json'
	configPath = '/datadrive_01/IQHelperConfig/config.json'
	argsPath = x
	config = getConfig(configPath)
	for a in config['BUCKET'].keys():
		bucketFullName = a
		bucketShortName = config['BUCKET'][bucketFullName]
	renamedFile, result, oldParent, fInfo= moveAndRename(argsPath)
	renamedFile = ocr_the_pdf(renamedFile)
	print("Started splitFileDetection")
	quitCode = printed_page_splitter(renamedFile, oldParent)
	print("Ended splitFileDetection")
	if quitCode == 1: 
		firstPageName = splitPages(renamedFile)
		bucketFileName = putFile(firstPageName, bucketFullName) 
		print("Started awsReturn")
		awsReturn = getAWSData(bucketFileName, bucketShortName)
		print("Ended awsReturn")
		deleteAWSUpload(bucketFileName, bucketShortName)
		print("Deleted object from aws")
		keymap , valuemap, blockmap, plain = getText(awsReturn) 
		kvs = get_kv_relationship(keymap, valuemap, blockmap)
		saveThePlainText(plain, renamedFile)
		try:
			#print("\nDEBUG:\n", kvs, "\n", plain, "\n", result)
			#output, doctypeCode= searchKeys(config, kvs, plain, result['StoreName'], result['DocType'])
			output, doctypeCode = searchReturn(config, kvs, plain, result['StoreName'], result['DocType'])
			print(str(output))
			for a in (config['REQUIREDFIELDS'][str(doctypeCode)]).values():
				if a in output:
					print("doing cover page")
					#print(str(output))
					coverpage = createCoverPage(output, renamedFile, kvs)
					print("doing merged")
					merged = addCoverPage(coverpage, renamedFile, config, doctypeCode)
					#merged = addCoverPage(renamedFile, coverpage, config, doctypeCode)
					print(merged, "done\n----\n")
					#
				else:
					print("Failed")
					filePath = pathlib.PurePath(argsPath)
					newname = pathlib.PurePath(renamedFile)
					print("\nresult:", result)
					typeShortCode = config["FOLDER_TO_DOC_TYPE"][result['DocType']]
					failPath = config["FINAL DUMPS"][str(typeShortCode)]["DUMP"] + str(newname.name)
					failPath2 = str(filePath.parents[1]) + '/failure/' + str(newname.name)
					os.chdir(str(filePath.parents[1]) + '/failure/')
					shutil.move (renamedFile, failPath)
					with open(failPath2 + '.txt', 'w') as a_t:
							a_t.write(plain)
					with open(failPath2 + '.json', 'w') as a_j:
							a_j.write(str(json.dumps(kvs)))
					print("Failed File - ",failPath2,"\n----\n")
					config["FOLDER_TO_DOC_TYPE"][result['DocType']]
		except:
			print("Failed")
			filePath = pathlib.PurePath(argsPath)
			newname = pathlib.PurePath(renamedFile)
			typeShortCode = config["FOLDER_TO_DOC_TYPE"][result['DocType']]
			failPath = config["FINAL DUMPS"][str(typeShortCode)]["DUMP"] + str(newname.name)
			failPath2 = str(filePath.parents[1]) + '/failure/' + str(newname.name)
			os.chdir(str(filePath.parents[1]) + '/failure/')
			shutil.move (renamedFile, failPath)
			with open(failPath2 + '.txt', 'w') as a_t:
					a_t.write(plain)
			with open(failPath2 + '.json', 'w') as a_j:
					a_j.write(str(json.dumps(kvs)))
			print("Failed File - ",failPath2,"\n----\n")
		#HOLD HERE
		try:
			#print("clean")
			cleanFiles()
		except IsADirectoryError:
			print("bumped into a directory")
	
		end_time = datetime.now()
		time_delta = end_time-start_time
		elapsed = time_delta.total_seconds()
		print('DONE -',fInfo)
		print(elapsed, "seconds\n---\n")



if __name__ == "__main__":
	main(sys.argv[1])