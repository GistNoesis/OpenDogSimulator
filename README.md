# OpenDogSimulator
Simulation for the Open Dog project

OpenDog project CAD based on :
https://github.com/XRobots/openDog

Flying openDog video :

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ocgPrY2Uf6A/0.jpg)](https://www.youtube.com/watch?v=ocgPrY2Uf6A)

Install :

- You'll need pybullet
- Then you can play and try make the robot walk.

License :

- Code is MIT
- STL files are derivatives of GPL V3 so inherit

Notes : 

- Due to the manual import and joint positionning it's not accurate for the moment.
- The masses and inertial matrices are not correct
- The model currently work with self_collisions, but if I had the rings of the body it is self colliding when it shouldn't, probably some pybullet optimization to the convex hull make it self collide
- The mirrored version of the leg have been done manually.


How to manually create a new URDF for updated versions : 


From the STP file : 


- Group the parts that belong to the same link into a single stl.

- Then manually edit the joint position and orientation, inside the urdf file.


Ideally one would have used solidworks to create a urdf file during the export :
http://wiki.ros.org/sw_urdf_exporter/Tutorials

Alternatively from fusion 360 :

We should be able to do Fusion 360 -> SDF using https://github.com/Roboy/SDFusion

Then SDF -> URDF using sdf2urdf.py of https://github.com/andreasBihlmaier/pysdf
