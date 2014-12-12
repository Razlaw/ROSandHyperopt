import hyperopt
from hyperopt import fmin, tpe, hp
from hyperopt.mongoexp import MongoTrials
import sys
import taskreg
import matplotlib.pyplot as plt
import numpy as np

# specification of the search space. First a choice between two methods. The second one with different parameters. After that to general parameters that allways have to be tuned 
space = [hp.choice('choiceAorB',
		# first choice, no parameters 
		[{'type': 1, 'scanToScan': 1},
		# second choice, parameters are choiceBchoice, choiceBint and choiceBint2. choiceBchoice is a nested choice 
		{'type': 2, 'MRSmapMethod': 2,
			'choiceBchoice': hp.choice('choiceBchoice',[ 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20]),
			'choiceBint': hp.quniform('choiceBint', 1, 5, 1),
			'choiceBint2': hp.quniform('choiceBint2', 50, 5000, 50)}]),
		# two parameters that allways have to be tuned 
			hp.quniform('allwaysDouble', 0.05, 0.95, 0.05),						
			hp.quniform('allwaysInteger', 20, 100, 5)]
			
# holds all values with the exp_key specified in the Makefile
# if ip (localhost), port (27017) or name of the database (razlaw) were changed in the Makefile, these changes have to be applied here as well  
trials = MongoTrials('mongo://localhost:27017/razlaw/jobs', exp_key=sys.argv[2])

# case for make server 
if sys.argv[1] == "search":
	best = fmin(taskreg.objective,
	    space=space,
	    trials=trials,
	    algo=tpe.suggest,
	    max_evals=1e6)
		
# case for make show 		
elif sys.argv[1] == "history":
	hyperopt.plotting.main_plot_history(trials)
elif sys.argv[1] == "histogram":
	hyperopt.plotting.main_plot_histogram(trials)
elif sys.argv[1] == "vars":
	bandit = hyperopt.Bandit(expr=space, do_checks=False)
	hyperopt.plotting.main_plot_vars(trials, bandit=bandit, colorize_best=5)
	
elif sys.argv[1] == "trialsToLoss":	
	# filters all the results with status == "ok" , definition is in taskreg.py
	oktrials = [t for t in trials.trials if t["result"]["status"] == "ok"]
	# all timestamps of "ok" trials are stored in trialIDs  
	tids = [t['result']['timeStamp'] for t in oktrials]
	# all results (loss) of "ok" trials are stored in cases  
	cases = [t['result']['loss'] for t in oktrials]

	# same as above for "fail" trials
	failtrials = [t for t in trials.trials if t["result"]["status"] == "fail"]
	failtids = [t['result']['timeStamp'] for t in failtrials]
	failcases = [t['result']['loss'] for t in failtrials]
	
	# scatter all "fail" trials with transparent red x marks and the label "fail" for the legend
	_a = plt.scatter(failtids, failcases, c='red', marker='x', label='fail', alpha=0.5)
	# scatter all "ok" trials with green circles and the label "ok" for the legend
	_b = plt.scatter(tids, cases, c='green', label='ok')

	# name the axes and plot 
	plt.xlabel('Timestamp')
	plt.ylabel('Loss')
	plt.title('Title of Plot')
	
	# plot a horizontal line e.g. the bassline for the result with standard parameters 
	line = plt.axhline(y=0.028346, xmin=0.0, xmax=1.0)
	# show legend at location "best"
	legend = plt.legend(loc='best')
	# show plot
	plt.show()

# case for make showone and showtwo
elif sys.argv[1] == "lossToInt":
	# similar to the case above to filter "ok" and "fail" trials
	oktrials = [t for t in trials.trials if t["result"]["status"] == "ok"]
	failtrials = [t for t in trials.trials if t["result"]["status"] == "fail"]
	# if you only want to plot the results for one of the choices, this is a possible way  
	choice = int(sys.argv[3])
	if choice == 1.0:
		# filter all the trials where the first choice was used 
		# beware that the first choice has the number 0
		maptrials = [t for t in oktrials if t['misc']['vals']['choiceAorB'] == [0.0]]
		failmaptrials = [t for t in failtrials if t['misc']['vals']['choiceAorB'] == [0.0]]
	elif choice == 2.0:
		maptrials = [t for t in oktrials if t['misc']['vals']['choiceAorB'] == [1.0]]
		failmaptrials = [t for t in failtrials if t['misc']['vals']['choiceAorB'] == [1.0]]

	# now we filter again to get the loss that corresponds to a certain value of "allwaysInteger" 
	# beware that the loss is scattered on the x-axis this time 
	tids = [t['result']['loss'] for t in maptrials]
	cases = [t['misc']['vals']['allwaysInteger'] for t in maptrials]
	failtids = [t['result']['loss'] for t in failmaptrials]
	failcases = [t['misc']['vals']['allwaysInteger'] for t in failmaptrials]
	
	# scattering as usual
	_a = plt.scatter(failtids, failcases, c='red', marker='x', label='fail', alpha=0.5)
	_b = plt.scatter(tids, cases, c='green', label='ok')

	# name as usual 
	plt.xlabel('Loss')
	plt.ylabel('allwaysInteger')
	plt.title('Title of Plot')
	
	# this time we use a vertical line to display the baseline, since the loss is on the x axis  
	line = plt.axvline(x=0.028346, ymin=0.0, ymax=1.0)
	plt.show()

# case for make best 
elif sys.argv[1] == "best":
	print trials.best_trial
