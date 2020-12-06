# Morse rover

<p align="center">
	<img src="https://raw.githubusercontent.com/Bouty92/Morse_rover/master/screenshot.png" width="600">
</p>

Dynamic simulation of a polyarticulated rover based on Blender via Morse.

[**bpy_kinematic_model.py**](bpy_kinematic_model.py) can be used as a library in order to draw 3D animated kinematics diagram with Blender 2.76 (independently from Morse).


### Usage

To import the Morse environment, execute:

`$ morse import Morse_rover/`


To be able to start the simulation from anywhere, add these lines in your bashrc:

	export MORSE_RESOURCE_PATH=~/path_to_the_directory/Morse_rover/
	export PYTHONPATH=$PYTHONPATH:~/path_to_the_directory/Morse_rover/


Finally, start the simulation with:

`$ morse run Morse_rover`
