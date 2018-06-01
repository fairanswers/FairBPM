import pytest
from fair_bpm import Say, Sing, FlexibleJobRunner, Process
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph
import fair_bpm

@pytest.fixture()
def say():
    return Say("id22", "The Say Activity")

@pytest.fixture()
def sing():
    return Sing("id33", "The Sing Activity")

@pytest.fixture()
def process():
    two = Say("id22", "The Say Activity")
    three = Sing("id33", "The Sing Activity")
    three.add_parent(two.id)
    four = Say("id44", "The Second Say Activity")
    four.add_parent(two.id)
    five = Sing("id55", "The Second Sing Activity")
    five.add_parent(two.id)
    ps = Process("Process_Two")
    ps.activities.append(two)
    ps.activities.append(three)
    ps.activities.append(four)
    ps.activities.append(five)
    return ps

def test_dot_tools(process):
    runner = FlexibleJobRunner()
    job = process.createJob(111, "SecondJob")
    runner.execute_job(job)
    tree = parse(job.to_dot())
    assert len(str(tree)) > 10
    g = SimpleGraph.build(tree.kid('Graph'))
    assert len(g.nodes) == 4
    assert len(g.edges) == 3
    assert g.nodes['id44']['state'] == 'COMPLETE'


def test_run_job(process):
    ps = process

    runner = FlexibleJobRunner()

    print("ps=" + str(ps))

    job = ps.createJob(111, "SecondJob")
    runner.execute_job(job)
    tree = parse(job.to_dot())
    g = SimpleGraph.build(tree.kid('Graph'))
    for node in g.nodes:
        print("Node -> "+str(node))
        assert node['state'] == 'COMPLETE'

def test_to_dot(say):
    output = say.to_dot()
    print(output)
    assert len(output) > 50

def test_is_parent(say, sing):
    assert len(say.parents) == 0
    assert len(sing.parents) == 0
    sing.add_parent(say)
    say.returned=fair_bpm.Activity.Returned.ANY
    assert len(sing.parents) == 1
    assert False == say.has_parent(sing, fair_bpm.Activity.Returned.ANY)
    assert True  == sing.has_parent(say, fair_bpm.Activity.Returned.ANY)

def test_is_parent_conditional(say, sing):
    assert len(say.parents) == 0
    assert len(sing.parents) == 0
    sing.add_parent(say)
    assert len(sing.parents) == 1
    say.returned=fair_bpm.Activity.Returned.TRUE
    assert True  == sing.has_parent(say.id, fair_bpm.Activity.Returned.TRUE)
    assert True  == sing.has_parent(say.id, fair_bpm.Activity.Returned.ANY)


def test_file_store(process):
    name=process.id
    data=process.to_dot()
    store=fair_bpm.file_dot_data_store()
    # assert len(store.list() )==0
    out=store.save(process)
    loaded=store.load(name)
    #TODO: implement equals
    assert len(loaded.to_dot()) > 50 and len(process.to_dot()) > 50
    assert len(store.list())>0
 #   assert store.delete(loaded.id)

def test_parse_activity_from_dot():
    d={'asdf':'qwerty'}
    act=fair_bpm.Activity.parse_from_dot('bbb',d)
    assert act.asdf == 'qwerty'
