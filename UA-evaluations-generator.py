import json, geojson, requests
import random, os, sys, shutil
import GeodesignHub, ShapelyHelper, config
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape, mapping, shape, asShape
from shapely.geometry import MultiPolygon, MultiPoint, MultiLineString
from shapely.ops import unary_union
from urllib.parse import urlparse
from os.path import splitext, basename
import zipfile	
import re	
import fiona
from fiona.crs import from_epsg
from shapely.geometry import box
from shapely.ops import unary_union

class DataDownloader():
	def downloadAOIFile(self, urls):
		for url in urls: 
			disassembled = urlparse(url)
			filename = basename(disassembled.path)
			ext = os.path.splitext(disassembled.path)[1]
			cwd = os.getcwd()
			outputdirectory = os.path.join(cwd,config.settings['workingdirectory'])
			if not os.path.exists(outputdirectory):
				os.mkdir(outputdirectory)
			local_filename = os.path.join(outputdirectory, filename)
			if not os.path.exists(local_filename):
				print("Downloading from %s..." % url)
				r = requests.get(url, stream=True)
				
				with open(local_filename, 'wb') as f:
				    for chunk in r.iter_content(chunk_size=1024): 
				        if chunk: # filter out keep-alive new chunks
				            f.write(chunk)

			if ext == '.zip':
				shapefilelist = self.unzipFile(local_filename)
			else: 
				shapefilelist = local_filename
		return shapefilelist	

	def readFile(self, filename):
		cwd = os.getcwd()
		workingdirectory = os.path.join(cwd,config.settings['workingdirectory'])
		local_filename = os.path.join(workingdirectory, filename)	
		
		ext = os.path.splitext(local_filename)[1]
		try:
			assert os.path.exists(local_filename)
		except AssertionError as ae:
			print("Input file does not exist %s" % ae)
		if ext == '.zip':
			shapefilelist = self.unzipFile(local_filename)
		else: 
			shapefilelist = [local_filename]
		return shapefilelist

			
	def unzipFile(self, zippath):
		# zip_ref = zipfile.ZipFile(zippath, 'r')
		print("Unzipping archive.. %s" % zippath)
		cwd = os.getcwd()
		workingdirectory = os.path.join(cwd,config.settings['workingdirectory'])
		shapefilelist = []
		fh = open(zippath, 'rb')
		z = zipfile.ZipFile(fh)
		for name in z.namelist():
			basename= os.path.basename(name)
			filename, file_extension = os.path.splitext(basename)
			if file_extension == '.shp' and 'MACOSX' not in name:

				shapefilelist.append(name)
			z.extract(name, workingdirectory)
		fh.close()

		return shapefilelist

class EvaluationBuilder():
	def __init__(self, systemname):

		self.redFeatures = []
		self.yellowFeatures = []
		self.greenFeatures = []
		self.systemname = systemname
		self.clippedFile = 0
		self.colorDict = {'red':self.redFeatures, 'yellow':self.yellowFeatures, 'green':self.greenFeatures}
		self.addedFeatures = []
	def processFile(self, color, uafile,uacodes):
		curfeatures = self.colorDict[color]
		cwd = os.getcwd()
		
		uafile = os.path.join(cwd,config.settings['workingdirectory'], uafile)
		with fiona.open(uafile, driver="GPKG") as source:
			for feature in source: 
				try: 
					if int(feature['properties']['code_2018']) in uacodes:
						curfeatures.append(feature)	
						self.addedFeatures.append(int(feature['properties']['OBJECTID']))
				except KeyError as ke:
					pass
		self.colorDict[color] = curfeatures

	def unAddedAsYellow(self,uafile):
		cwd = os.getcwd()
		uafile = os.path.join(cwd,config.settings['workingdirectory'], uafile)
		with fiona.open(uafile) as source:
			for feature in source: 
				if int(feature['properties']['OBJECTID']) in self.addedFeatures:
					pass
				else:
					self.colorDict['yellow'].append(feature)


	def writeEvaluationFile(self):
		opgeojson = self.systemname + '.geojson'
		cwd = os.getcwd()
		outputdirectory = os.path.join(cwd,config.settings['outputdirectory'])
		if not os.path.exists(outputdirectory):
			os.mkdir(outputdirectory)
		opfile = os.path.join(outputdirectory, opgeojson)
		fc = {"type":"FeatureCollection", "features":[]}
		for color, colorfeatures in self.colorDict.items():
			for curcolorfeature in colorfeatures:
				# print curcolorfeature
				f = json.loads(ShapelyHelper.export_to_JSON(curcolorfeature))
				f['properties']={}
				f['properties']['areatype'] = color.lower()
				fc['features'].append(f)

		with open(opfile, 'w') as output_evaluation:
			output_evaluation.write(json.dumps(fc))

	def cleanDirectories(self):
		cwd = os.getcwd()

		folders = [os.path.join(cwd,config.settings['workingdirectory'])]
		for folder in folders:
			for the_file in os.listdir(folder):
			    file_path = os.path.join(folder, the_file)
			    try:
			        if os.path.isfile(file_path):
			            os.unlink(file_path)
			        elif os.path.isdir(file_path): shutil.rmtree(file_path)
			    except Exception as e:
			        pass

if __name__ == '__main__':
	
	corinedataurl = config.settings['corinedata']
	systems = config.settings['systems']
	aoifile = config.settings['aoifile']
	uafile = os.path.join(os.getcwd(), config.settings['workingdirectory'], corinedataurl)
	myFileDownloader = DataDownloader()
	aoifile = myFileDownloader.downloadAOIFile([aoifile])
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	isURL = re.match(regex, corinedataurl) is not None

	myFileDownloader = DataDownloader()
	if isURL: 
		uafile = myFileDownloader.downloadFiles([corinedataurl])[0]
	else: 
		uafile = myFileDownloader.readFile(corinedataurl)[0]


	# for system, processchain in config.processchains.iteritems():
	for system in systems: 
		processchain = config.processchains[system]
		print("Processing %s .." % system)
		myEvaluationBuilder = EvaluationBuilder(system)
		for evaluationcolor, uacodes in processchain.items():
			myEvaluationBuilder.processFile(evaluationcolor,uafile,uacodes)
		myEvaluationBuilder.unAddedAsYellow(uafile)

		myEvaluationBuilder.writeEvaluationFile()

	
	# myEvaluationBuilder.cleanDirectories()


