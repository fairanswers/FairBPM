#!/usr/bin/python

#import utest

# class Pretty(object):
#     def __repr__(i):
#         return i.__class__.__name__ + kv(i.__dict__)
#
# def kv(d):
#     return '(' + ', '.join(['%s: %s' % (k, d[k])
#                               for k in sorted(d.keys())
#                               if k[0] != "_"]) + ')'
#
# class O(Pretty):
#   def __init__(i, **adds): i.__dict__.update(adds)
#
#

class Activity(object):
    def __init__(self, id, name):
        print("Init Activity")
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name

    def execute(self):
        print("In Activity Execute. id="+self.id+" name="+self.name)


print "SFSG"
a=Activity("id11", "name22")
print a.id
print a.name
a.execute()




