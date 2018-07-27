<h1>What is this???</h1>
This project is the software for a microtonal synth which combines an array of buttons connected to two arduino boards which communicate with a python program. It is based off pianoputer but nearly all of its original code has been changed.
<h2>Dependencies</h2>
In order to get this program working you need:
<ul>
	<li>Python 3</li>
	<li>PyGame</li>
	<li>PySerial</li>
</ul>
However, there is a virtual environment included which includes the required packages.
<h2>How to run this thing</h2>
<p>
Open "main.py" in a text editor and change the "serialinterfaces" variable to the ports of your two arduino boards. Then open "arduinoboard" in the Arduino IDE and upload the code to each arduino with one board having the board number set to 0 and the other set to 1 and how many buttons are connected to each. Connect the buttons to the digital pins starting at pin 2. Then if everything has been properly configured, when you run "main.py" it should register each note and assign a button to each and open PyGame and notes should play when you push the buttons.</p>
<br>
<p>The oldfiles folder contains backups of old revisions and experimentation as I converted pianoputer to microtonal and connected the arduinos to python.</p>
