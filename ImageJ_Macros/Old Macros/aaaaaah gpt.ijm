// Get the title of the active image
title = getTitle();

// Duplicate the image to work on a copy
run("Duplicate...", "title=title_copy duplicate");
selectWindow("title_copy");

// Set the measurements to include area and center of mass
run("Set Measurements...", "area center redirect=None decimal=3");

// Get the number of slices in the Z-stack
Zstack = nSlices;
middle = Zstack / 2;

// Define the number of slices below to be considered
x = middle;

// Prompt the user for the spacing between slices
dZ = getNumber("What is dZ ?", 1);

// Iterate over each slice in the Z-stack
for (i = 0; i < Zstack; i++) {
    setSlice(i + 1);
    
    // Apply Gaussian Blur to enhance particle detection
    run("Gaussian Blur...", "sigma=2 slice");
    
    // Convert to 8-bit image
    run("8-bit");
    
    // Make the image binary, focusing on black areas
    run("Make Binary", "calculate only black");
    
    // Analyze particles in the current slice
    run("Analyze Particles...", "size=100-Infinity circularity=0.60-1.00 display exclude include add slice");
}

// Close the Results window to avoid confusion
selectWindow("Results"); 
run("Close");

// Get the number of disks found using ROI manager
amount_of_Disks_found = roiManager("size");

// Iterate over each detected disk
for (i = 0; i < amount_of_Disks_found; i++) {
    // Select each ROI one by one
    roiManager("select", i);
    
    // Clear everything outside the selected ROI
    run("Clear Outside", "slice");
    
    // Invert the selection to focus on the black hole
    run("Invert", "slice");
    
    // Analyze the black hole area
    run("Analyze Particles...", "size=2-Infinity circularity=0.60-1.00 display exclude include add slice");
}

// Initialize arrays to store results
results = newArray(amount_of_Disks_found);
center = newArray(amount_of_Disks_found);

// Iterate over the results of particle analysis
for (n = 0; n < amount_of_Disks_found; n++) {
    area = getResult("Area", n);
    diameter = 2 * sqrt(area / PI);
    
    // Check if the diameter is greater than 1 (to filter out noise)
    if (diameter / 2 > 1) {
        results[n] = diameter;
        
        // Get the center coordinates of the detected particle
        centerX = getResult("XM", n);
        centerY = getResult("YM", n);
        
        // Calculate the Z-coordinate based on slice number and slice spacing
        centerZ = middle * dZ - x * dZ + n * dZ;
        
        // Format the result as [x, y, z]
        center[n] = "[" + centerX + ", " + centerY + ", " + centerZ + "]";
    }
}

// Join the results into strings
joinedResults = "[" + String.join(results) + "]" + ",";
joinedCenter = String.join(center, ",\n");

// Close the Results window to avoid confusion
run("Close");
selectWindow("Results"); 
run("Close");

// Print the results
print(joinedResults);
print(joinedCenter);
