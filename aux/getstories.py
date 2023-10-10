import os
import json

# Define the path to the stories directory
stories_dir = os.path.join(os.getcwd(), 'data/collected', 'stories')

# Define the path to the output file
output_file = os.path.join(os.getcwd(), 'output.txt')

# Open the output file in write mode
with open(output_file, 'w') as f:
    # Iterate over all the JSON files in the stories directory
    for filename in os.listdir(stories_dir):
        if filename.endswith('.json'):
            # Open the JSON file
            with open(os.path.join(stories_dir, filename), 'r') as json_file:
                # Load the JSON data
                data = json.load(json_file)
                # Write the title and content to the output file and ignore any kind of HTML tags
                f.write(data['title'] + '\n')
                f.write(data['content_raw'] + '\n')
                f.write('\n')
