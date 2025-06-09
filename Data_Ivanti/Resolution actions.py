import requests
import json
import os

# --- Step 1: Fetch all resolution actions with pagination ---

# Base URL for the API endpoint (replace with your actual URL)
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/ProblemResolutionActions"

# Authorization header (replace ****** with your actual REST API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all resolution action records
all_resolution_actions = []
url = base_url

# Fetch data page by page using @odata.nextLink for pagination
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse JSON response and extract records
    data = response.json()
    actions_page = data.get("value", [])

    # Add records from current page to the master list
    all_resolution_actions.extend(actions_page)

    # Update URL to next page if available
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_resolution_actions)} total resolution actions")

# --- Step 2: Clean the data ---

# Create a list to store only non-empty, cleaned records
cleaned_resolution_actions = []

# Loop through each record and remove empty or null fields
for action in all_resolution_actions:
    cleaned = {key: value for key, value in action.items() if value not in [None, "", [], {}]}

    # Only add records that still contain data after cleaning
    if cleaned:
        cleaned_resolution_actions.append(cleaned)

print(f"Cleaned data: {len(cleaned_resolution_actions)} valid resolution actions")

# --- Step 3: Split into batches under 2MB each ---

# Output directory to save the batches
output_dir = "resolution_actions_batches"
os.makedirs(output_dir, exist_ok=True)

# Define the maximum file size in bytes (2MB)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables for batching
current_batch = []
current_size = 0
batch_num = 1


# Helper function to estimate the JSON-encoded size of a record
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through cleaned records and split into batches
for record in cleaned_resolution_actions:
    record_size = get_json_size(record)

    # If adding this record would exceed the max size, save the current batch
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"resolution_actions_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Reset for the next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the record to the current batch
    current_batch.append(record)
    current_size += record_size

# Save the final batch (if any records remain)
if current_batch:
    with open(os.path.join(output_dir, f"resolution_actions_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final message
print("All resolution action batches created successfully.")
