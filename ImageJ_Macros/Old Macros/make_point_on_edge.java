// Select the ROI in the ROI Manager (assuming it's already added)
run("Select", "roi=1"); // Index of the ROI in the ROI Manager

// Get the selected ROI from the ROI Manager
roiIndex = roiManager("index");

// Get the coordinates of the center and the radius of the ROI
getSelectionBounds(x, y, width, height);
roiCenterX = x + (width / 2);
roiCenterY = y + (height / 2);
roiRadius = min(width, height) / 2;

// Calculate the coordinates of the point on the ring
angle = 45; // Example angle in degrees (adjust as needed)
pointX = roiCenterX + (roiRadius * cos(toRadians(angle)));
pointY = roiCenterY + (roiRadius * sin(toRadians(angle)));

// Place a point ROI at the calculated coordinates
makePoint(pointX, pointY);

// Retrieve the coordinates of the newly placed point
roiManager("Select", roiIndex + 1); // Select the newly placed point ROI
getSelectionBounds(x, y, width, height);
newPointX = x + (width / 2);
newPointY = y + (height / 2);

// Print or use the coordinates of the newly placed point
print("Coordinates of the new point: (" + newPointX + ", " + newPointY + ")");
