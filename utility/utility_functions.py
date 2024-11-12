from collections import Counter
import re
import pandas as pd

def inspect_topic(topic_model, topic_nr):
    top_words = topic_model.get_topic(topic_nr)
    print("Topic: "+str(topic_nr)+"\n\nTop Words:")
    for word in top_words:
        print(word[0], end=", ")
    print('\n\nRepresentative Target Sentences: ')
    for doc in topic_model.get_topic_info().iloc[topic_nr+1]['Representative_Docs']:
        print(doc)

def create_custom_label(topic_model, custom_label, topic_nr):
    custom_labels = {
        topic_nr: str(topic_nr)+"_"+custom_label,
    }
    topic_model.set_topic_labels(custom_labels)

# Function to retrieve custom label from topic model
def get_label_from_topic_nr(topic_model, topic_nr):
    for label in topic_model.custom_labels_:
        if label.startswith(str(topic_nr)):
            label = label
            label = re.sub(r"^\d+_", "", label)
            return label
    raise Exception('Provided Topic Number has no label assigned!')

# Function to inspect a topic by its number and retrieve its documents
'''
def inspect_topic_and_its_docs(topic_nr,n_docs=50):
    topic_docs = list(set([doc for doc, topic in zip(docs, topic_model.topics_) if topic == topic_nr]))
    print("Label: " + get_label_from_topic_nr(topic_nr)+"\n")
    print("Number of sentences for label: "+str(len(topic_docs)))
    print('\nSentences:\n')
    if len(topic_docs) < n_docs:
        n_docs = len(topic_docs)
    for i in range(n_docs):
        print(topic_docs[i])
    return topic_docs
'''

def inspect_topic_docs(topic_model, topic_nr, original_docs, n_docs=20):
    documents = [original_docs[i] for i, topic in enumerate(topic_model.topics_) if topic == topic_nr]
    print('Number of Documents: '+str(len(documents))+'\n')
    if len(documents) < n_docs:
        n_docs = len(documents)
    for i in range(n_docs):
        print(documents[i])
    return documents

# given a list of strings, returns a list of documents that contain at least one of the strings in the given list
def filter_topic_documents(topic_docs, white_list, black_list=[]):
    sentences_to_keep = []
    
    # Convert white_list and black_list to lowercase for case-insensitive matching
    white_list_lower = [item.lower() for item in white_list]
    black_list_lower = [item.lower() for item in black_list]
    
    # Check each document in a case-insensitive manner
    for doc in topic_docs:
        # Convert the document to lowercase for matching
        doc_lower = doc.lower()
        
        # If any substring in the white list is in the document, add to keep list
        if any(substring in doc_lower for substring in white_list_lower):
            sentences_to_keep.append(doc)
    
    # Remove items that contain any black-listed terms, ignoring case
    sentences_to_keep = [
        item for item in sentences_to_keep
        if not any(substring in item.lower() for substring in black_list_lower)
    ]
    
    # Remove duplicates
    sentences_to_keep = list(set(sentences_to_keep))
    sentences_to_discard = list(set(topic_docs) - set(sentences_to_keep))
    
    # Print the result
    print('Amount of sentences: ' + str(len(sentences_to_keep)))
    return sentences_to_keep, sentences_to_discard


