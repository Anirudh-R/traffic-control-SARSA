## Adaptive traffic control system using Reinforcement Learning

This project implements differential semi-gradient n-step SARSA algorithm to tackle the traffic congestion problem. More information can be found in the `/docs` folder and in the first referenced paper.

We use SUMO ([Simulation of Urban MObility](https://eclipse.dev/sumo/)) V1.6 package to simulate traffic patterns on which the algorithm has been tested. Details of SUMO installation can be found in the [documentation](https://sumo.dlr.de/docs/Installing.html). The TraCI API is used to control/monitor the simulation from Python.

We have used PyCharm and Anaconda for developement of this project. Any IDEs can be used, provided that the dependencies are properly installed in your respective environments.

The project folder contains two directories:
* The `/src` directory contains all the source codes needed to run the project.
* The `/scripts` directory contains SUMO files needed to generate traffic patterns. Also, output files from SUMO will be generated in this directory.

### Procedure to run the project
1. Set the `n`, `c`, and `Nruns` parameters in the `main.py` file. These values can be changed to test the n-step SARSA algorithm. We found optimal performance with `n=3` and `c=2`. 
2. Run `main.py`. This will run static signalling algorithm for `Nruns` trials and LQF algorithm for `Nruns` trials. Then, the trainiing for n-step SARSA will start. Based on the trained weights, SARSA Live will run for `Nruns` trials. All the performance metrics will be stored in the `/src/datapoints` sub-directory.
3. Set the `n` and `c` values that were used in the previous step in the `test.py` file and run it to get the performance graphs.

### References
1. Reinforcement Learning based Intelligent Traffic Signal Control using n-step SARSA: https://ieeexplore.ieee.org/document/9395942
2. Reinforcement Learning: An introduction by Richard S. Sutton and Andrew G. Barto, Chapter 7.
3. Reinforcement Learning With Function Approximation for Traffic Signal Control:
   http://www.cse.iitm.ac.in/~prashla/papers/2011RLforTrafficSignalControl_ITS.pdf
4. Diagnosing Reinforcement Learning for Traffic Signal Control:
   https://arxiv.org/pdf/1905.04716.pdf
5. Adaptive Traffic SIgnal Control: Exploring Reward Definition for Reinforcement Learning
   https://www.sciencedirect.com/science/article/pii/S1877050917309912
6. SUMO User Documentation:
   https://sumo.dlr.de/docs/SUMO_User_Documentation.html
7. TraCI: https://sumo.dlr.de/docs/TraCI.html
