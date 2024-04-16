import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

sucrose_1_3ul_zn=pd.read_csv('CSV_Data/sucrose_1_3ul_zn.csv')
sucrose_2_1ul_zn=pd.read_csv('CSV_Data/sucrose_2_1ul_zn.csv')

bead_6um_radius = pd.concat([(2*sucrose_1_3ul_zn['bead_radius_fit']),(2*sucrose_2_1ul_zn['bead_radius_fit'])])
(bead_6um_radius).plot.hist(bins=18)

# Define the parameters of the Gaussian distribution
mean = 6
cv = 0.1

# Calculate the standard deviation
std = cv * mean

# Define the Gaussian function
def gaussian(x):
    return 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-(x - mean)**2 / (2 * std**2))

# Generate the x-values
x = np.linspace(mean - 3 * std, mean + 3 * std, 1000)

# Calculate the y-values
y = gaussian(x)

# Plot the function
plt.plot(x, y)
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Gaussian Distribution with Mean=6 and CV=5%')

bead_6um_radius = np.array([bead_6um_radius.to_numpy()])
print(bead_6um_radius)
kde = gaussian_kde(bead_6um_radius)
print(kde)
# Plot the KDE
x_eval=np.arange(1,8,step=1/1000)
print(x_eval)
plt.plot(x_eval, kde(x_eval))
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Probability Density Function')


# kernel = ot.KernelSmoothing()
# estimated = kernel.build(np.array(bead_6um_radius))
# plt.plot(estimated)
plt.show()



sucrose_1ul_zn=pd.read_csv('CSV_Data/sucrose_1ul_zn.csv')
sucrose_1_8ul_zn=pd.read_csv('CSV_Data/sucrose_1_8ul_zn.csv')

bead_45um_radius = pd.concat([(2*sucrose_1_8ul_zn['bead_radius_fit']),(2*sucrose_1ul_zn['bead_radius_fit'])])
(bead_45um_radius).plot.hist(density=1, label='Fit of Bead Diameter',alpha=0.7)


# Define the parameters of the Gaussian distribution
mean = 4.5
cv = 0.1

# Calculate the standard deviation
std = cv * mean

# Define the Gaussian function
def gaussian(x):
    return 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-(x - mean)**2 / (2 * std**2))

# Generate the x-values
x = np.linspace(mean - 3 * std, mean + 3 * std, 1000)

# Calculate the y-values
y = gaussian(x)

# Plot the function
plt.plot(x, y, label='Manufacturer Bead Diameter', color='')

kde = gaussian_kde(bead_45um_radius)

# Plot the KDE
x_eval=np.arange(1,9,step=1/1000)
print(x_eval)
plt.plot(x_eval, kde(x_eval),label='PDF of Fit',color='blue')
plt.ylabel('Value')
plt.xlabel('Bead Diameter (μm)')
plt.title('Probability Density Function')
plt.gca().set_ylim(0, 1)

bead_45um_radius = np.array(bead_45um_radius.to_numpy())
print(bead_45um_radius)
plt.vlines(x=4.5, ymin=0,ymax=1, color='red', linestyles='--')

# kernel = ot.KernelSmoothing()
# estimated = kernel.build(np.array(bead_6um_radius))
# plt.plot(estimated)
plt.legend(loc='upper right')
plt.show()



sucrose_1_15ul_zn=pd.read_csv('CSV_Data/sucrose_1_15ul_zn.csv')
sucrose_2ul_zn=pd.read_csv('CSV_Data/sucrose_2ul_zn.csv')
without_sucrose_zn=pd.read_csv('CSV_Data/without_sucrose_zn.csv')

bead_10um_radius = pd.concat([(2*sucrose_1_15ul_zn['bead_radius_fit']),(2*sucrose_2ul_zn['bead_radius_fit'])])
bead_10um_radius = pd.concat([(bead_10um_radius),(2*without_sucrose_zn['bead_radius_fit'][2:])])
(bead_10um_radius).plot.hist()

# Define the parameters of the Gaussian distribution
mean = 10
cv = 0.05

# Calculate the standard deviation
std = cv * mean

# Define the Gaussian function
def gaussian(x):
    return 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-(x - mean)**2 / (2 * std**2))

# Generate the x-values
x = np.linspace(mean - 3 * std, mean + 3 * std, 1000)

# Calculate the y-values
y = gaussian(x)

# Plot the function
plt.plot(x, y)
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Gaussian Distribution with Mean=6 and CV=5%')

bead_10um_radius = np.array([bead_10um_radius.to_numpy()])
print(bead_10um_radius)
kde = gaussian_kde(bead_10um_radius)
print(kde)
# Plot the KDE
x_eval=np.arange(4,15,step=1/1000)
print(x_eval)
plt.plot(x_eval, kde(x_eval))
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Probability Density Function')


# kernel = ot.KernelSmoothing()
# estimated = kernel.build(np.array(bead_6um_radius))
# plt.plot(estimated)
plt.show()








