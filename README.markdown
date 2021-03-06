Parallel Optimization using ROS and Hyperopt
==============

This tutorial concentrates on a parallel optimization of parameters using the Robot Operating System (ROS). 

For a general tutorial on the usage of hyperopt visit:

	http://jaberg.github.io/hyperopt/

## Included Files 

The ROS package HyperoptROS as a basic example how to get parameter values from Hyperopt and return the results. 

Makefile: to save some typing. 

search.py: defining the borders for the search and including some code to plot the results.

taskreg.py: to start ROS nodes parallel and get results of each one.

## Running the Optimization

Install the Hyperopt and MongoDB. 

HyperoptROS is a hydro catkin package containing a node with fitting parameters, a costfunction that has to be minimized and an output that prints this value, we can now start the optimization.

0. Copy the package into your workspace, run catkin_make and create a symlink in ``.../HyperoptROS/bin`` pointing to ``.../yourWorkspace/devel/lib/HyperoptROS/hyperopt_ros``

1. Decide how many nodes you want to run parallel and start this many roscores as shown in steps 2 to 5 

2. Start the first roscore as usual using port 11311

         roscore 

3. For a new roscore first start a new terminal and export a new ROS_MASTER_URI by 

         export ROS_MASTER_URI=http://localhost:11312
  here port 11312 is used

4. Then start the new core by 

         roscore -p 11312

5. For each new roscore repeat steps 3 and 4 and increase the port number (11312 -> 11313 -> .. )  

---

6. Open another Terminal and run a server by "make server"

7. Open just as many terminals as you have roscores and run a client in each of them by "make client" 
  
## Remark
 
There might be dependencies you have install before optimization. 
Scypy is one of these. Check if you have it in case of errors. 
