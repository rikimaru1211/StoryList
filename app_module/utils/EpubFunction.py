import zipfile
import app_module.utils.HelpFunction as HelpFunction
from io import StringIO

MINETYPE = "mimetype"
MINETYPE_CONTENT = "application/epub+zip"
	
META_INF = "META-INF"
CONTAINER_XML = "META-INF/container.xml"
CONTAINER_XML_CONTENT = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""
	
OEBPS = "OEBPS"
CONTENT_OPF = "OEBPS/content.opf"
TOC_NCX = "OEBPS/toc.ncx"
TEXT = "OEBPS/Text"
TEXT_NAME = "Text"

def CreateMapFileHeader(id, sTitle):
	sKetQua = StringIO()
	sKetQua.write("""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="2.0">
	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
		<dc:title>""")
	sKetQua.write(sTitle)
	sKetQua.write("""</dc:title>
		<dc:language>en</dc:language>
		<dc:rights>Public Domain</dc:rights>
		<dc:creator opf:role="aut">TungCT</dc:creator>
		<dc:publisher>TungCT</dc:publisher>
		<dc:identifier id="BookID" opf:scheme="UUID">""")
	sKetQua.write(id)
	sKetQua.write("""</dc:identifier>
		<meta name="Sigil version" content="0.2.4"/>
	</metadata>
	<manifest>
		<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
""")
	return sKetQua.getvalue()

def CreateMapFileItem(index, src):
	sKetQua = StringIO()
	sKetQua.write("		<item id=\"chapter")
	sKetQua.write(str(index))
	sKetQua.write("\" href=\"")
	sKetQua.write(src)
	sKetQua.write("\" media-type=\"application/xhtml+xml\"/>\n")
	return sKetQua.getvalue()

def CreateMapFileEnd(length):
	sKetQua = StringIO()
	sKetQua.write("	</manifest>\n")
	sKetQua.write("	<spine toc=\"ncx\">\n")
	length = length + 1
	for i in range(1, length):
		sKetQua.write("		<itemref idref=\"chapter")
		sKetQua.write(str(i))
		sKetQua.write("\"/>\n")
	sKetQua.write("	</spine>\n")
	sKetQua.write("</package>")
	return sKetQua.getvalue()


def CreateIndexFileHeader(id, sTitle) :
	sKetQua = StringIO()
	sKetQua.write("""<?xml version="1.0" encoding="UTF-8"?> 
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
	"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"> 
			 
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"> 
	<head> 
		<meta name="dtb:uid" content=""")
	sKetQua.write("\"")
	sKetQua.write(id)
	sKetQua.write(""""/> 
		<meta name="dtb:depth" content="1"/> 
		<meta name="dtb:totalPageCount" content="0"/> 
		<meta name="dtb:maxPageNumber" content="0"/> 
	</head> 
	<docTitle> 
		<text>""")
	sKetQua.write(sTitle)
	sKetQua.write("""</text> 
	</docTitle> 
	<navMap>
""")
	
	return sKetQua.getvalue()

def CreateIndexFileItem(index, label, src):
	sKetQua = StringIO()
	sKetQua.write("		<navPoint id=\"chapter")
	sKetQua.write(str(index))
	sKetQua.write("\" playOrder=\"")
	sKetQua.write(str(index))
	sKetQua.write("""">
			<navLabel>
				<text>""")
	sKetQua.write(label)
	sKetQua.write("</text>\n" + 
			"			</navLabel>\n" + 
			"			<content src=\"")
	sKetQua.write(src)
	sKetQua.write("\" />\n" + 
			"		</navPoint>\n")
	return sKetQua.getvalue()

def CreateIndexFileEnd():
	sKetQua = StringIO()
	sKetQua.write("	</navMap>\n")
	sKetQua.write("</ncx>")
	return sKetQua.getvalue()


def CreateEpubFile(sTenTruyen, lstChuong, outFile):
	zipf = zipfile.ZipFile(outFile, 'w', compression=zipfile.ZIP_DEFLATED)

	#add cac file tinh vao zip file
	zipf.writestr(MINETYPE, MINETYPE_CONTENT.encode('utf-8'))
	zipf.writestr(CONTAINER_XML, CONTAINER_XML_CONTENT.encode('utf-8'))

	mapFile = StringIO()
	indexFile = StringIO()
	sIDTruyen = HelpFunction.UUID()

	mapFile.write(CreateMapFileHeader(sIDTruyen, sTenTruyen))
	indexFile.write(CreateIndexFileHeader(sIDTruyen, sTenTruyen))

	index = 0
	for vChuong in lstChuong:
		sTieuDe = vChuong["tieude"]
		strNoiDung = StringIO()
		strNoiDung.write("""<html xmlns="http://www.w3.org/1999/xhtml"> 
	                		<head>
	                			<meta http-equiv="Content-Type" content="text/html charset=utf-8" /><title>truyen</title>
	                		</head>
	                		<body> """)
		strNoiDung.write("<p>")
		strNoiDung.write(sTieuDe)
		strNoiDung.write("</p>")
		strNoiDung.write("<p>")
		strNoiDung.write(vChuong["noidung"].replace("\n", "</p><p>"))
		strNoiDung.write("</p>")
		strNoiDung.write("</body>") 
		strNoiDung.write("</html>")
		sNoiDung = strNoiDung.getvalue()

		index = vChuong["stt"]
		sTenFile = "/chuong"+str(index)+".xhtml"
		zipf.writestr(TEXT + sTenFile, sNoiDung.encode('utf-8'))

		mapFile.write(CreateMapFileItem(index, "Text" + sTenFile))
		indexFile.write(CreateIndexFileItem(index, sTieuDe, "Text" + sTenFile))

	mapFile.write(CreateMapFileEnd(len(lstChuong)))
	indexFile.write(CreateIndexFileEnd())

	zipf.writestr(CONTENT_OPF, mapFile.getvalue().encode('utf-8'))
	zipf.writestr(TOC_NCX, indexFile.getvalue().encode('utf-8'))

	zipf.close()
