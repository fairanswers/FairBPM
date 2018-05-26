import pytest
from fair_bpm import Say, Sing, FlexibleJobRunner, Process
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph
import fair_bpm

@pytest.fixture()
def say():
    Say("id22", "The Say Activity")

@pytest.fixture()
def sing():
    Sing("id33", "The Sing Activity")

@pytest.fixture()
def process():
    two = Say("id22", "The Say Activity")
    three = Sing("id33", "The Sing Activity")
    three.addParent(two.id)
    four = Say("id44", "The Second Say Activity")
    four.addParent(two.id)
    five = Say("id55", "The Second Sing Activity")
    five.addParent(two.id)
    ps = Process("p2", "Process Two")
    ps.activities.append(two)
    ps.activities.append(three)
    ps.activities.append(four)
    ps.activities.append(five)
    return ps

def test_dot_tools(process):
    runner = FlexibleJobRunner()
    job = process.createJob(111, "SecondJob")
    runner.executeJob(job)
    tree = parse(job.to_dot())
    assert len(str(tree)) > 10
    g = SimpleGraph.build(tree.kid('Graph'))
    assert len(g.nodes) == 4
    assert len(g.edges) == 3

def test_run_job(process):
    ps = process

    runner = FlexibleJobRunner()

    print("ps=" + str(ps))

    job = ps.createJob(111, "SecondJob")
    runner.executeJob(job)
    tree = parse(job.to_dot())
    g = SimpleGraph.build(tree.kid('Graph'))
    for node in g.nodes:
        print("Node -> "+str(node.attrs))
#        assert node['state'] == 'COMPLETE'


