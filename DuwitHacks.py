from numpy import sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def empty(item):
    if item == '': return False
    else: return True

def sort_data():

    dataSet = []
    latLst = []
    longLst = []

    file = open('DuwitHacks Hackathon/GSFC.glb.200204_202410_RL06v2.0_OBP-ICE6GD/Mascon_placement_file_gen6.txt', 'r')
    allLines = file.readlines() # All the lines in the file

    numOfPoints = 41168 # (All data points)
    for n in range(14, 14 + numOfPoints): # Make dataset for the first howevermany lines
        line = allLines[n].split(' ') # Find the string line
        dataValues = [float(i) for i in list(filter(empty, line))] # Make string a list of floats
        data = { # Make dictionary for this line
            'Position Latitude': dataValues[0],
            'Position Longitude': dataValues[1],
            'Width Latitude': dataValues[2],
            'Width Longitude': dataValues[3]
        }
        dataSet.append(data) # Add data to the dataset
    file.close()

    # Make list for longitudes, latitudes and relative mass
    latLst = [data['Position Latitude'] for data in dataSet]
    longLst = [data['Position Longitude'] for data in dataSet]
    mass = [pi * data['Width Latitude'] * data['Width Longitude'] for data in dataSet]

    return latLst, longLst, mass

def plotting(latLst, longLst, mass):

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_aspect("equal")

    # Plot datapoints
    x = [cos(lat) * cos (long) for lat, long in zip(latLst, longLst)]
    y = [cos(lat) * sin (long) for lat, long in zip(latLst, longLst)]
    z = [sin(lat) for lat in latLst]
    plot = ax.scatter(x, y, z, s = mass, c = mass, marker = '.', norm = 'log')

    def update(frame): # Spin animation
        ax.view_init(elev = 20, azim = frame)
    anim = animation.FuncAnimation(fig, update, frames = range(360), interval = 200)

    colourBar = fig.colorbar(plot)
    colourBar.set_label('Relative size of mascons represeted logarithmically',loc = 'center', rotation = 270)

    ax.text2D(-0.25, 1, 'The colour and size of each point is representative\nof the size of the respective mascon.\n\nThe colour is logarithmic whilst the size is not.', transform = ax.transAxes)
    plt.show()

latLst, longLst, mass = sort_data()
plotting(latLst, longLst, mass)