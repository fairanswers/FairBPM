import pytest
import fair_bpm
import fair_bpm_example
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph
import fair_bpm

@pytest.fixture()
def say():
    return fair_bpm.Say("id22", "The Say Activity")

@pytest.fixture()
def sing():
    return fair_bpm.Sing("id33", "The Sing Activity")

@pytest.fixture()
def process():
    two = fair_bpm.Say("id22", "Say")
    three = fair_bpm.Sing("id33", "Sing")
    three.add_parent(two.id)
    four = fair_bpm.Say("id44", "Say")
    four.add_parent(two.id)
    five = fair_bpm.Sing("id55", "Sing")
    five.add_parent(two.id)
    ps = fair_bpm.Process("Process_Two")
    ps.activities.append(two)
    ps.activities.append(three)
    ps.activities.append(four)
    ps.activities.append(five)
    return ps

@pytest.fixture()
def good_dot_src():
    str='''
    digraph one {
  urgent [ name = "Always_True" state = "WAITING" returned = "ANY" fillcolor=WHITE style=filled shape=ellipse]
  send_text [ name = "Random_True_False" state = "WAITING" returned = "ANY" fillcolor=WHITE style=filled shape=ellipse]
  send_email [ name = "Always_False" state = "WAITING" returned = "ANY" fillcolor=WHITE style=filled shape=ellipse]
  end [ name = "Say" state = "WAITING" returned = "ANY" fillcolor=WHITE style=filled shape=ellipse]
  error [ name = "Say" state = "WAITING" returned = "ANY" fillcolor=WHITE style=filled shape=ellipse]
  urgent -> send_email [label="False"]
  urgent -> send_text [label="True"]
  send_text -> end [label="True"]
  send_email -> end [label="True"]
  send_text -> error [label="False"]
  send_email -> error [label="False"]
}
    '''
    return str

@pytest.fixture()
def chore_dot():
    str='''
digraph chores
{
    feed_dog -> needs_water [label="ANY"]
    needs_water -> water_dog [label=True]
    needs_water -> is_first_of_month [label=False]
    water_dog -> is_first_of_month [label=True]
    is_first_of_month -> end [label=False]
    is_first_of_month -> medicate_dog [label=True]
    medicate_dog -> pills_left 
    pills_left -> end [label=True]
    pills_left -> order_medication [label=False]
    order_medication -> end [label=True]
    
    feed_dog [name="fair_bpm_example.FeedDog"]
    needs_water [name="Command"]
    water_dog [name="fair_bpm_example.WaterDog"]
    is_first_of_month [name=Command command="return True"]
    end [name=Say]
    medicate_dog [name="fair_bpm_example.MedicateDog"]
    pills_left [name=Command command="return False"]
    order_medication [name="fair_bpm_example.OrderMedication"]
}
'''
    return str

def test_dot_tools(process):
    runner = fair_bpm.FlexibleJobRunner()
    job = process.createJob(111)
    runner.execute_job(job)
    tree = parse(job.to_dot())
    assert len(str(tree)) > 10
    g = SimpleGraph.build(tree.kid('Graph'))
    assert len(g.nodes) == 4
    assert len(g.edges) == 3
    assert g.nodes['id44']['state'] == 'COMPLETE'


def test_run_job(process):
    ps = process

    runner = fair_bpm.FlexibleJobRunner()

    print("ps=" + str(ps))

    job = ps.createJob(111)
    runner.execute_job(job)
    tree = parse(job.to_dot())
    g = SimpleGraph.build(tree.kid('Graph'))
    for node in g.nodes:
        # print("Node -> "+str(node))
        assert g.nodes[node]['state'] == 'COMPLETE'

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

def test_execute_with_context(process):
    com=fair_bpm.Command()
    context={}
    context['first']=1
    com.command="answer=1"
    com.execute(context)
    assert context['answer'] == 1
    com.command = "answer=answer+answer"
    com.execute(context)
    assert context['answer'] == 2

def test_parse_conditional_parents_from_dot(good_dot_src):
    ps=fair_bpm.Process.parse(good_dot_src)
    act=ps.find_activity_by_id('urgent')
    assert len(act.parents)==0
    act=ps.find_activity_by_id('send_text')
    assert len(act.parents)==1
    act=ps.find_activity_by_id('error')
    assert len(act.parents)==2

def test_random_activities(good_dot_src):
    ps=fair_bpm.Process.parse(good_dot_src)
    runner=fair_bpm.create_runner()
    for x in range(1, 100):
        job=ps.createJob("888")
        runner.run(job)
        assert job.find_activity_by_id('urgent').returned == True
        assert job.find_activity_by_id('send_email').state == 'WAITING'
        assert job.find_activity_by_id('send_text').state == 'COMPLETE'
        assert (job.find_activity_by_id('send_text').returned == True
            or job.find_activity_by_id('error').state == 'COMPLETE')
        assert (job.find_activity_by_id('send_text').returned == False
            or job.find_activity_by_id('end').state == 'COMPLETE')

def test_chores(chore_dot):
    ps = fair_bpm.Process.parse(chore_dot)
    runner = fair_bpm.create_runner()
    job = ps.createJob("999")
    runner.run(job)


def get_module_class_name_from_dot_name():
    default="Say"
    external="otherpackage.Say"
    result = fair_bpm.Activity.get_module_class_name_from_dot_name(default)
    assert result[0] == "fair_bpm" and result[1] == "Say"
    result=fair_bpm.Activity.get_module_class_name_from_dot_name(external)
    assert result[0] == "otherpackage" and result[1]== "Say"
