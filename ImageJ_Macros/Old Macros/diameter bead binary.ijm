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
	selectWindow("title_copy");
	
	roiManager("select", i)
	setSlice(i+start);
	run("Clear Outside", "slice");
	run("Invert", "slice");
	
	run("Analyze Particles...", "size=10-Infinity circularity=0.60-1.00 display exclude include add slice");
}
results = newArray(nResults);

center = newArray(nResults);

waitForUser("what slice is first correct segmentation");
firstseg = getNumber("What slice is first correct segmentation?", 2)
for (n = 0; n<= nResults-1; n++) {
	area = getResult("Area", n);
	diameter = 2*sqrt(area/PI);
	
	
	if (diameter/2 > 1) {
	
		results[n] = diameter;
	
		centerX = getResult("XM", n);
		centerY = getResult("YM", n);
		
		
		centerZ = n*dZ + firstseg ;
		// Format the result as [x, y, z]
	    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
		
	}
}

joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");

close("title_copy-1");
selectWindow("Results"); 
run("Close");


print(joinedResults);
print(joinedCenter);