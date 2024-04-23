title=getTitle();
selectWindow(title);

run("Duplicate...", "title=title_copy duplicate");
selectWindow("title_copy");
run("Set Measurements...", "area center redirect=None decimal=3");


Zstack = nSlices;
middle = Zstack/2;
x = 10; // number of slices below taken

dZ= getNumber("What is dZ ?", 1)




for (i = 0 ; i <= Zstack-1; i++) {
	setSlice(i+1);
	run("Gaussian Blur...", "sigma=2 slice");
	run("8-bit");
	run("Make Binary", "calculate only black");
	run("Analyze Particles...", "size=100-Infinity circularity=0.60-1.00 display exclude include add slice");
	
}

selectWindow("Results"); 
run("Close")


amount_of_Disks_found = roiManager("size")

for (i = 0 ; i <=  amount_of_Disks_found; i++) {
	roiManager("select", i)
	run("Clear Outside", "slice");
	run("Invert", "slice");
	
	run("Analyze Particles...", "size=2-Infinity circularity=0.60-1.00 display exclude include add slice");
}

results = newArray(nResults);

center = newArray(nResults);

for (n = 0; n<= nResults-1; n++) {
	area = getResult("Area", n);
	diameter = 2*sqrt(area/PI);
	
	
	if (diameter/2 > 1) {
	
		results[n] = diameter;
	
		centerX = getResult("XM", n);
		centerY = getResult("YM", n);
		
		centerZ = Zstack*dZ/2-x*dZ + n*dZ ;
		// Format the result as [x, y, z]
	    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
		
	}
}

joinedResults = "[" + String.join(results) + "]" + "," ;
joinedCenter= String.join(center, ",\n");

run("Close");
selectWindow("Results"); 
run("Close");


print(joinedResults);
print(joinedCenter);
//List.setMeasurements 



