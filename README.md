# A Random Walk Simulation:

In this repository you can find a basic implementation of a random walk simulation in a 
2-dimensional space. The scenario is always the same: Our walker is bored with being 
inside, he rather goes for a stroll outside. So, the walker leaves the house and starts 
walking, without any destination in mind… and refuses to go back inside! 

You can specify for how long the walker should walk and at what pace. You’ll get 
a map of the route the walker took returned! But be aware: if you let the walker walk to
far, he might rather take a plane...


## How to use the Script
In order to use the script, you have to clone this repository to your drive and the 
following libraries need to be installed your python environment:
### Dependencies
For running:
- Python 3.7.10
- NumPy 1.20.3
- Matplotlib 3.3.4

For testing if the script is executed correctly:
- pytest 6.2.4

### Usage
To use the script, you need to navigate to the cloned repository on your machine from 
the command line. If you're in your directory and the correct python environment is 
activated, you can run the script. Therefore, you state the command `python walker.py ` 
followed by your settings. You have to specify the following settings:
````
1. The walking time
2. The number of walker who are walking at usual speed
3. The number of walker who are walking fast
4. The number of walker who are running
5. The path the outfile should be saved at
````

However, note that all settings have to be defined, so if you want to have a single 
walker, just define all the others as 0. Furthermore, a maximum of 12 walker overall are
allowed. 

As an example, you would need to state the following command to get the walking maps of 
two walker at usual speed, one fast-walking walker and a running walker if you let them 
walk over a time of 1000:

`python walker.py 1000 2 1 1 ./TheRoutesOfMyWalker.png`

The resulting image of the maps would look similar to the one below:

![image](https://github.com/hn437/random_walk/blob/main/TheRoutesOfMyWalker.png)

### And now: let them walk!
