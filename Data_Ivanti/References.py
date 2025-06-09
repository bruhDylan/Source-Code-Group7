import requests
import json
import os

# --- Step 1: Fetch all references with pagination ---

# Define the base API endpoint for fetching knowledge references
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/FRS_Knowledge__References"

# Set the authorization header (replace ****** with your actual REST API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to hold all fetched reference records
all_references = []
url = base_url

# Loop to fetch all paginated data using @odata.nextLink
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse the response JSON
    data = response.json()

    # Get the list of records in the current page
    references_page = data.get("value", [])

    # Add current page's records to the full list
    all_references.extend(references_page)

    # Get the next page link if available
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_references)} total references")

# --- Step 2: Clean the data ---

# List to hold cleaned reference records
cleaned_references = []

# Iterate through each record and remove empty/null fields
for reference in all_references:
    cleaned = {
        key: value for key, value in reference.items()
        if value not in [None, "", [], {}]
    }
    # Only add non-empty records
    if cleaned:
        cleaned_references.append(cleaned)

print(f"Cleaned data: {len(cleaned_references)} valid references")

# --- Step 3: Split into batches under 2MB each ---

# Define the output directory for storing batches
output_dir = "references_batches"
os.makedirs(output_dir, exist_ok=True)

# Define the maximum file size (2MB)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables for batch creation
current_batch = []
current_size = 0
batch_num = 1


# Helper function to calculate size of a JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through cleaned records and create batches
for record in cleaned_references:
    record_size = get_json_size(record)

    # If adding the next record exceeds 2MB, write current batch to file
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"references_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Prepare for next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the current record to the batch
    current_batch.append(record)
    current_size += record_size

# Write the final batch to file (if any records remain)
if current_batch:
    with open(os.path.join(output_dir, f"references_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final success message
print("All reference batches created successfully.")
