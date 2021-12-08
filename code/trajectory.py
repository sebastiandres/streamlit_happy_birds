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

def fig_from_list(trajectory_list, pig_position=[]):
    """
    Plots the trajectory of a projectile, given the initial velocity (v0),
    launch angle (theta), and time (t).
    """
    fig = plt.figure()
    ax = plt.subplot(111)
    legend = []
    xmax_list = []
    # Linestyles
    linestyles = ['-', '--', '-.', ':']
    # Iterate and plot
    for i, trajectory in enumerate(trajectory_list):
        plt.plot(trajectory["x"], trajectory["y"], 
                    color = trajectory["color"], 
                    linestyle=linestyles[i%len(linestyles)])
        legend.append(trajectory["legend"])
        xmax_list.append(np.max(trajectory["x"]))
    plt.xlabel('x - horizonal distance in meters')
    plt.ylabel('y - vertical distance in meters')
    plt.suptitle('Trajectory of a projectile')

    # Adding the pig
    if len(pig_position) > 0:
        ax.plot(pig_position[0], pig_position[1], marker='$\U0001F437$', ms=20)
        xmax_list.append(pig_position[0])

    # xmax_list and ymax calculations
    if len(xmax_list) > 1:
        xmax = max(xmax_list)
        plt.xlim(-xmax*0.05, xmax*1.05)
        plt.ylim(-xmax*0.05, xmax*1.05) # Same limits for x and y

    # Resizing for the legend     
    #plt.legend(legend)
    """
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=5)

    """
    return fig

def check_solution(pig_position, trajectory_list):
    """
    Checks if the pig is in the trajectory of the projectile.
    """
    x_tol, y_tol = 1.0, 1.0
    print("pig_position:", pig_position)
    # Iterate and check
    for trajectory in trajectory_list:
        x = trajectory["x"][-1]
        y = trajectory["y"][-1]
        print(f"x={x}, y={y}")
        if abs(pig_position[0] - x) < x_tol and abs(pig_position[1] - y) < y_tol:
            return True
    return False