import requests
import json
import os

# --- Step 1: Fetch all workarounds with pagination ---

# Base URL for the API endpoint to fetch Problem Workarounds
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/ProblemWorkarounds"

# Authorization headers (replace ****** with your actual API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# List to store all workaround records
all_workarounds = []
url = base_url

# Loop to paginate through the data until there are no more pages
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # If the request fails, stop execution and print the error
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse the response JSON
    data = response.json()

    # Extract the list of workaround records from the current page
    workarounds_page = data.get("value", [])
    all_workarounds.extend(workarounds_page)

    # Get the URL for the next page if it exists, otherwise exit the loop
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_workarounds)} total workarounds")

# --- Step 2: Clean the data ---

# List to store cleaned workaround records
cleaned_workarounds = []

# Loop through each record and remove any empty/null fields
for workaround in all_workarounds:
    cleaned = {key: value for key, value in workaround.items() if value not in [None, "", [], {}]}

    # Only keep records that still contain meaningful data
    if cleaned:
        cleaned_workarounds.append(cleaned)

print(f"Cleaned data: {len(cleaned_workarounds)} valid workarounds")

# --- Step 3: Split into batches under 2MB each ---

# Create a directory to store batch files if it doesn't exist
output_dir = "workarounds_batches"
os.makedirs(output_dir, exist_ok=True)

# Define the maximum allowed file size (2MB)
max_file_size_bytes = 2 * 1024 * 1024  # 2 megabytes

# Initialize variables for batch processing
current_batch = []
current_size = 0
batch_num = 1


# Helper function to estimate the size of a JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through the cleaned records to group them into size-constrained batches
for record in cleaned_workarounds:
    record_size = get_json_size(record)

    # If adding this record would exceed the 2MB limit, write current batch to file
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"workarounds_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Reset batch variables for the next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the current record to the batch
    current_batch.append(record)
    current_size += record_size

# Write the final batch to file (if there are remaining records)
if current_batch:
    with open(os.path.join(output_dir, f"workarounds_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

print("All workarounds batches created successfully.")
