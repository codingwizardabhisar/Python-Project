#---------------------------Double pendullum-----------------------------------------


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

# Double pendulum parameters
L1 = 1.0 # Length of line1, from the stationary point to m1
L2 = 0.5 # Length of line2, from m1 to m2
m1 = 1.0 # The first mass
m2 = 2.0 # The second mass
g = 9.81 # Gravity of course

# Initial conditions
theta1_0 = np.pi / 2.0
theta2_0 = np.pi / 2.0
omega1_0 = 0.0
omega2_0 = 0.0
y1_0 = 0.0
y2_0 = 0.0
y3_0 = 0.0

# Time range and step size
t_start = 0.0
t_end = 50.0
dt = 0.05 #Time step
t = np.arange(t_start, t_end, dt)

# Solve the double pendulum equations of motion
def double_pendulum(t, y, L1, L2, m1, m2, g):
    theta1, omega1, theta2, omega2, y1, y2, y3 = y

    # Equations of motion
    theta1_dot = omega1
    omega1_dot = (-g * (2 * m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2) - 2 *
                 np.sin(theta1 - theta2) * m2 * (omega2 ** 2 * L2 + omega1 ** 2 * L1 * np.cos(theta1 - theta2))) / \
                (L1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))

    theta2_dot = omega2
    omega2_dot = (2 * np.sin(theta1 - theta2) * (omega1 ** 2 * L1 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1) +
                                                omega2 ** 2 * L2 * m2 * np.cos(theta1 - theta2))) / \
                (L2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))

    y1_dot = 0.0  # Stationary point
    y2_dot = omega1 * np.sin(theta1) * L1 + omega2 * np.sin(theta2) * L2
    y3_dot = omega2 * np.sin(theta2) * L2

    return [theta1_dot, omega1_dot, theta2_dot, omega2_dot, y1_dot, y2_dot, y3_dot]

# Solve the initial value problem
sol = solve_ivp(double_pendulum, [t_start, t_end], [theta1_0, omega1_0, theta2_0, omega2_0, y1_0, y2_0, y3_0],
                args=(L1, L2, m1, m2, g), t_eval=t)

# Extract the solution
theta1, omega1, theta2, omega2, y1, y2, y3 = sol.y


# Convert to Cartesian coordinates
x1 = L1 * np.sin(theta1)
y1 = L1 * np.cos(theta1)
z1 = -L1 * np.sin(y1)

x2 = x1 + L2 * np.sin(theta2)
y2 = y1 + L2 * np.cos(theta2)
z2 = z1 - L2 * np.sin(y2)

# Create the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Double Pendulum Animation')

# Initialize the lines
line1, = ax.plot([], [], [], 'o-', color='blue', lw=2)  # Line for the first arm
line2, = ax.plot([], [], [], 'o-', color='green', lw=2)  # Line for the second arm
line_trace, = ax.plot([], [], [], color='red', lw=1)  # Line trace for m2

# Animation update function
def update_animation(i):
    # Update the lines
    line1.set_data([0, x1[i]], [0, y1[i]])
    line1.set_3d_properties([0, z1[i]])
    line2.set_data([x1[i], x2[i]], [y1[i], y2[i]])
    line2.set_3d_properties([z1[i], z2[i]])

    # Update the line trace for m2
    line_trace.set_data(x2[:i+1], y2[:i+1])
    line_trace.set_3d_properties(z2[:i+1])

    return line1, line2, line_trace

# Create the animation
animation = FuncAnimation(fig, update_animation, frames=len(t), interval=50, blit=True)

# Show the plot
plt.show()
