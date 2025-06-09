import requests
import json
import os

# --- Step 1: Fetch all problems with pagination ---

# Base URL to access the Problems business object from the HEAT API
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/Problems"

# Authorization headers (replace ****** with your actual API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all problem records retrieved
all_problems = []
url = base_url

# Loop to handle pagination using @odata.nextLink
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Convert the response to JSON and extract current page data
    data = response.json()
    problems_page = data.get("value", [])

    # Add current page of records to the master list
    all_problems.extend(problems_page)

    # Get the next page URL if available (pagination)
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_problems)} total problems")

# --- Step 2: Clean the data ---

# Prepare a list to store cleaned problem records
cleaned_problems = []

# Filter out any fields in each record with null/empty values
for problem in all_problems:
    cleaned = {
        key: value for key, value in problem.items()
        if value not in [None, "", [], {}]
    }
    # Only include records that are not completely empty after cleaning
    if cleaned:
        cleaned_problems.append(cleaned)

print(f"Cleaned data: {len(cleaned_problems)} valid problems")

# --- Step 3: Split into batches under 2MB each ---

# Directory to save the output JSON batch files
output_dir = "problems_batches"
os.makedirs(output_dir, exist_ok=True)

# Set maximum file size for each batch (2 megabytes)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables for batching
current_batch = []
current_size = 0
batch_num = 1

# Function to calculate the byte size of a JSON-encoded object
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

# Loop through cleaned records and group them into batches
for record in cleaned_problems:
    record_size = get_json_size(record)

    # If the next record would exceed the size limit, save the current batch
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"problems_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Reset batch variables
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the current record to the batch
    current_batch.append(record)
    current_size += record_size

# Save the final batch if it contains any remaining records
if current_batch:
    with open(os.path.join(output_dir, f"problems_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Final confirmation message
print("All problem batches created successfully.")
