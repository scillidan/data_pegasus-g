# Useage
# python .py -i input.csv -o output.csv --game "Game1" "Game2" "Game3"

import csv
import re
import argparse

def filter_csv(input_file, output_file, game_strings):
    # Create a regex pattern from the game strings
    pattern = re.compile(r'|'.join(re.escape(gs) for gs in game_strings))

    # Open the input and output CSV files with utf-8 encoding
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Iterate through each row in the input file
        for row in reader:
            # Join the row to a string and check if it matches the pattern
            if any(pattern.search(cell) for cell in row):
                # Write the matching row to the output file
                writer.writerow(row)

    print(f"Filtering complete. Check '{output_file}' for results.")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Filter rows from a CSV file based on game strings.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    parser.add_argument('--game', nargs='+', required=True, help='List of game strings to filter by')

    # Parse arguments
    args = parser.parse_args()

    # Call the filter function
    filter_csv(args.input, args.output, args.game)

if __name__ == '__main__':
    main()
