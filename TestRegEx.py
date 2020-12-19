import re
import json

inputstr="a/b/c[d/e/f='g']/h/i"
#outstr= re.sub(r"\[.+?\/.+?\]","[CheckForEachLoopfilter]", inputstr)
#print(outstr)

outpfx = "$ParseXML/pfx10:OrderRelease/@NotificationType='forTest'"
outstr= re.sub(r"\/.+?:","/", outpfx)
print(outstr)
outstr2= re.search(r"\[.+?\/.+?\]", inputstr)
#print((outstr2.re.Match.match))


try:
    with open('Config.json', 'r') as ConfigFile:
        global Config_dict
        Config_dict = json.load(ConfigFile)
        global requiredFileNamePattern
        requiredFileNamePattern = Config_dict['Config']['allowedFileNames']
        print(requiredFileNamePattern)
        global htmlHEAD
        print('gggg')
        htmlHEAD = Config_dict['Config']['htmlHEAD']
        print(htmlHEAD)
except Exception as e:
        print(str(e))
# load default config