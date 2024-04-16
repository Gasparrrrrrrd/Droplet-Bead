
def sphere_residuals(params, points):
    """Compute residuals for sphere fitting, used for error"""
    x0, y0, z0, r = params
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    return (x - x0)**2 + (y - y0)**2 + (z - z0)**2 - r**2

def fit_sphere(points,center_points):
    """Fit a sphere to the given points using least squares."""
    # Initial guess: center as mean of points, radius as average distance from center
    center_initial = np.mean(center_points, axis=0)
    #print("initial guess center",center_initial)
    radius_initial = np.mean(np.linalg.norm(points - center_initial, axis=1))
    #print("initial guess radius",radius_initial)
    # center_initial = [1,1,1]
    # radius_initial = 1

    # Perform least squares fitting
    ### sphere_Residuals is called, with params= [center_initial[0], center_initial[1], center_initial[2], radius_initial], and points are in args=(points)
    result = least_squares(sphere_residuals, [center_initial[0], center_initial[1], center_initial[2], radius_initial], args=(points,))

    # Extract fitted parameters
    x0, y0, z0, r = result.x


#------------------- OPTIONAL -------------------#
# Calculate LSQ error
    # array_of_d = sphere_residuals(result.x, center_points) + r**2 - (center_points[:, 2] - z0)**2 ###### rdius and z position are unimporrtant, we look at 2d fit because thats our deal
    array_of_d = (center_points[:, 0] - x0)**2 + (center_points[:, 1] - y0)**2  #### centerx ImageJ - xfit ^2

    lsq_error = np.mean( np.sqrt((array_of_d)))

    Zhere= np.arange(0, len(points))
    plt.plot(Zstack*dZ/2-number_samples*dZ + Zhere*dZ,array_of_d)
    plt.ylim(0,1)
    return (x0, y0, z0), r, lsq_error




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------+++++ FOR THE BEAD++++++----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sphere_residuals_bead(params, points):
    """Compute residuals for sphere fitting, used for error"""
    bead_x0, bead_y0, bead_z0, bead_r = params
    bead_x, bead_y, bead_z = points[:, 0], points[:, 1], points[:, 2]
    return (bead_x - bead_x0)**2 + (bead_y - bead_y0)**2 + (bead_z - bead_z0)**2 - bead_r**2

def fit_sphere_bead(points,center_points):
    """Fit a sphere to the given points using least squares."""
    # Initial guess: center as mean of points, radius as average distance from center
    bead_center_initial = np.mean(center_points, axis=0)
    #print("\n")
    #print("initial guess center",bead_center_initial)
    bead_radius_initial = np.mean(np.linalg.norm(points - bead_center_initial, axis=1))
    #print("initial guess radius",bead_radius_initial)

    # Perform least squares fitting
    ### sphere_Residuals is called, with params= [center_initial[0], center_initial[1], center_initial[2], radius_initial], and points are in args=(points)
    bead_result = least_squares(sphere_residuals, [bead_center_initial[0], bead_center_initial[1], bead_center_initial[2], bead_radius_initial], args=(points,))

    # Extract fitted parameters
    bead_x0, bead_y0, bead_z0, bead_r = bead_result.x


#------------------- OPTIONAL -------------------#
# Calculate LSQ error
    #bead_array_of_d = sphere_residuals(bead_result.x, center_points) + bead_r**2 - (center_points[:, 2] - z0)**2 ###### rdius and z position are unimporrtant, we look at 2d fit because thats our deal
    bead_array_of_d = (center_points[:, 0] - bead_x0)**2 + (center_points[:, 1] - bead_y0)**2  #### centerx ImageJ - xfit ^2

    bead_lsq_error = np.mean(np.sqrt((bead_array_of_d)))

    bead_Zhere= np.arange(0, len(points))
    plt.plot(Zstack*dZ/2-number_samples*dZ + bead_Zhere*dZ,bead_array_of_d)

    return (bead_x0, bead_y0, bead_z0), bead_r, bead_lsq_error



