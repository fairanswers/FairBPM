import sys, fair_bpm

infile="demo.dot"
print(len(sys.argv))
if len(sys.argv) == 2:
    infile = sys.argv[1]

print("Processing file "+infile)
print("File Contents:")
with open(infile, 'r') as myfile:
    src=myfile.read()
print(src)
print("Parsing file")
ps = fair_bpm.Process.parse(src)
print("Creating job")
job = ps.createJob("999")
print("Creating job runner")
runner = fair_bpm.create_runner()
print("Running job")
runner.run(job)
print("Completed output\n")
print(job.to_dot())