# 3d-slicer
Interative slicer for 3D numpy arrays with visualization 

Compatible with:
* pygame 1.9.6
* numpy 1.18.5
* OpenCV2 4.2.0

# Commands:
* Left Click: Select a point on the image shown
* Right Click: Reset all selected points on the image shown
* Mouse Scroll: Change the visualized slice (first dimension of the array)
  * Press shift + mouse scroll: Change the visualized slice with step 10
* Q: Shift the visualization axis to the right [ Example: ```img.shape``` == (3,4,5) => (4,5,3) ]
* R: Shift the visualization axis to the left  [ Example: ```img.shape``` == (3,4,5) => (5,3,4) ]
* W: For all axis, transform all selected points into a rectangle
* S: Export the selected parallelepiped into ```save_path``` directory

Good luck, have fun 😉