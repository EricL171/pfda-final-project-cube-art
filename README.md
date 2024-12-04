#PFDA Final Project - Cube Art

## Repository
https://github.com/EricL171/pfda-final-project-cube-art.git


## Demo
https://www.youtube.com/watch?v=pjiYErZECW8

## Description
A program for playing with 3D isometric projections of a cube and planes. This program is not complete, but the foundation is here for experimenting with 3D projection. 

"placeholder.png" and "placeholder2.png" is the title screen of the program. In the future, the start screen will be edited to be formatted more aesthetically, and the file path
should be generalized across OS filepaths. Some considerations for a future title screen could include splitting the words into separate surfaces for animating them separately,
as well as adding shadows and randomized background animations on startup.

In the future, more 3D objects should be added, as well as more ways of interacting, such as adding in rotatable circular planes, spheres, and prisms. 
Addition of differently shaped planes, such as triangular and circular planes likely can lead to interesting illusions.

Other areas to explore: perspective and distortion, other axonometric projections, locators and rotation points that can change the "center" of an object
shading of faces and shading patterns (i.e. line hatching instead of solid color faces), creating basic 3D graphics, more animation applications

The program will likely become too large and unwieldy in one file, and likely must be split into several files for all the classes that are needed. Perhaps 
consider creating a library in the future.

The structure of the game loop may need to be reorganized, due to the screen change system. There should be more considerations for the "layering" of surfaces,
as the screen constantly fills with white and may lead to confusion if a layer gets covered by the screen being filled with white. 

Adding an options menu for changing resolution, toggling fullscreen, and changing background color in the application would be helpful.
