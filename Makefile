# needed so the database can distinguish between different tasks
# has to be changed everytime the search space in search.py or the return dimension in taskreg.py is changed 
EXPKEY=surfelopt1

all:
	echo "make {server|client|show|showone|showtwo|best}"

# fills a queue with jobs for the client, each job is a trial in the optimization task to find better parameters 
server:
	python search.py search $(EXPKEY)

# takes the jobs out of the queue and returns the result of the task 
# --mongo=localhost:27017/razlaw has to fit to your database and to the trials variable in search.py, 27017 is the default port and razlaw is the name of the used database 
client:
	PYTHONPATH=`pwd` hyperopt-mongo-worker --mongo=localhost:27017/razlaw --poll-interval=30 --exp-key=$(EXPKEY)

# plots plots
show:
	# progress of the loss
	python search.py history $(EXPKEY)
	# histogram of the loss 
	python search.py histogram $(EXPKEY)
	# effects of each parameter on the loss, 5 best trials coloured green
	python search.py vars $(EXPKEY)
	# example how to plot a special parameter against the loss 
	python search.py trialsToLoss $(EXPKEY)

# examples how to colourize different bool choices in the search space  
showone:
	python search.py ateMaxIter $(EXPKEY) 1

showtwo:
	python search.py ateMaxIter $(EXPKEY) 2

# return all values of the best trial 
best:
	python search.py best $(EXPKEY)

clean:
	find -type d -name '????????????????????????' -exec rm -r {} \;
