import requests
import json
import os

# --- Step 1: Fetch all error messages with pagination ---

# API endpoint to fetch error messages from the FRS_Knowledge__ErrorMessages table
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/FRS_Knowledge__ErrorMessages"

# Authentication header (replace the asterisks with your actual API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all fetched error message records
all_error_messages = []
url = base_url  # Start with the base URL

# Paginated fetch loop
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Handle request errors
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse the JSON response
    data = response.json()

    # Extract current page of error messages
    messages_page = data.get("value", [])

    # Add to the cumulative list
    all_error_messages.extend(messages_page)

    # Get the link to the next page, if available
    url = data.get("@odata.nextLink", None)

# Log the total number of error messages fetched
print(f"Fetched {len(all_error_messages)} total error messages")

# --- Step 2: Clean the data ---

# Initialize list to hold cleaned (non-empty) error message records
cleaned_error_messages = []

# Remove fields with empty, null, or non-informative values
for message in all_error_messages:
    cleaned = {
        key: value
        for key, value in message.items()
        if value not in [None, "", [], {}]  # Filter out empty values
    }
    if cleaned:  # Keep only non-empty records
        cleaned_error_messages.append(cleaned)

# Log the number of valid cleaned records
print(f"Cleaned data: {len(cleaned_error_messages)} valid error messages")

# --- Step 3: Split into batches under 2MB each ---

# Output directory to store the resulting JSON batch files
output_dir = "error_messages_batches"
os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist

# Define the maximum allowed size per JSON file (2MB)
max_file_size_bytes = 2 * 1024 * 1024  # 2MB

# Initialize batching variables
current_batch = []
current_size = 0
batch_num = 1


# Function to calculate JSON-encoded byte size of an object
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through cleaned error messages and create size-limited batches
for record in cleaned_error_messages:
    record_size = get_json_size(record)

    # If adding the next record exceeds size limit, write the current batch to file
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"error_messages_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Reset for next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the record to the current batch
    current_batch.append(record)
    current_size += record_size

# Write the final batch to a file
if current_batch:
    with open(os.path.join(output_dir, f"error_messages_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final log message
print("All error message batches created successfully.")
