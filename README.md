# Python-Game
This game is a group project for CIS 4930: Python Programming and COP 4360: Mobile Programming

The porting process is achieved by first adjusting the Python source code to be able to run on android. First all references to the keyword “None” had to be removed, as this is not applicable for the RAPT framework and breaks the game when it is ported to android. Next the pygame_sdl2 library needs to be imported as pygame at the top of the file (followed by an import of pygame). This allows the app to use sdl2 libraries when applicable and fills in the gaps with pygame logic (as stated earlier this allows graphics to be rendered on the Android platform). Next, a configuration file is created using RAPT for each individual app. This process even includes the creation of a key to be used for the play store. Various settings are specified including that the app should all be stored on local storage (as opposed to external), and that the app should lock the phone in landscape mode. Finally RAPT is used to create an APK which is automatically loaded onto a connected device and run. RAPT includes adb utilities to allow debugging of APKs

The steps to load an APK of cubism on your phone are as follows.

Gather all the Prerequisite Software, including:

Python 2.7 (Source: https://www.python.org/)

	With libraries including but not limited to Cython, PySDL2, Pygame
  
	These can all be retrieved using apt-get and pip
  
pygame_sdl2 library (Source: https://github.com/renpy/pygame_sdl2)

	Download the dependencies:
  
	(on ubuntu)
  
	sudo apt-get install build-essential python-dev libsdl2-dev
  
	sudo apt-get install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
  
	sudo apt-get install libjpeg-dev libpng12-dev virtualenvwrapper
  
	Must be downloaded using this github link: https://github.com/renpy/pygame_sdl2
  
	Example Command: git clone "https://github.com/renpy/pygame_sdl2.git"
  
	Install by runing python setup.py install
  
	You can tell if this has been successful by attempting to run "import pygame_sdl2" in the python shell
  
RAPT (Source: https://github.com/renpytom/rapt-pygame-example)

	Download the rapt file from this URL: http://nightly.renpy.org/current/
  
	Title ends in "...rapt.zip"
  
	Extract this into a directory where it can reside as a utility (I put ours in my Python directory)
  
	Install the SDK by running, in the RAPT directory, python android.py installsdk
  
		We have encountered errors with some devices with it being unable to detect the Java SDK
    
Configure the APK preferences using the RAPT utility (Source: as above):

	Run the command, in the RAPT directory, as follows:
  
		python android.py configure /path/to/cubism/
    
	This will open up an interactive dialog which you can use to specify:
  
		The name of the application
    
		The name that appears under the icon
    
		The package name
    
	 	Readable and Version Code
    
		Orientation: Cubism uses landscape
    
		Expansion APK: No
    
		Android Version: Android 4.0
    
		Application Layout: Single directory, device internal storage
    
		Include Source Code: no
    
		Permissions: VIBRATE
    
		SQlite3: no
    
    PIL: no
    
	This will create an .android.json file with the specifications for the application in the application's directory.

Modify the source code to make it compatible with your devcie:

	In its current state, Cubism is hard coded to a 2k resolution device -- characteristic of the S7 line of products. To adjust this change the WINX and WINY constants to be appropriate for your device in the source code. 

Create the APK and load it onto your phone (Source: as above):

	Firstly, make sure your phone is plugged into the computer, and that drivers (if needed) are installed.
  
	RAPT will handle all of the work for both compiling the APK and loading it onto the phone as an application with the following command, executed from the RAPT folder:
  
	python android.py --launch build /path/to/cubism release install
  
This will launch Cubism on your phone. It will be installed and available in your applications menu for future use.
