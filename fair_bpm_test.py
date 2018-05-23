import pytest
from fair_bpm import Say, Sing, FlexibleJobRunner, Process
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph


def test_dumb():
    print("SFSG")

    two = Say("id22", "The Say Activity")
    three = Sing("id33", "The Sing Activity")
    three.addParent(two.id)
    four = Say("id44", "The Second Say Activity")
    four.addParent(two.id)
    five = Say("id55", "The Second Sing Activity")
    five.addParent(two.id)

    runner = FlexibleJobRunner()
    ps = Process("p2", "Process Two")
    ps.activities.append(two)
    ps.activities.append(three)
    ps.activities.append(four)
    ps.activities.append(five)

    print("ps=" + str(ps))

    print("to_dot" + five.to_dot())
    job = ps.createJob(111, "SecondJob")
    runner.executeJob(job)
    print('ps.to_dot' + ps.to_dot())
    print('job.to_dot' + job.to_dot())

    tree = parse(job.to_dot())
    print(tree)

    g = SimpleGraph.build(tree.kid('Graph'))
    print(g.nodes)
    print(g.edges)

