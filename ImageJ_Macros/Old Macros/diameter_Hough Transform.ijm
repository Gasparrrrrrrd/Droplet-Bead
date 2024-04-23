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
Zstack = nSlices;
middle = Zstack/2;
dZ= getNumber("What is dZ ?", 0.5)

results = newArray(nResults);

center = newArray(nResults);

for (n = 0; n<= nResults-1; n++) {
	radius= getResult("Radius (pixels)", n);
	radius = radius*pixel_size;
	results[n] = radius;
	
	centerX = getResult("X (pixels)", n);
	centerX = centerX*pixel_size;
	centerY = getResult("Y (pixels)", n);
	centerY = centerY*pixel_size;
	
	centerZ = n*dZ + start*dZ ; ///// n * x not n??
	// Format the result as [x, y, z]
    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
	
}
joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");


close("title_copy");
run("Close");
selectWindow("Results"); 
run("Close");


print(joinedResults);
print(joinedCenter);