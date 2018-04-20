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
    class State(Pretty):
        WAITING='WAITING'
        READY='READY'
        COMPLETE='COMPLETE'
        ERROR = 'ERROR'

    class Returned(Pretty):
        TRUE=True
        FALSE=False
        ANY='ANY'

    def __init__(self, id, name):
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name
        self.parents=[]
        self.state=Activity.State.WAITING

    def addParent(self, parent):
        if type(parent) is str:
            self.parents.append(parent)
        else:
            self.parents.append(parent.id)

    def execute(self):
        print("In Activity Execute. id="+self.id+" name="+self.name)

class Say(Activity):
    def execute(self):
        print("In Say " +self.name)

class Sing(Activity):
    def execute(self):
        print("In Sing "+ self.name)

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
        aid=activity.id
        for act in self.activities:
            if act.state != Activity.State.COMPLETE and aid in act.parents:
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
        first_activity.state=Activity.State.COMPLETE
        tasksLeft=True
        while tasksLeft:
            activities=job.findChildren(first_activity)
            if not activities:
                tasksLeft=False
            else:
                for act in activities:
                    act.execute()
                    act.state=Activity.State.COMPLETE

class FlexibleJobRunner(Pretty):
    def executeJob(self, job):
        print "Flexible Job Runner.  Handle multiple starts and runs multiple children."
        self.setAllParentlessActivityToReady(job)
        while self.hasReadyActivities(job):
            act = self.findReadyActivity(job)
            act.execute()
            act.state=Activity.State.COMPLETE
            nextReady = job.findChildren(act)
            for nr in nextReady:
                nr.state = Activity.State.READY

    def setAllParentlessActivityToReady(self, job):
        for act in job.activities:
            if len(act.parents) == 0:
                act.state=Activity.State.READY

    def hasReadyActivities(self, job):
        for act in job.activities:
            if act.state == Activity.State.READY:
                return True
        return False

    def findReadyActivity(self, job):
        for act in job.activities:
            if act.state == Activity.State.READY:
                return act

print "SFSG"

two=Say("id22", "The Say Activity")
three=Sing("id33", "The Sing Activity")
three.addParent(two)
four=Say("id44", "The Second Say Activity")
four.addParent(two)
five=Say("id55", "The Second Sing Activity")
five.addParent(two)

runner = FlexibleJobRunner()
ps=Process("p2", "Process Two")
ps.activities.append(two)
ps.activities.append(three)
ps.activities.append(four)
ps.activities.append(five)

print("ps="+str(ps) )

job=ps.createJob(111, "SecondJob")
runner.executeJob(job)


