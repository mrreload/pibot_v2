__author__ = 'marc.hoaglin'
import time
import collections


ts = time.time()
print(ts)

tr2 = collections.defaultdict(list)
tr = collections.OrderedDict()
# tr.update({"Hello": "Goodbye"})
# tr.update({"Hola": "Adios"})
# tr["Hello"].add["GoodBye"]

tr[time.time()] = 123.01
time.sleep(.1)
tr[time.time()] = 456.78
time.sleep(.1)
tr[time.time()] = 654.001

print 'Size=' + str(len(tr))
# tr.items()
print 'all values'
for key, val in tr.items():
	print key, val

print 'One popitem'
print tr.popitem(last=False)
print 'all values'
for key, val in tr.items():
	print key, val
print 'One popitem'
print tr.popitem(last=False)
print 'all values'
for key, val in tr.items():
	print key, val

#tr.popitem(last=False)




