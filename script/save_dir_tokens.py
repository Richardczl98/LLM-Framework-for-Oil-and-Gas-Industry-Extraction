import os
import sys
import csv
from pathlib import Path


this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from lib import helper
from model import tokens, models


def find_papers(directory: str) -> list:
    """
    Find all files named 'paper.txt' recursively in the given directory.

    :param directory: The path of the directory to search in.
    :return: A list of paths to 'paper.txt' files found.
    """
    return [str(file) for file in Path(directory).rglob('paper.txt')]


def get_paper_name(txt_path):
    segments = txt_path.split('/')
    return segments[-4]


def save_paper_tokens(dir: str):
    paper_list = find_papers(dir)

    # Define the path of the CSV file where the results will be saved
    csv_file_path = Path(dir) / "papers_tokens_count.csv"

    # Open the CSV file for writing
    with csv_file_path.open(mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Paper Name', 'Number of Tokens'])

        for paper in paper_list:
            paper_name = get_paper_name(paper)
            content = helper.read_file(paper)
            no_of_tokens = tokens.count_tokens(models.MDL_GPT_4, content)

            # Write the paper name and number of tokens to the CSV file
            writer.writerow([paper_name, no_of_tokens])

    return

# Example usage:
# save_paper_tokens('/path/to/your/directory')


def main():
    save_paper_tokens(this_file_path + '/../result/')

if __name__ == "__main__":
    main()
