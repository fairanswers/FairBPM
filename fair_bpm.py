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

    #Pretty sure this will need some work.  Skipping for now
    class StateColor(Pretty):
        WAITING='WHITE'
        READY='YELLOW'
        COMPLETE='GREEN'
        ERROR='RED'

    def __init__(self, id=-1, name='unknown'):
        def __init__(self, id=-1, name='unknown'):
            O.__init__(self, id=-1, name=name)
        self.id = id
        self.name = name
        self.parents=[]
        self.state=Activity.State.WAITING
        self.returned=self.Returned.ANY
        self.color=self.StateColor.WAITING

    def to_dot(self):
        c= self.__class__
        dot = '  {} [ class = {} name = "{}" state = "{}" returned = "{}" color={} style=filled] \n'.format( self.id, self.__class__.__name__, self.name, self.state, self.returned, self.color)
        for p in self.parents:
            dot = dot + '{} -> {} \n'.format(p[0], self.id)
        return dot

    def has_parent(self, aid, ret_val):
        if isinstance(aid, Activity):
            aid=aid.id
        for p in self.parents:
            if p[0] is aid and (p[1] is ret_val or p[1] == Activity.Returned.ANY):
                return True
        return False

    def add_parent(self, parent):
        # Check for a list.  if so, add the first and second items as parent.
        if type(parent) is list:
            if type(parent[0]) is Activity:
                parent[0]=parent[0].id
            # Check for string
            if parent[0] is str:
                self.parents.append([parent[0], parent[1] ] )
                return
        # Check for a string.  If so, assume ANY Returned
        if type(parent) is str:
            self.parents.append([parent, Activity.Returned.ANY])
            return
        # Check for activity, assume ANY
        if isinstance(parent, Activity):
            self.add_parent(parent.id)
            return
            # Need to raise error if we ever load here, or inthe outer 'else' from here
        raise TypeError("Parent in add_parent must be string, Activity, or list of activit and condition")

    def execute(self):
        raise TypeError("Activity.execute should always be overridden, but is being invoked directly. id="+self.id+" name="+self.name)

    @classmethod
    def parse_from_dot(cls, id, fields):
        act=Activity(id)
        for key in fields:
            act.__setattr__(str(key),str(fields[key]))
        return act


class Say(Activity):
    def execute(self):
        print("In Say " +self.name)


class Sing(Activity):
    def execute(self):
        print("In Sing "+ self.name)


class Process(Pretty):
    def __init__(self, id):
        def __init__(self, id=-1 ):
            O.__init__(self, id=-1)
        self.id = id
        self.activities=[]

    def to_dot(self):
        dot= 'digraph {} '.format(self.id) + "{"
        for act in self.activities:
            dot = dot + act.to_dot()
        dot = dot + '}\n'
        return dot

    def createJob(self, id):
        job = Job(id, self)
        return job

    @classmethod
    def parse_to_simple_graph(cls, dot):
        tree = parse(dot)
        g = SimpleGraph.build(tree.kid('Graph'))
        return g

    @classmethod
    def parse(cls, dot):
        tree = parse(dot)
        id=tree.kid('Graph').children[1].label
        g = SimpleGraph.build(tree.kid('Graph'))
        ps=Process(id)
        for node in g.nodes:
            ps.activities.append(Activity.parse_from_dot(node, g.nodes[node]))
        for edge in g.edges:
            act=next((x for x in ps.activities if x.id == edge[1]), None)
            # if none throw error
            act.add_parent(edge[0])


        return ps


class Job(Process):
    def __init__(self, id, process):
        self.id=time.time()
        self.process=process
        self.activities=copy.deepcopy(process.activities)

    def get_first_activity(self):
        for act in self.activities:
            if len(act.parents) == 0:
                return act
        raise Exception("Can't find first activity")

    def find_children(self, activity):
        children=[]
        aid=activity.id
        for act in self.activities:
            if act.state != Activity.State.COMPLETE and act.has_parent(aid, activity.returned):
                children.append(act)
        return children

class FlexibleJobRunner(Pretty):
    def execute_job(self, job):
        self.set_all_parentless_activity_to_ready(job)
        while self.has_ready_activities(job):
            act = self.find_ready_activity(job)
            act.execute()
            act.state=Activity.State.COMPLETE
            nextReady = job.find_children(act)
            for nr in nextReady:
                nr.state = Activity.State.READY

    def set_all_parentless_activity_to_ready(self, job):
        for act in job.activities:
            if len(act.parents) == 0:
                act.state=Activity.State.READY

    def has_ready_activities(self, job):
        for act in job.activities:
            if act.state == Activity.State.READY:
                return True
        return False

    def find_ready_activity(self, job):
        for act in job.activities:
            if act.state == Activity.State.READY:
                return act

class dot_data_store(Pretty):

    def save(self, dot):
        pass

    def load(self, id):
        pass

    def delete(self, id):
        pass

    def list(self):
        pass

class file_dot_data_store(dot_data_store):
    store_dir=""
    extention=".dot"

    def __init__(self, dir=os.getcwd()+os.sep+"dot_archive"):
        self.store_dir=dir
        if not os.path.exists(self.store_dir):
            os.makedirs(self.store_dir)
        if not os.access(self.store_dir, os.W_OK):
            raise IOError("Can't write to archive directory "+self.store_dir)

    def save(self, dot):
        filename=self.store_dir + os.sep + dot.id + self.extention
        with open(filename, 'w') as f:
            f.write(dot.to_dot() )

    def load(self, id):
        filename=self.store_dir+os.sep+id+self.extention
        with open(filename) as f:
            dot=f.read()
        ps= Process.parse(dot)
        return ps


    def delete(self, id):
        pass

    def list(self):
        cont=os.listdir(self.store_dir)
        return cont


if __name__ == '__main__':
    import fair_bpm_test
    say=fair_bpm_test.say()
    sing=fair_bpm_test.sing()
    ps = fair_bpm_test.process()
    fair_bpm_test.test_parse_activity_from_dot()
    fair_bpm_test.test_file_store(ps)

