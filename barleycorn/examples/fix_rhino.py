import datetime
import sys

print datetime.datetime.now()

print "sys.modules: " 
print sys.modules
print sys.modules.keys()

to_reload = [
    "barleycorn.toolkits.toolkitRhino",
    "barleycorn.examples.designs",
    "barleycorn.examples.scratch",
    "barleycorn.examples.designs_rhino"
]

for mod in to_reload:
    if mod in sys.modules:
        reload(sys.modules[mod])
        print "reloaded " + mod
