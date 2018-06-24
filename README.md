# FairBPM

## Overview
Fair BPM is a workflow library. With it, you can describe a process as a series of steps to get work done.

The basic building block in Fair BPM is the **Activity**.  An activity usually does one thing.  For instance, and activity might get data from a service, calculate a value, or send a message.

A group of activities is called a **Process**.  The process describes what activities will be executed and how they relate.

# Features:

*  Modular design
*  Conditional logic
*  Graphical Components
*  Easy to save and analyze

There are two modes in Fair BPM:  Design and Run.  Design time is where you build a process and
map out what should happen.  Run time takes a process, creates a Job from that process, and runs the job.  It remembers what activites have been completed and what values are set by each activity.

If you're an Object Oriented programmer: The process is like the class, and the job is the instance of that class.

# Example

For an example, lets say we have a (very smart) smart home, and we wanted a process that would automate dog chores.  The steps might be.

1.    Feed the dog.
2.    Give it water if it needs it.
3.    If it's the first of the month, give it a pill.  If its the last pill, order more.

If you break this into individual activites, it might look like this:
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
Programmatically, you would create a stand-alone piece of functionality that does each of the *custom* tasks (feed dog,
water dog, medicate dog, order medication).  This would interact with your smart home to find information and get things
done.

This code in in example/fair_bpm_example.py

<pre>
from fair_bpm import Activity

class feed_dog(Activity):
    def execute(self):
        print("Starting feed dog")
        # Put feed dog code here

class needs_water(Activity):
    def execute(self):
        print("Checking if dog needs water dog")
        # Put checking code here

class water_dog(Activity):
    def execute(self):
        print("Starting water dog")
        # Put water dog code here

    class medicate_dog(Activity):
    def execute(self):
        print("Starting medicate dog")
        # Put medicate dog code here

class order_medication(Activity):
    def execute(self):
        print("Starting order_medication dog")
        # Put order_medication dog code here
</pre>

What about the other tasks, where we make decisions?  Luckily, Fair BPM has some default activities that can handle that.
String manipulation, checking for values, and making simple decisions are all handled by Activiites that are already
written, like the Command activity.  More on that later.
<list>


### Graphically.
This flow would graphically look like this


### Conceptually
And behind the scenes, it would be saved in a file with a string like this.

<example>

