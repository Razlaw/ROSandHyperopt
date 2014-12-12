#include <ros/ros.h>
#include <string>
#include <stdlib.h>
#include <time.h>       

int main( int argc, char** argv ) {

	// init
	ros::init( argc, argv, "hyperopt_ros" );

	// for parameters
	ros::NodeHandle nh();
	ros::NodeHandle ph("~");

	int threadID = 0;
	// some default values for parameters defined in the searchspace 
	int choiceAorB;

	double choiceBchoice = 8.0;
	int choiceBint = 4;
	int choiceBint2 = 250;
	
	int allwaysInteger = 10;
	double allwaysDouble = 0.9;

	int aConstant;

	// getting values from rosrun 
	ph.getParam("choiceAorB", choiceAorB);

	ph.getParam("choiceBchoice", choiceBchoice);
	ph.getParam("choiceBint", choiceBint);
	ph.getParam("choiceBint2", choiceBint2);

	ph.getParam("allwaysInteger", allwaysInteger);
	ph.getParam("allwaysDouble", allwaysDouble);

	ph.getParam("aConstant", aConstant);

	ph.getParam("threadID", threadID);

	// setting logger level for no output
	if( ros::console::set_logger_level(ROSCONSOLE_DEFAULT_NAME, ros::console::levels::Fatal) ) {
	   ros::console::notifyLoggerLevelsChanged();
	}
	
	// in case you need output
	std::cerr << "Output hyperopt ignores" << std::endl;

	// your code here 

	// some random calculations to generate some output 
	double loss;
	double otherOutput;
	if (choiceAorB == 1){
 		loss = (allwaysDouble + 2.0);
		otherOutput = static_cast<double>(allwaysInteger);
	}else{
		loss = (allwaysDouble + choiceBchoice) * aConstant;
		otherOutput = static_cast<double>(allwaysInteger) + choiceBint * choiceBint2;
	}

	ros::Time stamp = ros::Time::now();

  	srand (time(NULL));
 	double random = rand() % 100;

	// threadID could be used to generate some files 

	// output for hyperopt
	std::cout << loss << std::endl;
	std::cout << otherOutput << std::endl;
	std::cout << stamp.sec << std::endl;
	std::cout << random << std::endl;

	ros::shutdown();

	return 0;
}


	

