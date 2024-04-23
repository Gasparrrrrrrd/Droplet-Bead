This collection of code will use arrays of Bead or Droplet fitting from ImageJ to produce an accurate 3d spherical reconstitution of the slices of ImageJ.

The FunctionsFit.py and FunctionsFitPlot.py files are storing the essential functions, the Analysis.py file takes as input an array of the shape:

[ [radius_slice1, radius_slice2,......,radius_slicen],

[centerx_slice1,centery_slice1,centerz_slice1],

[centerx_slice2,centery_slice2,centerz_slice2],


.

.

.


[centerx_slicen,centery_slicn1,centerz_slicen] ]

The results of the Analysis: the radius of the droplet, its center position can be used to reconstruct the 3d sphere it is. Same goes for the bead. 
From their center position and radius, their distance is computed. All this data is stored thanks to StoreData.py in a CSV file, stored in CSV_Data folder.

