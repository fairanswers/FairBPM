# FairBPM

Fair BPM is a simple, flexible workflow library. With it, you can describe a process and use
testable, reusable code strung together like building blocks.  It features

*  Simple, modular design
*  Conditional logic
*  Graphical Components
*  Easy to save and analyze

The basic building block in Fair BPM is the Activity.  An activity usually does one thing, like get data from a service,
calculate a value, or send a message.

A group of activities is called a process.  The process describes what activities will get run and how they relate.

There are two fundamentally different modes in Fair BPM:  Design and Run.  Design time is where you build a process and
map out what should happen. In a traditional language, this would be when you are writing code.

Run time takes the process, creates a Job from that process, and runs the job.  Traditionally, this would be what
happens when the code is running. It remembers what activites have been run, and what values have been set.

If you're an Object Oriented programmer: The process is like the class, and the job is the instance of that class.

For an example, lets say you wanted a process that would automate your morning chores.  The steps might be.

#.   Feed the dog.
#.   Give it water if it needs it.
#.   If it's the first of the month, give it a pill.  If its the last pill, order more.

If you break this into individual activites, it might look like this:
#.  Feed the dog.
#.  Does it need water?
#.     Yes: give it water.
#.     No: do nothing.
#.  Is it the first of the month?
#.     No: do nothing.
#.     Yes:  Give it a pill
#.        Any pills left?
#.           Yes: do nothing.
#.           No:  order pills.

