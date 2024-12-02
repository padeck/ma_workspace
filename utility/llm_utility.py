
def create_json_batch(df_subset, system_prompt, userprompt, model="gpt-4o-mini", max_tokens=1000):
    indexes = df_subset.index
    emails = df_subset['text'].tolist()
    data_objects = [
        {
            "custom_id": str(index),
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model, 
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": userprompt.replace("{email}", email)}
                ],"max_tokens": max_tokens
            }
        }
        for index,email in zip(indexes, emails)
    ]
    return data_objects


def print_batches(client, limit=10):
    batches = client.batches.list(limit=limit)
    for batch in batches:
        print(f'Batch ID: {batch.id}')
        print(f'Status: {batch.status}')
        print(f'{batch.metadata['description']}')
        print(f'Output ID: {batch.output_file_id}')
        print('\n--------------------------------')
