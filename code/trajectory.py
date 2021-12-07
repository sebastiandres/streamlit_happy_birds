from matplotlib import pyplot as plt
import numpy as np

def motion(v0, theta, t, g=9.81, x0=0, y0=0):
    """
    Computes the trajectory of a projectile, given the initial velocity (v0),
    launch angle (theta), and time (t).
    """
    x = v0*np.cos(theta)*t 
    y = v0*np.sin(theta)*t - 0.5 * g * t**2
    return x, y

def get_time(v0, theta, g=9.81, x0=0, y0=0):
    """
    Computes the time of flight of a projectile, given the initial velocity (v0),
    launch angle (theta), and distance (t).
    """
    # Get the time to get back to the ground
    # y = v0*np.sin(theta)*t - 0.5 * g * t**2 -> solve for y=0, t!=0
    t_max = 2*v0*np.sin(theta)/g
    # Create a time array
    t = np.linspace(0, t_max, 100) # 0.1 is the time step
    return t

def get_trajectory(v0, theta, g=9.81, gravity_label="", x0=0, y0=0):
    """
    Computes the trajectory of a projectile, given the initial velocity (v0),
    launch angle (theta). It creates a vector with times, and from that a
    trajectory.
    """
    # Get the time to get back to the ground
    t = get_time(v0, theta, g=g, x0=x0, y0=y0)
    # Get the trajectory for the times
    x, y = motion(v0, theta, t, g=g, x0=x0, y0=y0)
    # Get a legend for the trajectory
    legend = f"$v_0$={v0}, $\\theta$={theta:.2f}, g={g} ({gravity_label})"
    # Get the color
    color_dict = {'Earth':"green", 'Moon':"gray", 'Mars':"red", 'Jupiter':"black"}
    color = color_dict[gravity_label]
    # Create a dictionary with the trajectory
    trajectory_dict = {"x": x, "y": y, "legend": legend, "color": color}
    return trajectory_dict

def fig_from_list(trajectory_list):
    """
    Plots the trajectory of a projectile, given the initial velocity (v0),
    launch angle (theta), and time (t).
    """
    fig = plt.figure()
    ax = plt.subplot(111)
    legend = []
    xmax = []
    ymax = []
    # Linestyles
    linestyles = ['-', '--', '-.', ':']
    # Iterate and plot
    for i, trajectory in enumerate(trajectory_list):
        plt.plot(trajectory["x"], trajectory["y"], 
                    color = trajectory["color"], 
                    linestyle=linestyles[i%len(linestyles)])
        legend.append(trajectory["legend"])
        xmax.append(np.max(trajectory["x"]))
        ymax.append(np.max(trajectory["y"]))
    #plt.legend(legend)
    plt.xlabel('x - horizonal distance in meters')
    plt.ylabel('y - vertical distance in meters')
    plt.suptitle('Trajectory of a projectile')
    if len(xmax) > 1:
        plt.xlim(-max(xmax)*0.05, max(xmax)*1.05)
    if len(ymax) > 1:
        plt.ylim(0, max(ymax)*1.05)

    # Resizing for the legend     
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=5)

    return fig
