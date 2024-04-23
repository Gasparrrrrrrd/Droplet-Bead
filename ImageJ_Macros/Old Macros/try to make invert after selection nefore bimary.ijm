title=getTitle();
selectWindow(title);
waitForUser("Go through slices and choose good start and end for the bead");
run("Duplicate...", "title=title_copy duplicate");
run("Duplicate...", "title=ROIonGrayImage duplicate");
run("Gaussian Blur...", "sigma=3 stack");

selectWindow("title_copy");
run("Gaussian Blur...", "sigma=3 stack");

run("Make Binary", "background=Dark calculate black");


start= getNumber("What is a good starting point ?", 2)

end= getNumber("What is a good ending point ?", nSlices-2)

run("Duplicate...", "duplicate range=start-end");

run("Fill Holes", "stack");

run("Watershed", "stack");

setOption("BlackBackground", true);

run("Erode", "stack");  //////not needed if no droplet fused

run("Find Edges", "stack");

Zstack = nSlices;
middle = Zstack/2;


dZ= getNumber("What is dZ ?", 1)

for (i = 0 ; i <= Zstack-1; i++) {
	setSlice(i+1);
	run("Analyze Particles...", "size=90-Infinity circularity=0.60-1.00 display exclude include add slice");
	
}

selectWindow("Results"); 
run("Close")



amount_of_Disks_found = roiManager("size")

for (i = 0 ; i <=  amount_of_Disks_found; i++) {
	selectWindow("ROIonGrayImage");
	
	roiManager("select", i)
	setSlice(i+start);
	
	run("Invert", "slice");
	waitForUser("Please create a selection to indicate\nthe bead location, then\nclick OK to proceed.");
	run("8-bit");
	run("Clear Outside", "slice");
	
	run("Make Binary", "calculate only ");
	run("Watershed", "stack");
	run("Erode", "stack");  //////not needed if no droplet fused
	run("Find Edges", "stack");
	run("Analyze Particles...", "size=20-Infinity circularity=0.70-1.00 display exclude include add slice");
}

selectWindow("Results"); 
run("Close");


waitForUser("what slices are first and last correct segmentation");
firstseg = getNumber("What slice is first correct segmentation?", 2)
lastseg = getNumber("What slice is last correct segmentation?", 2)

run("Duplicate...", "duplicate range=firstseg-lastseg");

run("Fill Holes", "stack");

run("Watershed", "stack");

setOption("BlackBackground", true);

run("Erode", "stack");  //////not needed if no droplet fused

run("Find Edges", "stack");
run("Hough Circle Transform","minRadius=10, maxRadius=300, inc=1, minCircles=1, maxCircles=200, threshold=0.4, resolution=300, ratio=1.0, bandwidth=20, local_radius=10,  reduce local_search show_mask results_table");

waitForUser("wait for the hough transform =)");;

results = newArray(nResults);

center = newArray(nResults);

for (n = 0; n<= nResults-1; n++) {
	radius= getResult("Radius (microns)", n);
	//radius = radius_pixels*pixel_size;
	results[n] = radius;
	
	centerX = getResult("X (microns)", n);
	//centerX = centerX_pixels*pixel_size;
	centerY = getResult("Y (microns)", n);
	//centerY = centerY_pixels*pixel_size;
	
	centerZ = n*dZ + firstseg; ///// n * x not n??
	// Format the result as [x, y, z]
    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
	
}

joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");


close("title_copy");
close("title_copy-1");
close("title_copy-2");
//run("Close");


selectWindow("Results"); 
run("Close");
selectWindow("ROI Manager"); 
run("Close");

print(joinedResults);
print(joinedCenter);