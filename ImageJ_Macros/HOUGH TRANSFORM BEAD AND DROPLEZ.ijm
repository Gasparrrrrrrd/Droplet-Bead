title=getTitle();
selectWindow(title);
run("Duplicate...", "title=title_copy duplicate");
selectWindow("title_copy");


run("Gaussian Blur...", "sigma=3 stack");

run("Make Binary", "background=Dark calculate black");

waitForUser("Go through slices and choose good start and end");
start= getNumber("What is a good starting point ?", 2)

end= getNumber("What is a good ending point ?", nSlices-2)

run("Duplicate...", "duplicate range=start-end");

run("Fill Holes", "stack");

run("Watershed", "stack");

setOption("BlackBackground", true);

run("Erode", "stack");  //////not needed if no droplet fused
run("Erode", "stack");  //////not needed if no droplet fused
run("Erode", "stack");  //////not needed if no droplet fused
run("Erode", "stack");  //////not needed if no droplet fused
run("Erode", "stack");  //////not needed if no droplet fused

run("Find Edges", "stack");

// run("Find Edges", "stack");

run("Hough Circle Transform","minRadius=20, maxRadius=300, inc=1, minCircles=1, maxCircles=200, threshold=0.35, resolution=300, ratio=10.0, bandwidth=20, local_radius=10,  reduce local_search show_mask results_table");

image_size = 81.92 /// micron from settings
image_pixel_size = 512
pixel_size = image_size/image_pixel_size
dZ= getNumber("What is dZ ?", 0.5)

results = newArray(nResults);

center = newArray(nResults);

for (n = 0; n<= nResults-1; n++) {
	radius= getResult("Radius (microns)", n);
	//radius = radius*pixel_size;
	results[n] = radius;
	
	centerX = getResult("X (microns)", n);
	//centerX = centerX*pixel_size;
	centerY = getResult("Y (microns)", n);
	//centerY = centerY*pixel_size;
	
	centerZ = n*dZ + start*dZ ; ///// n * x not n??
	// Format the result as [x, y, z]
    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
	
}
joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");


close("title_copy");
run("Close");



print(joinedResults);
print(joinedCenter);


selectWindow(title);
run("Duplicate...", "title=title_copy_bead duplicate");
selectWindow("title_copy_bead");

image_size = 81.92 /// micron from settings
image_pixel_size = 512
pixel_size = image_size/image_pixel_size

run("Gaussian Blur...", "sigma=3 stack");

run("Make Binary", "background=Dark calculate black");

run("Duplicate...", "duplicate range=start-end");

run("Fill Holes", "stack");

run("Watershed", "stack");

setOption("BlackBackground", true);

run("Erode", "stack");  //////not needed if no droplet fused

run("Find Edges", "stack");

selectWindow("title_copy_bead-1")
Zstack = nSlices;
middle = Zstack/2;

for (i = 0 ; i <= Zstack-1; i++) {
	setSlice(i+1);
	run("Analyze Particles...", "size=80-Infinity pixel circularity=0.75-1.00 display include add slice");
	
}

selectWindow("Results"); 
run("Close")



amount_of_Disks_found = roiManager("size")

for (i = 0 ; i <  amount_of_Disks_found; i++) {
	selectWindow("title_copy_bead");
	
	roiManager("select", i)
	setSlice(i+start);
	run("Clear Outside", "slice");
	run("Invert", "slice");
	
	run("Analyze Particles...", "size=10-Infinity pixel circularity=0.60-1.00 display exclude include add slice");
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
run("Erode", "stack");  //////not needed if no droplet fused
run("Erode", "stack");  //////not needed if no droplet fused


run("Find Edges", "stack");
run("Hough Circle Transform","minRadius=5, maxRadius=300, inc=1, minCircles=1, maxCircles=200, threshold=0.4, resolution=300, ratio=1.0, bandwidth=20, local_radius=10,  reduce local_search show_mask results_table");
waitForUser("wait for the hough transform =)");

results = newArray(nResults);

center = newArray(nResults);

for (n = 0; n<= nResults-1; n++) {
	radius= getResult("Radius (microns)", n);
	//radius= getResult("Radius (pixels)", n);
	//radius = radius*pixel_size;  // THIS ONLY IF PIXEL
	results[n] = radius;
	
	centerX = getResult("X (microns)", n);
	//centerX = getResult("X (pixels)", n);
	//centerX = centerX*pixel_size;
	centerY = getResult("Y (microns)", n);
	//centerY = getResult("Y (pixels)", n);
	//centerY = centerY*pixel_size;
	
	centerZ = n*dZ + firstseg*dZ ; ///// n * x not n??
	// Format the result as [x, y, z]
    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
	
}

joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");


//close("title_copy");
//close("title_copy-1");
//close("title_copy-2");
//run("Close");


selectWindow("Results"); 
run("Close");
selectWindow("ROI Manager"); 
run("Close");

print(joinedResults);
print(joinedCenter);


