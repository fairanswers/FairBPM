#!/usr/bin/python

#import utest
import copy

class Pretty(object):
    def __repr__(i):
        return i.__class__.__name__ + kv(i.__dict__)

def kv(d):
    return '(' + ', '.join(['%s: %s' % (k, d[k])
                              for k in sorted(d.keys())
                              if k[0] != "_"]) + ')'

class O(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)



class Activity(Pretty):
    def __init__(self, id, name):
        print("Init Activity")
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name

    def execute(self):
        print("In Activity Execute. id="+self.id+" name="+self.name)

class Say(Activity):
    def execute(self):
        print("In Say")


class Sing(Activity):
    def execute(self):
        print("In Sing")

class Process(Pretty):
    def __init__(self, id, name):
        print("Init Process")
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name
        self.activities=[]

    def createJob(self, id, name):
        job = Job(id, name, self)
        return job



class Job(Pretty):
    def __init__(self, id, name, process):
        self.id=id
        self.name=name
        self.process=process
        self.activities=copy.deepcopy(process.activities)

class SimpleJobRunner(Pretty):
    def executeJob(self, job):
        print("Starting job "+str(job) )
        for act in job.activities:
            act.execute()



print "SFSG"
one=Activity("id11", "name22")
print one.id
print one.name
one.execute()

two=Say("id22", "The Say Activity")
three=Sing("id33", "The Sing Activity")


two.execute()
three.execute()

ps=Process("p1", "pOne")
ps.activities.append(two)
ps.activities.append(three)

print("ps="+str(ps) )

job=ps.createJob(111, "FirstJob")

# print("job before change="+str(job) )
#
# job.activities[0].name="different"
#
# print("job after change="+str(job) )
#
# print("ps after change="+str(ps) )

print("About to run simple job")

runner = SimpleJobRunner()
runner.executeJob(job)