# Function to facilitate the concatenation of new DFs
def concat_to_df(new_df, filepath, overwrite=False, ):
    try:
        df = pd.read_csv(filepath, sep='\t')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["text", "label"])
    if new_df.iloc[0]['label'] not in df['label'].values: # Make sure that DF does not already contain entry for label
        new_df = new_df.reset_index(drop=True)
        df = df.reset_index(drop=True)
        df = pd.concat([df, new_df], ignore_index=True)
        df = df.reset_index(drop=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(filepath, sep='\t')
        return df
    else:
        if overwrite:
            df = df[~df['label'].str.contains(new_df.iloc[0]['label'])]
            df = pd.concat([df, new_df], ignore_index=True)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df.to_csv("../data/labeled/send.tsv", sep='\t', index=False)
            return df
        else:
            print("Label '"+new_df.iloc[0]['label']+"' already in the final DF, so it's being skipped.")
def get_distinct_words_df(df):
    all_words = [word for sublist in df['action_object_pairs'] for word in sublist]

    # Use Counter to count occurrences of each word
    word_counts = Counter(all_words)

    # Convert to DataFrame (optional, if you want to keep it in tabular form)
    distinct_words_df = pd.DataFrame(word_counts.items(), columns=['action_object_pairs', 'count'])
    distinct_words_df = distinct_words_df.sort_values(by='count', ascending=False)
    #display(HTML(distinct_words_df.head(n).to_html()))
    return distinct_words_df

# Define a function to inspect entries for a given action-object pair
def inspect_action_object_pair(pair_to_inspect, entry, print_extracted_text=True, print_target=True):
    test = df_filtered[df_filtered['action_object_pairs'].apply(lambda x: pair_to_inspect in x)]
    if print_extracted_text:
        print(test.iloc[entry]['extracted_text'])
    if print_target:
        if print_extracted_text:
            print('----------------------')
    print(test.iloc[entry]['target'])
    del test


def is_aggregated(entry):
    """
    Check if the entry is an aggregated row (i.e., a list of keywords).
    
    Parameters:
    - entry: The action-object pair to check.
    
    Returns:
    - True if the entry is aggregated, otherwise False.
    """
    return isinstance(entry, str) and ', ' in entry



def aggregate_by_keywords(df, keywords):
    """
    Aggregate action-object pairs based on a coherent list of keywords,
    excluding already aggregated entries from being re-aggregated.
    
    Parameters:
    - df: The DataFrame to aggregate.
    - keywords: A list of strings representing a coherent group of keywords.
    
    Returns:
    - A DataFrame with the newly aggregated action-object pairs.
    """
    # Create a single pattern to match any of the keywords
    pattern = '|'.join(keywords)
    
    # Filter entries that match the keywords but are not already aggregated
    matching_entries = df[
        df['action_object_pairs'].str.contains(pattern, case=False, na=False) &
        ~df['action_object_pairs'].apply(is_aggregated)
    ]
    
    # Create a new DataFrame for aggregated results
    aggregated_rows = []
    
    # Only create a new entry for the matched pairs if there are any
    if not matching_entries.empty:
        aggregated_row = {
            'action_object_pairs': ', '.join(matching_entries['action_object_pairs'].tolist()),
            'count': matching_entries['count'].sum()
        }
        aggregated_rows.append(aggregated_row)

        # Remove the matching entries from the original DataFrame
        df = df.drop(matching_entries.index)

    # Convert aggregated rows to DataFrame if any
    aggregated_df = pd.DataFrame(aggregated_rows)

    # Concatenate remaining entries with the aggregated DataFrame
    final_df = pd.concat([df, aggregated_df], ignore_index=True)

    return final_df.sort_values(by='count', ascending=False).reset_index(drop=True)

def remove_entries_containing(aggregated_df, original_df, substring):
    original_df = get_distinct_words_df(original_df)
    # Step 1: Identify the aggregated row index
    aggregated_row_index = aggregated_df[aggregated_df['action_object_pairs'].str.contains(',', case=False)].index
    if not aggregated_row_index.empty:
        aggregated_row_index = aggregated_row_index[0]
        
        # Step 2: Get the current list and split into individual entries
        current_list = aggregated_df.at[aggregated_row_index, 'action_object_pairs'].split(', ')
        
        # Step 3: Identify entries to remove
        entries_to_remove = [entry for entry in current_list if substring in entry]
        
        # Step 4: Create new rows for each removed entry using original counts
        new_rows = []
        for entry in entries_to_remove:
            # Get the count of the removed entry from the original DataFrame
            count_of_entry = original_df.loc[original_df['action_object_pairs'] == entry, 'count']
            if not count_of_entry.empty:
                new_rows.append({'action_object_pairs': entry, 'count': count_of_entry.values[0]})
            else:
                print(f"Warning: Could not find count for entry '{entry}'")

        # Step 5: Remove the entries from the current list
        updated_list = [entry for entry in current_list if entry not in entries_to_remove]

        # Step 6: Update the aggregated row
        if new_rows:
            aggregated_df.at[aggregated_row_index, 'action_object_pairs'] = ', '.join(updated_list)
            updated_count = aggregated_df.at[aggregated_row_index, 'count'] - sum(row['count'] for row in new_rows)
            aggregated_df.at[aggregated_row_index, 'count'] = updated_count

            # Step 7: Convert new_rows to DataFrame
            new_rows_df = pd.DataFrame(new_rows)

            # Step 8: Concatenate new rows for removed entries to the aggregated DataFrame
            aggregated_df = pd.concat([aggregated_df, new_rows_df], ignore_index=True)

            # Step 9: Sort the DataFrame by count in descending order
            aggregated_df = aggregated_df.sort_values(by='count', ascending=False).reset_index(drop=True)
    
    return aggregated_df


def aggregate_specific_indices(df, index_pairs):
    """
    Aggregate entries in the DataFrame based on specific index pairs.

    Parameters:
    - df: The DataFrame to aggregate.
    - index_pairs: A list of tuples, where each tuple contains indices of rows to aggregate.

    Returns:
    - A DataFrame with aggregated action-object pairs and their counts.
    """
    # Create a list to hold new aggregated rows
    aggregated_rows = []

    # Track which indices have been aggregated to avoid duplicates
    aggregated_indices = set()

    for indices in index_pairs:
        # Check if all indices are valid and not already aggregated
        if all(idx < len(df) for idx in indices) and not any(idx in aggregated_indices for idx in indices):
            # Select the rows to aggregate
            group = df.iloc[list(indices)]
            # Aggregate the action_object_pairs and the counts
            aggregated_row = {
                'action_object_pairs': ', '.join(group['action_object_pairs']),
                'count': group['count'].sum()
            }
            aggregated_rows.append(aggregated_row)
            # Mark these indices as aggregated
            aggregated_indices.update(indices)

    # Create a new DataFrame from aggregated rows
    aggregated_df = pd.DataFrame(aggregated_rows)

    # Add remaining unaggregated rows to the aggregated DataFrame
    unaggregated_rows = df[~df.index.isin(aggregated_indices)]
    aggregated_df = pd.concat([aggregated_df, unaggregated_rows], ignore_index=True)

    return aggregated_df.sort_values(by='count', ascending=False).reset_index(drop=True)


def split_dataframes(df, action_object_pairs):
    mask = df['action_object_pairs'].progress_apply(lambda pairs: any(pair in action_object_pairs for pair in pairs))

    # Extract the rows that match the filter criteria into a new DataFrame
    df_intent = df[mask].copy()

    # Remove the matching rows from the original DataFrame
    df_remaining = df[~mask].copy()
    
    return df_intent, df_remaining


def create_count_df(df):
    all_strings = [item for sublist in df['action_object_pairs'] for item in sublist]
    all_strings = [s.lower() for s in all_strings]
    # Step 2: Count occurrences of each full string
    full_string_counts = Counter(all_strings)

    # Step 3: Convert the Counter to a DataFrame and sort by counts in descending order
    counts_df = pd.DataFrame(full_string_counts.items(), columns=['action_object_pairs', 'Count']).sort_values(by='Count', ascending=False)

    # Reset index for neatness (optional)
    counts_df = counts_df.reset_index(drop=True)
    return counts_df