# Pingu-run
## Hi! So, you're interested in playing my game? Well, thanks a lot! :D

**Pingu run** was programmed in **python** using the set of modules **pygame**.
So, for running the game you may first install both python and pygame in your own PC. 
I highly recommend you to do it by first installing **anaconda** and create a virtual environment for pygame. 

For more information about anaconda, please, check its official website:

https://www.anaconda.com/

For its installation, go to:

https://www.anaconda.com/products/individual

The official anaconda documentation is available at:

https://docs.anaconda.com/

Once you have installed anaconda on your PC, you will have to create an environment for pygame.
You can do it by using the **GUI Anaconda Navigator**, which should be included with your anaconda
installation. You can also create an environment directly from **command line**. To do so, open your anaconda
prompt and run the line bellow:

`conda create --name myenv`

or

`conda create -n myenv`

Here "myenv" is the name of your environment, so, as it is meant to be for pygame let's choose a better
name for it, like "Pygame" or something like that, the idea is that you can easily remember that name.

With your pygame environment created, you can now install pygame. So, first enter to your environment, 
again, you can do it from your GUI Anaconda navigator, or directly with the command line:

`conda activate Pygame`

(Remember that "Pygame" should be replaced with the name you've chosen for your own environment)

So, once you are in your pygame environment install pygame searching the package in the GUI or with the command
line:

`pip install -U pygame --user`

We use the --user flag to tell it to install into the home directory, rather than globally.

For more information about pygame check its official website:
https://www.pygame.org/news

And for its installation you can go to:
https://www.pygame.org/wiki/GettingStarted

Now that you have installed python and created an environmet with pygame installed in it, you can play pingu run.
To do so, download all the repository files and save them in a folder, lets call it "Pingurun".
To run the game, open a prompt and look for the folder where it is saved, it should look like this:

`cd Documents/.../Pingurun`

When you're there, run the next command line:

`python runpenguin.py`

And that´s all! That line will open a window and the game will start!

There's a variety of levels in the repository, if you want to try them all you may go to the Pingurun folder and open the file "configPenguin.py".
In the 25th line of this file you should find the variable ' levelsP = "levelsFunc/"', you can change the value "levelsFunc" for any of the levels folders
available (levelsFunc, levelsFuncCB, levelsFuncSB, levelsP).

More levels will be added in the future, so please, look forward to them.

**Enjoy Pingu run! :D**
