import lxml.etree as ET
import os
rootfolder = 'D:\workspace\sampledata\projectfolder'
#xml_filename='D:\workspace\sampledata\\tibcobw5xprocess.process'
xsl_filename='D:\workspace\TibcoMappingGenerator\StripNamespaces.xslt'

for subdir, dirs, files in os.walk(rootfolder):
    for file in files:
        print(file)
        if ('mapper' in file):
            xml_filename=os.path.join(subdir, file)
            print('have to go in')


        else:
            continue



recovering_parser = ET.XMLParser(recover=True)
dom = ET.parse(xml_filename, parser=recovering_parser)
xslt = ET.parse(xsl_filename, parser=recovering_parser)
transform = ET.XSLT(xslt)
newdom = transform(dom)

print(ET.tostring(newdom, pretty_print=True))