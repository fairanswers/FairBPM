#!/usr/bin/python
import copy
import os
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph
import time

class O(object):
  def __init__(i, **adds): i.__dict__.update(adds)


class Pretty(O):
    def __repr__(i):
        return i.__class__.__name__ + kv(i.__dict__)

def kv(d):
    return '(' + ', '.join(['%s: %s' % (k, d[k])
                              for k in sorted(d.keys())
                              if k[0] != "_"]) + ')'


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
        ERROR='ERROR' # Do we need this?

    def __init__(self, id, name):
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name
        self.parents=[]
        self.state=Activity.State.WAITING
        self.returned=self.Returned.ANY
        self.color={}
        self.color[self.State.WAITING]='WHITE'
        self.color[self.State.READY]='YELLOW'
        self.color[self.State.COMPLETE]='GREEN'
        self.color[self.State.ERROR]='RED'

    def to_dot(self):
        c= self.__class__
        dot = '  {} [ class = {} name = "{}" state = "{}" returned = "{}" color={} style=filled] \n'.format( self.id, self.__class__.__name__, self.name, self.state, self.returned, self.color[self.state])
        for p in self.parents:
            dot = dot + '{} -> {} \n'.format(p[0], self.id)
        return dot

    def isParent(self, aid, ret_val):
        for p in self.parents:
            if p[0] is aid and (p[1] is ret_val or p[1] == Activity.Returned.ANY):
                return True
            else:
                return False

    def addParent(self, parent):
        # Check for a string.  If so, assume ANY Returned
        if type(parent) is str:
            self.parents.append([parent, Activity.Returned.ANY])
        # Check for a list.  if so, add the first and second items as parent.
        if type(parent) is list:
            # Check for string
            if parent[0] is str:
                self.parents.append([parent[0], parent[1] ] )
            # Need to raise error if we ever get here, or inthe outer 'else' from here

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

    def to_dot(self):
        dot= 'digraph {} '.format(self.name) + "{"
        for act in self.activities:
            dot = dot + act.to_dot()

        dot = dot + '}\n'
        return dot

    def createJob(self, id, name):
        job = Job(id, name, self)
        return job

    @classmethod
    def parse(cls, dot):
        tree = parse(dot)
        print(tree)

        g = SimpleGraph.build(tree.kid('Graph'))
        print(g.nodes)
        print(g.edges)
        #Name and ID?
        


class Job(Process):
    def __init__(self, id, name, process):
        self.id=time.time()
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
            if act.state != Activity.State.COMPLETE and act.isParent(aid, activity.returned):
                children.append(act)
        return children

class FlexibleJobRunner(Pretty):
    def executeJob(self, job):
        print("Flexible Job Runner.  Handle multiple starts and runs multiple children.")
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

class dot_data_store(Pretty):

    def save(self, dot):
        pass

    def get(self, id):
        pass

    def delete(self, id):
        pass

    def list(self):
        pass

class file_dot_data_store(dot_data_store):
    store_dir="archive"

    def __init__(self):
        os.makedirs(self.store_dir, 'w', True)

    def save(self, dot):
        with open(dot.name, 'w') as f:
            f.write(dot.to_dot() )

    def get(self, name):
        with open(name) as f:
            f.read(name)

    def delete(self, id):
        pass

    def list(self):
        pass



