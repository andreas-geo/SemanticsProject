import time
import urllib.parse
import urllib.request
import json
import openai
import pandas as pd

# API Key
openai.api_key = 'Replace with your OpenAI API Key'

#This function reads queries from a file.
def read_sparql_queries(log_file_path, number_of_queries=100):
    """Read the top N SPARQL queries from a file trying different encodings."""
    queries = []
    encodings = ['utf-8', 'ISO-8859-1', 'utf-16', 'cp1252']
    for encoding in encodings:
        try:
            with open(log_file_path, 'r', encoding=encoding) as file:
                for line in file:
                    if len(queries) < number_of_queries:
                        query = line.strip()
                        if query:  #Check if the query is empty
                            queries.append(query)
                    else:
                        break
            break  # If successfull break the encoding loop
        except UnicodeDecodeError:
            continue  # Check next encoding 
    if not queries:
        raise ValueError(f"Could not read the file with any of the provided encodings: {encodings}")
    return queries

#Communicate with DBpedia Endpoint and retrn results. 
def execute_sparql_query(query):
    """Execute a SPARQL query against the DBpedia endpoint."""
    params = {
        "default-graph-uri": "http://dbpedia.org",
        "query": query,
        "format": "application/sparql-results+json"
    }
    try:
        response = urllib.request.urlopen(f"https://dbpedia.org/sparql?{urllib.parse.urlencode(params)}")
        data = json.loads(response.read().decode())
        print(f"Query executed successfully: {query}")
        return data
    except Exception as e:
        print(f"Failed to fetch DBpedia result for query: '{query}', with error: {e}")
        return None

#This function summarizes the text return from the API so that we can cope with the rate limit.
def summarize_result(result):
    """Summarize the DBpedia result to reduce the size of the translation request."""

    summary = json.dumps(result)[:500]
    return summary

#Transforming DBpedia results to plain English
def translate_to_english(query, result):
    """Translate DBpedia query results into English using OpenAI's API, with summarized input."""
    summarized_result = summarize_result(result)  #Sympiesi
    prompt = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Translate the following SPARQL query and its result into plain English.\nQuery: {query}\nResult: {summarized_result}"}
        ]
    }
    response = openai.ChatCompletion.create(**prompt)
    return response.choices[0]["message"]["content"]

#Main Function
def main():
    log_file_path = 'Your logfile path'
    excel_file_path = 'path to your .xlsx file'

    all_queries = read_sparql_queries(log_file_path, 150)
    successful_queries, successful_results, translations = [], [], []

    print("Attempting to fetch and translate queries:")

    for i, query in enumerate(all_queries):
        if len(successful_queries) >= 50:
            break
        result = execute_sparql_query(query)
        if result:
            successful_queries.append(query)
            successful_results.append(result)
            translation = translate_to_english(query, result)
            translations.append(translation)
            if (i + 1) % 5 == 0:
                print("Pausing for a minute to counter OpenAI's rate limits...")
                time.sleep(60)  # Pause for 60 seconds to renew allowed tokens per sec.

    # Storing results directly to excel file.
    data = {
        'Query': successful_queries,
        'DBpedia Result': [json.dumps(result) for result in successful_results],
        'Translation': translations
    }
    df = pd.DataFrame(data)
    df.to_excel(excel_file_path, index=False)
    print(f"Finished processing. Results saved to {excel_file_path}.")


if __name__ == "__main__":
    main()