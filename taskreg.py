#!/usr/bin/python
from hyperopt import STATUS_OK, STATUS_FAIL
import subprocess
import sys
import os
import fcntl
import time

# definition of the job the client has to work on 
def objective(args):
	# get the parameters defined in the search space 
	# beware that choiceAorB is the "choice-tuple", and allwaysDouble and allwaysInteger are the values that allways have to be tuned
	choiceAorB, allwaysDouble, allwaysInteger = args
	
	# this part is essential for having multiple clients working parallel on equal ROS nodes 
	print "starting subprocess"
	# the standard port for a ros core 
	port = 11311
	# try locking one of eight files to be sure that the node is started on a "free"/unused roscore 
	for count in range(0, 8):
		lockstring = "/tmp/.lock_%s.pod" % count
		fp = open(lockstring, 'w')
		try:
			fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
		except IOError:
			print "cannot lock file %s" % count
			continue
		# remember the port of the unused roscore 
		port = 11311 + count
		# and leave the loop 
		break
	else:
		# if no file is lockable quit this trial (and wait for a process to finish) 
		sys.exit(0)		
	
	# the threadid is used as are variable for the node, in case one has to lock something in the node or create files associated to this node or ... 
	threadid = port - 11311		
	
	# measure time if needed 
	start = time.time()
	# in case the first choice in the search space was made 
	if choiceAorB['type'] == 1:	
		# export a new ROS_MASTER_URI to use the unused roscore and then run rosrun as always, parameters can be set by _parameter:=value 
		# if you use a catkin workspace be aware that rosrun might search in the bin folder of the package for an executable, creating a symlink fixes this problem 
		command = "export ROS_MASTER_URI=http://localhost:%s && rosrun HyperoptROS hyperopt_ros _threadID:=%s _aConstant:=3 _choiceAorB:=%s _allwaysInteger:=%s _allwaysDouble:=%s" % (port,threadid,choiceAorB['type'],allwaysInteger,allwaysDouble)	
	# case of second choice, works analogously 
	elif choiceAorB['type'] == 2:	
		command = "export ROS_MASTER_URI=http://localhost:%s && rosrun HyperoptROS hyperopt_ros _threadID:=%s _aConstant:=3 _choiceAorB:=%s _choiceBchoice:=%s _choiceBint:=%s _choiceBint2:=%s _allwaysInteger:=%s _allwaysDouble:=%s" % (port,threadid,choiceAorB['type'],choiceAorB['choiceBchoice'],choiceAorB['choiceBint'],choiceAorB['choiceBint2'],allwaysInteger,allwaysDouble)	

	# for checking whether the command was right or which constellations cause problems 
	print command	

	# the node must be designed in a way that !only! the results are printed out, turn off all other outputs (like ROS_INFO and so on) 
	# if needed std::err can be used (e.g. debug info) 
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)	
	proc_out, proc_err = proc.communicate()
	print 'proc_out ', proc_out

	# measure time if needed 
	workedTime = time.time() - start
	
	# the printed out results have to be split by linebreaks 
	proc_out = proc_out.split("\n")
	assert len(proc_out) == 5
	assert len(proc_out[-1]) == 0
	# transform the results to float values and store them in the right variables 
	loss, otherOutput, timeStamp, random = (float(x) for x in proc_out[:-1])
	# print results, helps finding wrong results 
	print "ERGEBNIS loss=%2.3f, otherOutput=%2.3f, timeStamp=%2.3f, random=%2.3f" % (loss,otherOutput,timeStamp,random)
	# return the results to hyperopt, loss is always the value that has to be minimized and status is always a bool that shows hyperopt whether this run was ok 
	# other return values are only stored in the database, a unique stamp helps finding results in the database 
	return {'loss': loss,
			'status': STATUS_FAIL if (loss < 0.00001 or random > 50) else STATUS_OK,
			'otherOutput': otherOutput,
			'timeStamp': timeStamp,
			'random': random}
