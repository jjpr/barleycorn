import datetime
import sys

print datetime.datetime.now()

print "sys.modules: " 
for key in sys.modules.keys():
    print key

to_reload = [
    "barleycorn.examples.designs_rhino"
]

for mod_name in to_reload:
    if mod_name in sys.modules:
        mod = sys.modules[mod_name]
        if mod:
            reload(mod)
            print "reloaded " + mod_name
