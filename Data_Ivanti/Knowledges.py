import requests
import json
import os

# --- Step 1: Fetch all knowledges with pagination ---

# Base URL for the API endpoint to retrieve "FRS_Knowledges" data (limited to 100 records per page)
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/FRS_Knowledges?$top=100"

# Authentication header with REST API key (replace ****** with actual key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all retrieved knowledge records
all_knowledges = []
url = base_url

# Loop to handle pagination using @odata.nextLink
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse JSON response
    data = response.json()

    # Extract current page of records
    knowledges_page = data.get("value", [])

    # Append records to the master list
    all_knowledges.extend(knowledges_page)

    # Get next page URL if available
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_knowledges)} total knowledges")

# --- Step 2: Clean the data ---

# List to store cleaned knowledge entries
cleaned_knowledges = []

# Remove fields that have empty values (None, "", [], {})
for knowledge in all_knowledges:
    cleaned = {
        key: value for key, value in knowledge.items()
        if value not in [None, "", [], {}]
    }
    if cleaned:  # Only keep non-empty records
        cleaned_knowledges.append(cleaned)

print(f"Cleaned data: {len(cleaned_knowledges)} valid knowledges")

# --- Step 3: Split into batches under 2MB each ---

# Directory to save the output JSON files
output_dir = "knowledges_batches"
os.makedirs(output_dir, exist_ok=True)

# Maximum size per file: 2MB
max_file_size_bytes = 2 * 1024 * 1024

# Initialize batching variables
current_batch = []
current_size = 0
batch_num = 1


# Helper function to calculate JSON-encoded byte size of an object
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through cleaned records and group them into size-limited batches
for record in cleaned_knowledges:
    record_size = get_json_size(record)

    # If adding this record exceeds 2MB, write current batch to file
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"knowledges_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Prepare for next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add record to current batch
    current_batch.append(record)
    current_size += record_size

# Write the final batch if it contains any remaining records
if current_batch:
    with open(os.path.join(output_dir, f"knowledges_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final success message
print("All knowledge batches created successfully.")
