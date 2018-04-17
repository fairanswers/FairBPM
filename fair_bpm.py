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
    WAITING='WAITING'
    READY='READY'
    COMPLETE='COMPLETE'
    def __init__(self, id, name):
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name
        self.parents=[]
        self.state=Activity.WAITING

    def addParent(self, parentId):
        self.parents.append(parentId)

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

    def getFirstActivity(self):
        for act in self.activities:
            if len(act.parents) == 0:
                return act
        raise Exception("Can't find first activity")

    def findChildren(self, activity):
        children=[]
        id=activity.id
        for act in self.activities:
            if act.state != Activity.COMPLETE and id in act.parents:
                children.append(act)
        return children


class SimpleJobRunner(Pretty):
    def executeJob(self, job):
        print("Starting job for SimpleJobRunner.  Run all activites. "+str(job.name) )
        for act in job.activities:
            act.execute()

class BetterJobRunner(Pretty):
    def executeJob(self, job):
        print("Better Job Runner.  Start with the one with no parents. "+str(job.name) )
        first_activity=job.getFirstActivity()
        first_activity.execute()
        first_activity.state=Activity.COMPLETE
        tasksLeft=True
        while tasksLeft:
            activities=job.findChildren(first_activity)
            if not activities:
                tasksLeft=False
            else:
                for act in activities:
                    act.execute()
                    act.state=Activity.COMPLETE

print "SFSG"

two=Say("id22", "The Say Activity")
three=Sing("id33", "The Sing Activity")
#two.addParent(three.id)
three.addParent(two.id)

ps=Process("p1", "Process One")
ps.activities.append(two)
ps.activities.append(three)

print("ps="+str(ps) )

job=ps.createJob(111, "FirstJob")

print("About to run simple job")

runner = BetterJobRunner()
runner.executeJob(job)


