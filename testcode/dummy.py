__author__ = 'marc.hoaglin'
import time
import collections


ts = time.time()
print(ts)

tr2 = collections.OrderedDict()
tr = collections.OrderedDict()
# tr.update({"Hello": "Goodbye"})
# tr.update({"Hola": "Adios"})
# tr["Hello"].add["GoodBye"]

tr[float(time.time())] = 123.01
tr2[time.time()] = "First Value"
time.sleep(.01)
tr[time.time()] = 456.78
tr2[time.time()] = "Second Value"
time.sleep(.01)
tr[time.time()] = 654.001
tr2[time.time()] = "3rd value"

print "time.time(): %f " %  time.time()
ti = float("%0.3f" %  time.time())
print float(ti)
print 'Size=' + str(len(tr))
# tr.items()
print 'all values'
for key, val in tr.items():
	print key, val

it1 = tr.popitem(last=False)
print it1[0]

print 'Getting item from tr2'
print tr2.get(it1[0])

it2 = tr.popitem(last=False)
print tr2.get(it2[0])

it3 = tr.popitem(last=False)
print tr2.get(it3[0])

print 'Size=' + str(len(tr))
#tr.popitem(last=False)




