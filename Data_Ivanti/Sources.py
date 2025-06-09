import requests
import json
import os

# --- Step 1: Fetch all sources with pagination ---

# Base URL of the API endpoint (update with your actual endpoint)
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/ProblemSources"

# API headers including the authorization key (replace ****** with your key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all fetched source records
all_sources = []
url = base_url

# Loop through paginated API results using @odata.nextLink
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Stop and display an error if the request fails
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse the JSON response and extract the "value" array (data)
    data = response.json()
    sources_page = data.get("value", [])

    # Add the records from this page to the main list
    all_sources.extend(sources_page)

    # Check if there is a next page, else stop
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_sources)} total sources")

# --- Step 2: Clean the data ---

# List to store cleaned records (removing empty or null fields)
cleaned_sources = []

for source in all_sources:
    # Remove any fields where the value is None, empty string, empty list, or empty dict
    cleaned = {key: value for key, value in source.items() if value not in [None, "", [], {}]}

    # Only add records that still contain data after cleaning
    if cleaned:
        cleaned_sources.append(cleaned)

print(f"Cleaned data: {len(cleaned_sources)} valid sources")

# --- Step 3: Split into batches under 2MB each ---

# Create the output directory to save batch files
output_dir = "sources_batches"
os.makedirs(output_dir, exist_ok=True)

# Define the maximum size per file (2MB in bytes)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables to track batch state
current_batch = []
current_size = 0
batch_num = 1


# Helper function to calculate the size of a JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through each cleaned record and split into batches
for record in cleaned_sources:
    record_size = get_json_size(record)

    # If adding this record exceeds the size limit, save the current batch
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"sources_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Start a new batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the record to the current batch
    current_batch.append(record)
    current_size += record_size

# Save the last batch if any records remain
if current_batch:
    with open(os.path.join(output_dir, f"sources_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final confirmation message
print("All sources batches created successfully.")
