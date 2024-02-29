import json
import os
import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the JSON data from the file
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line}\nError: {e}")
    return data

# Plot the 3D chart of player journeys
def plot_player_journeys(data):
    player_paths = {}
    for entry in data:
        # Check if 'player' key exists in 'body'
        if 'player' in entry.get('body', {}):
            player_id = entry['body']['player']['name']
            x = entry['body']['player']['position']['x']
            y = entry['body']['player']['position']['y']
            z = entry['body']['player']['position']['z']
            if player_id not in player_paths:
                player_paths[player_id] = {'x': [], 'y': [], 'z': []}
            player_paths[player_id]['x'].append(x)
            player_paths[player_id]['y'].append(y)
            player_paths[player_id]['z'].append(z)
        else:
            # Optionally, print a warning or handle entries without 'player' differently
            print(f"Warning: 'player' key not found in entry: {entry}")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for player_id, coords in player_paths.items():
        ax.plot(coords['x'], coords['z'], coords['y'], marker='o', linestyle='-', label=player_id)

    ax.set_title('Player Journeys in 3D Space')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Z Coordinate')
    ax.set_zlabel('Y Coordinate')
    ax.legend()


# Generate and display the player analysis report
def display_player_analysis(data):
    player_reports = {}
    for event in data:
        player_name = event.get('body', {}).get('player', {}).get('name')
        if player_name:
            if player_name not in player_reports:
                player_reports[player_name] = {'distance_traveled': 0, 'blocks_broken': 0, 'blocks_placed': 0}
            if event['header']['eventName'] == 'PlayerTravelled':
                player_reports[player_name]['distance_traveled'] += event['body']['metersTravelled']
            elif event['header']['eventName'] == 'BlockBroken':
                player_reports[player_name]['blocks_broken'] += 1
            elif event['header']['eventName'] == 'BlockPlaced':
                player_reports[player_name]['blocks_placed'] += 1

    print(f"{'Player Name':<20}{'Distance Traveled':<20}{'Blocks Broken':<15}{'Blocks Placed':<15}")
    for name, report in player_reports.items():
        print(f"{name:<20}{report['distance_traveled']:<20}{report['blocks_broken']:<15}{report['blocks_placed']:<15}")

def main():
    file_path = 'C:\\Users\\juedwards\\github_python\\2102240011.json'
    data = load_data(file_path)
    display_player_analysis(data)  # Display the player analysis report in the console
    plot_player_journeys(data)
    plt.show()  # Show the 3D plot

    

if __name__ == "__main__":
    main()
