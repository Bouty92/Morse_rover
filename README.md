# Morse_rover

Dynamic simulation of a polyarticulated rover based on Blender via Morse.
bpy_kinematic_model.py can be used as a library in order to draw 3D animated kinematics diagram with Blender.

Execute:

`$ morse import Morse_rover/`

to import the Morse environment.

Add:

<pre><code>export MORSE_RESOURCE_PATH=~/*path_to_the_directory*/Morse_rover/
export PYTHONPATH=$PYTHONPATH:~/*path_to_the_directory*/Morse_rover/</code></pre>

to your bashrc if you want to be able to launch the simulation from anywhere.

Finally, launch the simulation with:

`$ morse run Morse_rover`
