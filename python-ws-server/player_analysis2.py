import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load and parse the JSON data
data = []
with open('C:\\Users\\juedwards\\github_python\\2102240011.json', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Initialize a dictionary to store coordinates by player
player_paths = {}

# Iterate over the data to fill player_paths
for entry in data:
    player_id = entry['body']['player']['name']  # Adjust based on actual data structure
    x = entry['body']['player']['position']['x']
    y = entry['body']['player']['position']['y']  # Ensure 'y' coordinate is being accessed correctly
    z = entry['body']['player']['position']['z']
    if player_id not in player_paths:
        player_paths[player_id] = {'x': [], 'y': [], 'z': []}
    player_paths[player_id]['x'].append(x)
    player_paths[player_id]['y'].append(y)
    player_paths[player_id]['z'].append(z)

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for player_id, coords in player_paths.items():
    ax.plot(coords['x'], coords['z'], coords['y'], marker='o', linestyle='-', label=player_id)  # Note the order of coordinates

ax.set_title('Player Journeys in 3D Space')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Z Coordinate')
ax.set_zlabel('Y Coordinate')  # Y coordinate is along the vertical axis in this plot
ax.legend()
plt.show()
