# OpenDogSimulator
Simulation for the Open Dog project

Flying openDog video :

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ocgPrY2Uf6A/0.jpg)](https://www.youtube.com/watch?v=ocgPrY2Uf6A)

Install :

You'll need pybullet
Then you can play and try make the robot walk.


How to manually create a new URDF for updated versions : 
From the STP file : 
-group the parts that belong to the same link into a single stl.
-Then manually edit the joint position and orientation, inside the urdf file.

Ideally one would have used solidworks to create a urdf file during the export.
http://wiki.ros.org/sw_urdf_exporter/Tutorials

Alternatively from fusion 360 :
We should be able to do Fusion 360 -> SDF using https://github.com/Roboy/SDFusion
Then SDF -> URDF using sdf2urdf.py of https://github.com/andreasBihlmaier/pysdf
