def fitting_lsq_plotting3d_n_slice(data, bead_data, details_of_fit='yes'):


    import numpy as np
    import math
    from scipy.optimize import least_squares
    import matplotlib.pyplot as plt
    from termcolor import colored

    accepted_error = 17  ### 12% can be 0-100

    disk_radii = np.array(data[0][:])
    center_points = np.array(data[1:])

    radii = disk_radii

    dZ = points[1, 2] - points[0, 2]
    number_samples = (len(disk_radii) - 1) / 2

    # -----------------------------------------------------------------------+++++ FOR THE BEAD++++++----------------------------------------------------------------------------------------

    bead_disk_radii = np.array(bead_data[0][:])
    bead_center_points = np.array(bead_data[1:])
    bead_radii = bead_disk_radii

    center_fits = []
    radius_fits = []
    bead_center_fits = []
    bead_radius_fits = []
    lsq_errors = []
    bead_lsq_errors = []

    loop = 50
    a = 0
    while a < loop:
        # Calculate the coordinates of the point on the ring FOR DROPLET
        edge_points = center_points.copy()

        for j in range(len(edge_points)):
            angle = np.random.random() * 360  # Example angle in degrees (adjust as needed)
            edge_points[j, 0] = edge_points[j, 0] + (radii[j] * math.cos(math.radians(angle)))
            edge_points[j, 1] = edge_points[j, 1] + (radii[j] * math.sin(math.radians(angle)))

        points = edge_points.copy()

        # Calculate the coordinates of the point on the ring FOR BEAD
        bead_edge_points = bead_center_points.copy()

        for i in range(len(bead_radii)):
            bead_angle = np.random.random() * 360  # Example angle in degrees (adjust as needed)
            bead_edge_points[i, 0] = bead_edge_points[i, 0] + (bead_radii[i] * math.cos(math.radians(bead_angle)))
            bead_edge_points[i, 1] = bead_edge_points[i, 1] + (bead_radii[i] * math.sin(math.radians(bead_angle)))

        bead_points = bead_edge_points.copy()

        # Fit a sphere to the points
        (center_fit, radius_fit, lsq_error) = fit_sphere(points, center_points)
        # Fit a bead to the points
        (bead_center_fit, bead_radius_fit, bead_lsq_error) = fit_sphere(bead_points, bead_center_points)

        # print(lsq_error*100/(radius_fit) , bead_lsq_error*100/(bead_radius_fit), bead_radius_fit)
        if lsq_error * 100 / (radius_fit) < accepted_error and bead_radius_fit < bead_experiment * (
                1 + accepted_error / 100) and bead_radius_fit > bead_experiment * (1 - accepted_error / 100):
            ### bead_lsq_error*100/(bead_radius_fit) < accepted_error and
            # Store results for the droplet fitting
            center_fits.append(center_fit)
            radius_fits.append(radius_fit)
            lsq_errors.append(lsq_error)

            # Perform bead fitting and store results
            bead_center_fits.append(bead_center_fit)
            bead_radius_fits.append(bead_radius_fit)
            bead_lsq_errors.append(bead_lsq_error)

            a += 1

    mean_center_fit = np.mean(center_fits, axis=0)
    mean_bead_center_fit = np.mean(bead_center_fits, axis=0)

    mean_radius_fit = np.mean(radius_fits, axis=0)
    mean_bead_radius_fit = np.mean(bead_radius_fits, axis=0)

    lsq_error = np.mean(lsq_errors)
    bead_lsq_error = np.mean(bead_lsq_errors)

    print(mean_bead_center_fit, mean_center_fit, bead_radius_fit)

    small_r = math.sqrt(
        (mean_center_fit[0] - mean_bead_center_fit[0]) ** 2 + (mean_center_fit[1] - mean_bead_center_fit[1]) ** 2 + (
                    mean_center_fit[2] - mean_bead_center_fit[2]) ** 2)
    distance_Z = mean_bead_center_fit[2] - mean_center_fit[2]

    normalised_rn = (small_r / mean_radius_fit) * (
                mean_radius_fit / (mean_radius_fit - mean_bead_radius_fit))  ############ r/R-r

    normalised_zn = (distance_Z / mean_radius_fit) * (
                mean_radius_fit / (mean_radius_fit - mean_bead_radius_fit))  ############ Z/R-r

    print("normalised distance of bead to center (r/R)  :\n", '\033[92m' + str(normalised_rn) + '\033[0m)')

    print(" normalised Z distance of bead to center (Z/R) :\n", '\033[92m' + str(normalised_zn) + '\033[0m')

    center_fit = mean_center_fit
    radius_fit = mean_radius_fit
    bead_center_fit = mean_bead_center_fit
    bead_radius_fit = mean_bead_radius_fit

    ###################### details of fit
    if details_of_fit == "yes":
        print("Droplet fit:")
        print("------------------------------------------------------------------------------------------------")
        print("Fitted center and radius:\n", '\033[92m' + str(center_fit) + '\033[0m', ",",
              '\033[92m' + str(radius_fit) + '\033[0m')
        print("Fitted diameter:", radius_fit * 2)
        print("LSQ error:", lsq_error, "    in percent of diameter:", lsq_error * 100 / (radius_fit * 2), "%")
    if details_of_fit == "yes":
        print("Bead fit:")
        print("---------------------------------------------------------------------------------------------------")
        print("Fitted center and radius:\n", '\033[92m' + str(bead_center_fit) + '\033[0m', ",",
              '\033[92m' + str(bead_radius_fit) + '\033[0m')
        print("Fitted diameter:", bead_radius_fit * 2)
        print("LSQ error:", bead_lsq_error, "    in percent of diameter:", bead_lsq_error * 100 / (bead_radius_fit * 2),
              "%")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------+++++Plotting Slice+++++-------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def plot_sphere_slice(center, radius, Z, want_to_plot='yes'):
        from mpl_toolkits.mplot3d import Axes3D
        from ipywidgets import interact
        import numpy as np

        """
        Plot a slice of the sphere at a specific azimuth angle.

        Parameters:
            center (tuple): Tuple containing the (x, y, z) coordinates of the sphere center.
            radius (float): Radius of the sphere.
            Z (float): height  for the slice.
        """
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111)

        ### plot circle of slice imageJ
        theta = np.linspace(0, 2 * np.pi, 100)
        a = center_points[Z, 0] + radii[Z] * np.cos(theta)
        b = center_points[Z, 1] + radii[Z] * np.sin(theta)
        ax.plot(a, b, linestyle="dashed", color='r')

        # Plot points if provided
        if points is not None:
            ax.scatter(points[Z, 0], points[Z, 1], color='r', marker='x', s=80)
            ax.scatter(center_points[Z, 0], center_points[Z, 1], color='r', marker='.', s=60)
            ax.scatter(center_fit[0], center_fit[1], color='b', marker='.', s=60)

            # Plot circle representing the slice
        Zposition = Z + center_points[0, 2]
        Zc = center[2]
        radius_r = radius * math.sin(math.acos((Zposition - Zc) / radius))

        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius_r * np.cos(theta)
        y = center[1] + radius_r * np.sin(theta)
        ax.plot(x, y, color='b')

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Sphere Slice at Z= {Zstack * dZ / 2 - number_samples * dZ + Z * dZ}')

        # Set the aspect ratio of the plot to be equal and based on the sphere's radius
        ax.set_aspect('equal')
        # Set axes limits
        ax.set_xlim(center[0] - radius - 1, center[0] + radius + 1)
        ax.set_ylim(center[1] - radius - 1, center[1] + radius + 1)

        plt.grid(True)
        plt.show()

        if want_to_plot == "yes":
            interact(lambda Z: plot_sphere_slice(center_fit, radius_fit, Z), Z=(0, len(center_points) - 1, 1))
        # interact(lambda Z: plot_bead_slice(bead_center_fit, bead_radius_fit, Z),Z=(0, len(bead_center_points)-1, 1))

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------+++++Plotting Sphere+++++-------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def plot_spheres(center1, radius1, center2, radius2, points=None, azimuth=250, elevation=30, roll=150,
                     want_to_plot='yes'):

        from mpl_toolkits.mplot3d import Axes3D
        from ipywidgets import interact
        import numpy as np
        from matplotlib import cm
        """
        Plot two spheres in 3D along with optional points.

        Parameters:
            center1 (tuple): Tuple containing the (x, y, z) coordinates of the first sphere center.
            radius1 (float): Radius of the first sphere.
            center2 (tuple): Tuple containing the (x, y, z) coordinates of the second sphere center.
            radius2 (float): Radius of the second sphere.
            points (numpy.ndarray, optional): Array of shape (N, 3) containing additional points to plot.
            azimuth (float): Azimuth angle for the view.
            elevation (float): Elevation angle for the view.
            roll (float): Roll angle for the view.
        """

        distance_r = math.sqrt(
            (center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2 + (center2[2] - center1[2]) ** 2)
        print('\n')
        print('\033[92m' + "normalised distance center to bead (r/R):  " + '\033[0m' + '\033[92m' + str(
            distance_r / radius_fit) + '\033[0m')
        print('\n')

        volume_bead = bead_radius_fit ** 3
        volume_droplet = radius_fit ** 3
        print('\033[92m' + "Volume Bead to Droplet (r3/R3):  " + '\033[0m' + '\033[92m' + str(
            volume_bead / volume_droplet * 100) + "  %" + '\033[0m')
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Plot first sphere surface
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x1 = center1[0] + radius1 * np.outer(np.cos(u), np.sin(v))
        y1 = center1[1] + radius1 * np.outer(np.sin(u), np.sin(v))
        z1 = center1[2] + radius1 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x1, y1, z1, color='b', alpha=0.2)
        ax.plot_wireframe(x1, y1, z1, color='black', alpha=0.3, linewidth=1.5)

        u = np.linspace(0, 2 * np.pi, 15)
        v = np.linspace(0, np.pi, 15)
        # Plot second sphere surface with transparency
        x2 = center2[0] + radius2 * np.outer(np.cos(u), np.sin(v))
        y2 = center2[1] + radius2 * np.outer(np.sin(u), np.sin(v))
        z2 = center2[2] + radius2 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x2, y2, z2, cmap=cm.coolwarm, alpha=0.3)  # Adjust alpha for transparency
        ax.plot_wireframe(x2, y2, z2, color='black', alpha=0.3, linewidth=1)

        # # Plot points if provided
        # if points is not None:
        #     ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='r', marker='x', s=80)

        # # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.plot([center1[0], center2[0]], [center1[1], center2[1]], [center1[2], center2[2]], color='k', linestyle='--')
        ax.plot(center2[0], center2[1], center2[2], marker="X", color='orange', alpha=1, )
        ax.plot(center1[0], center1[1], center1[2], marker="X", color='blue', alpha=1, )

        ax.set_aspect('equal')
        # Rotate the plot
        ax.view_init(elev=elevation, azim=azimuth)  # Change the elevation and azimuth angles as desired

        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])

        # Rotate the plot
        ax.view_init(elev=elevation, azim=azimuth)
        ax.dist = 8  # distance

        # Roll the plot
        ax.view_init(elev=elevation, azim=azimuth)
        ax.dist = 8  # distance
        ax.azim = roll

        plt.show()

        if want_to_plot == "yes":
            # Assuming you have defined center1_fit, radius1_fit, center2_fit, radius2_fit somewhere in your code
            interact(
                lambda azimuth, elevation, roll: plot_spheres(center_fit, radius_fit, bead_center_fit, bead_radius_fit,
                                                              points, azimuth, elevation, roll),
                azimuth=(0, 360, 10),
                elevation=(-90, 90, 10),
                roll=(0, 360, 10))


    return normalised_zn, center_fit, radius_fit, bead_center_fit, bead_radius_fit