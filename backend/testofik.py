from visual_kinematics.RobotSerial import *
import numpy as np
from math import pi

np.set_printoptions(precision=3, suppress=True)
'''dh_params = np.array([
    [0, 0, 0, 0],           # Joint 1
    [0.05, 0, np.pi/2, 0],     # Joint 2
    [0, 0.10, 0, 0],          # Joint 3
    [0, 0.07, 0, 0],           # Joint 4
    [0, 0.04, np.pi/2, 0]      # Joint 5
])'''
dh_params = np.array([[0.163, 0., 0.5 * pi, 0.],
                          [0., 0.632, pi, 0.5 * pi],
                          [0., 0.6005, pi, 0.],
                          [0., 0.2, -0.5 * pi, -0.5 * pi],
                          [0., 0.1, 0, 0]])

dh_params = np.array([[0.163, 0., 0.5 * pi, 0.],
                          [0., 0.632, pi, 0.5 * pi],
                          [0., 0.6005, pi, 0.],
                          [0., 0.2,0, 0],
                          [0., 0.1, pi/2, 0]])

# Create the robot instance
robot = RobotSerial(dh_params)

# Define the desired end-effector position and orientation
desired_position = np.array([[0.5], [1.], [1]]) # 2D array for position (3, 1)
desired_orientation = np.array([0, 0., 0])  # Corrected to 1D array for orientation (3,)

# Use the Frame.from_euler_3 method with the correct dimensions
end = Frame.from_euler_3(desired_orientation, desired_position)  # Order matters: orientation first, then position

# Calculate inverse kinematics to find the required joint angles
joint_angles = robot.inverse(end)

# Print the resulting joint angles
print("Calculated Joint Angles:", joint_angles)
robot.show()