import os
import json
import spacy

# Define the path to the stories directory
stories_dir = os.path.join(os.getcwd(), '../data/collected', 'stories')

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
                nlp = spacy.load('en_core_web_lg') 
                
                stop_words = spacy.lang.en.stop_words.STOP_WORDS 

                doc_title = nlp(data['title'])

                filtered_tokens = [token for token in doc_title if not token.is_stop and not token.is_punct and not token.is_digit and not token.is_quote] 

                f.write(' '.join([token.text for token in filtered_tokens]) + '\n')

                doc_content = nlp(data['content_raw'])

                filtered_tokens = [token for token in doc_content if not token.is_stop]

                f.write(' '.join([token.text for token in filtered_tokens]) + '\n')
 
