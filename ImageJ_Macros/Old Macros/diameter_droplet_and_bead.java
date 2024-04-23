title=getTitle();
selectWindow(title);

run("Duplicate...", "title=title_copy duplicate");
selectWindow("title_copy");
run("Set Measurements...", "area center redirect=None decimal=3");


Zstack = nSlices;
middle = Zstack/2;
x = 14; // number of slices below (and up total 6) taken

dZ= getNumber("What is dZ ?", 1)


for (i = middle - x; i <= middle + x; i++) {
	setSlice(i);
	run("Gaussian Blur...", "sigma=2 slice");
	setAutoThreshold("Default dark");
	run("Analyze Particles...", "size=100-Infinity circularity=0.60-1.00 display exclude include add slice");
	
}


setSlice(middle)

results = newArray(2*x+1);

center = newArray(2*x+1);

for (n = 0; n<= 2*x; n++) {
	area = getResult("Area", n);
	diameter = 2*sqrt(area/PI);
	results[n] = diameter;
	
	centerX = getResult("XM", n);
	centerY = getResult("YM", n);
	
	centerZ = Zstack*dZ/2-x*dZ + n*dZ ;
	// Format the result as [x, y, z]
    center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
	
}
joinedResults = String.join(results);
joinedCenter= String.join(center, ",\n");

selectWindow("Results"); 
run("Close");





//List.setMeasurements 

