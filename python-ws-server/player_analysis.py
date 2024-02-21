import json
import os
import glob

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

# Collect unique player names from the data
def get_unique_player_names(data):
    player_names = set()
    for event in data:
        player_name = event.get('body', {}).get('player', {}).get('name')
        if player_name:
            player_names.add(player_name)
    return list(player_names)

# Filter events by player name
def filter_events_by_player(data, player_name):
    return [event for event in data if event.get('body', {}).get('player', {}).get('name') == player_name]

# Analyze player data and generate a report
def analyze_player_data(events):
    distance_traveled = 0
    blocks_broken = 0
    blocks_placed = 0

    for event in events:
        if event['header']['eventName'] == 'PlayerTravelled':
            distance_traveled += event['body']['metersTravelled']
        elif event['header']['eventName'] == 'BlockBroken':
            blocks_broken += 1
        elif event['header']['eventName'] == 'BlockPlaced':
            blocks_placed += 1

    report = f"Player Analysis Report:\n" \
             f"Total Distance Traveled: {distance_traveled} meters\n" \
             f"Blocks Broken: {blocks_broken}\n" \
             f"Blocks Placed: {blocks_placed}\n"

    return report

def main():
    file_path = 'C:\\Users\\juedwards\\github_python'
    json_files = glob.glob(os.path.join(file_path, '*.json'))
    print("Available JSON files:")
    for idx, file in enumerate(json_files, start=1):
        print(f"{idx}. {os.path.basename(file)}")

    file_choice = int(input("Enter the number of the JSON file you'd like to analyze: ")) - 1
    if file_choice < 0 or file_choice >= len(json_files):
        print("Invalid selection.")
        return

    selected_file = json_files[file_choice]
    data = load_data(selected_file)

    player_names = get_unique_player_names(data)
    if not player_names:
        print("No player data found in the selected file.")
        return

    player_reports = []
    for player_name in player_names:
        player_events = filter_events_by_player(data, player_name)
        report = analyze_player_data(player_events)
        player_reports.append((player_name, report))

    print("Player Analysis Summary:")
    print(f"{'Player Name':<20}{'Distance Traveled':<20}{'Blocks Broken':<15}{'Blocks Placed':<15}")
    for name, report in player_reports:
        distance_traveled, blocks_broken, blocks_placed = parse_report(report)
        print(f"{name:<20}{distance_traveled:<20}{blocks_broken:<15}{blocks_placed:<15}")

def parse_report(report):
    lines = report.split('\n')
    distance_traveled = float(lines[1].split(': ')[1].split(' ')[0])
    blocks_broken = int(lines[2].split(': ')[1])
    blocks_placed = int(lines[3].split(': ')[1])
    return distance_traveled, blocks_broken, blocks_placed

if __name__ == "__main__":
    main()
