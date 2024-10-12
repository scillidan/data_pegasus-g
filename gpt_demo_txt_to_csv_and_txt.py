import os
import csv
import sys

def process_metadata(input_file):
    games = []
    current_game = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("game:"):
                if current_game:
                    games.append(current_game)
                    current_game = {}
                current_game['game'] = line.split(":", 1)[1].strip()
            elif line.startswith("file:"):
                current_game['file'] = line.split(":", 1)[1].strip()
            elif line.startswith("sort-by:"):
                current_game['sort-by'] = line.split(":", 1)[1].strip()
            elif line.startswith("developer:"):
                current_game['developer'] = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                current_game['description'] = line.split(":", 1)[1].strip().replace('\\n', '\n')
        
        # Append the last game if exists
        if current_game:
            games.append(current_game)

    return games

def write_csv(games, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['collection', 'game', 'file', 'sort-by', 'developer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for game in games:
            writer.writerow({
                'collection': 'DC',  # Adjust this as needed
                'game': game.get('game', ''),
                'file': game.get('file', ''),
                'sort-by': game.get('sort-by', ''),
                'developer': game.get('developer', '')
            })

def write_descriptions(games, output_dir):
    for game in games:
        if 'game' in game and 'description' in game:
            filename = os.path.join(output_dir, f"{game['game']}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(game['description'])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cli.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    games = process_metadata(input_file)
    
    # Write the CSV and descriptions to the specified output directory
    write_csv(games, os.path.join(output_dir, 'output.csv'))
    write_descriptions(games, output_dir)

    print(f"CSV and text files have been created in {output_dir}.")
