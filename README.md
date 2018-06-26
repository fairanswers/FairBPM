# FairBPM

## Overview
Fair BPM is a workflow library. With it, you can describe a something you want to do, then have the computer do it.  It's like
a simple programming language that non-programmers can use. Since it's simple and flexible, our business users can change
how it works without waiting for the requirements/design/code/test/deploy cycle.

The basic building block in Fair BPM is the **activity**.  An activity usually completes one step.  For instance, an activity
might get data from a service, calculate a value, or send an email.  The activity gets written in python where we can
test it before it goes into production.  Once it's deployed, the activity can be strung together with other
activities to describe a process. Activities can be used more than once in the same process.

A **process** is a group of activities.  The process describes what activities will be executed and how they relate.

To run a process, you first create a **job**. A job is a copy of the process that remembers which steps have been done.
If a process is a recipe for a meal, a job is what happens when someone orders that meal.
If you run two jobs they will have different details, even if they use the same process.

# Example

For an example, lets say we have a (very smart) smart home, and we wanted a process that would automate dog chores.  The steps might be.

1.    Feed the dog.
2.    Give it water if it needs it.
3.    If it's the first of the month, give it a pill.  If its the last pill, order more.

If you break this into individual activities, it might look like this:
1.    Feed the dog.
2.    Does it need water?

        2.1    Yes: give it water.

        2.2    No: do nothing.

3.    Is it the first of the month?

        3.1      No: do nothing.

        3.2      Yes:  Give it a pill

        3.3      Any pills left?

                3.3.1 . Yes: do nothing.

                3.3.2 . No:  order pills.

4.    Finish


### Step 1:  Programmatically
Programmatically, you can see there are two types of tasks: custom and standard.  A custom commands interact wit the smart home: feed dog,
water dog, medicate dog, order medication. Standard commands are
for making decisions and simple calculations.  Custom command look like this.

[This code in in example/fair_bpm_example.py]

<pre>
import fair_bpm

class FeedDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting feed dog")
        # Put feed dog code here

class WaterDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting water dog")
        # Put water dog code here

class MedicateDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting medicate dog")
        # Put medicate dog code here
        # Set Pills Left in context

class OrderMedication(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting order_medication dog")
        # Put order_medication dog code here
</pre>

What about the other tasks, where we make decisions?  Luckily, Fair BPM has some default activities that can handle that.
String manipulation, comparing values, and making simple decisions are all handled by the Command activity.  More on that later.


### Graphically.
This flow would graphically look like this

![Example Chores Process][example/ExampleChoresProcess.PNG]

### Conceptually
We start at the top and see the first activity is to water the dog.  Then the arrow goes to "need_water", and there are two
arrows that come from that, labeled True and False.  If the dog does need water, it follows the True path and add some water
to her bowl.  If not, it skips that step and goes on.

Each activity can have a "returned" vale that can be either True, False, or Any. If your link to the next step is Any, the job doesn't care if you returned a True or False, or if you just left it as Any. Otherwise it only follow the step with its label.

Behind the scenes, chores are saved in a file with a string like this.
<pre>
digraph chores
{
    feed_dog [name="fair_bpm_example.FeedDog"]
    needs_water [name="fair_bpm_example.CheckWater"]
    water_dog [name="fair_bpm_example.WaterDog"]
    is_first_of_month [name=Command command="me.returned=True"]
    end [name=Say]
    medicate_dog [name="fair_bpm_example.MedicateDog"]
    pills_left [name=Command command="me.returned=False"]
    order_medication [name="fair_bpm_example.OrderMedication"]

    feed_dog -> needs_water [label="Any"]
    needs_water -> water_dog [label=True]
    needs_water -> is_first_of_month [label=False]
    water_dog -> is_first_of_month [label=Any]
    is_first_of_month -> end [label=False]
    is_first_of_month -> medicate_dog [label=True]
    medicate_dog -> pills_left
    pills_left -> end [label=True]
    pills_left -> order_medication [label=False]
    order_medication -> end [label=Any]
}

</pre>


# Features:

*  Modular design
*  Conditional logic
*  Graphical Components
*  Easy to save and analyze

# Behind the scenes
FairBPM communicates jobs and processes in a language known as [DOT](https://www.graphviz.org/).  DOT describes activities as nodes, and decisions as lines.  This way, we can easily describe what needs to be done.

If you'll look at the chores example above, you can see there are a set of nodes (feed_dog, needs_water,...), a blank line, and then a list of relationships between the nodes.  This is how DOT files work.  You can add all the extra key/value pairs you need, and it's still valid DOT format, whether DOT uses that pair or not.  This flexibility lets us use it for our processes.

For each activity there are a list of key/value pairs [inside brackets] that give you the name of the activity.  These correspond to the class names that get run for every activity.

If you'll look at the is_first_of_month node, the name is Command, and it has a "command" pair.  This value is actually __python__ code that gets run for this activity.  This is dangerous in the hands of hackers so you'll need to be careful.

# What's Missing?
The big thing that users need (but the library doesn't) is a Graphcial User Interface.  This is a graphical language, and it needs a reliable interface for the users to use.  Otherwise, they'll be POSTing strings to services to design processes.

Luckily, Graphviz has been around for decades, so there are parsers for it in just about any language you'd want to use.

# Installation
TBD

# What's Missing?
As you can see, the FairBPM is a back-end library for running workflows.  In order to be a helpful tool for non-programmers,
we'll need a snazzy front end that makes it easy to
*  Declare nodes and Edges (and their attributes)
*  Use the RESTful interface to CRUD processes
