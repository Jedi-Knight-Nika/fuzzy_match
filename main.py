import pandas as pd
import json
import time
from fuzzywuzzy import process
from typing import List, Dict, Any

def fuzzy_match(data: List[Dict[str, Any]], 
                data_column: str, 
                reference_data: List[Dict[str, Any]], 
                reference_column: str, 
                id_column: str, 
                score_threshold: int = 80) -> pd.DataFrame:
    """
    Perform fuzzy matching and return matches with scores above the threshold.

    Args:
    - data: List of dictionaries (your data).
    - data_column: The key in your data dicts for the text to match.
    - reference_data: List of dictionaries (your reference data).
    - reference_column: The key in your reference data dicts containing the text to match against.
    - id_column: The key in your reference data dicts for the identifier.
    - score_threshold: The minimum score for a match to be considered valid.

    Returns:
    - DataFrame with matches and their scores.
    """
    results = []
    for item in data:
        text_to_match = item.get(data_column)
        if not text_to_match:
            continue

        best_match, score = process.extractOne(text_to_match, [ref[reference_column] for ref in reference_data])

        if score >= score_threshold:
            matched_id = next((ref[id_column] for ref in reference_data if ref[reference_column] == best_match), None)
            results.append({data_column: text_to_match, 'Matched ID': matched_id, 'Match Score': score})

    return pd.DataFrame(results)

def main():
    start_time = time.time()
    print("Start process...")
    
    with open('path/to/your/data.json') as file:
        data = json.load(file)

    with open('path/to/your/reference_data.json') as file:
        reference_data = json.load(file)

    matched_results = fuzzy_match(data=data, 
                                  data_column='description', 
                                  reference_data=reference_data, 
                                  reference_column='title', 
                                  id_column='id')


    unique_matched_results = matched_results.drop_duplicates(subset=['id', 'title'])

    print(unique_matched_results)
    unique_matched_results.to_excel('path/to/your/result.xlsx', index=False)
    unique_matched_results.to_csv('path/to/your/result.csv', index=False)
    
    end_time = time.time()
    print(f"End processs... Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()