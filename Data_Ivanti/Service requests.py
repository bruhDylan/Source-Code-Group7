import requests
import json
import os

# --- Step 1: Fetch all resolved service requests with pagination ---

# Base API URL with filter to only fetch service requests that have a Resolution (i.e., resolved)
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/ServiceReqs?$filter=Resolution ne '$NULL'&$top=100"

# Authorization header (replace ****** with actual API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# Initialize list to store all retrieved service requests
all_service_requests = []
url = base_url  # Starting URL for the first API request

# Loop to handle paginated results
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check for successful HTTP response
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)  # Print error details for debugging
        break  # Exit loop on error

    # Parse JSON response
    data = response.json()

    # Extract list of service requests from current page
    requests_page = data.get("value", [])

    # Add current page's data to the complete list
    all_service_requests.extend(requests_page)

    # Get the next page URL if it exists; else, loop ends
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_service_requests)} total service requests")

# --- Step 2: Clean the data ---

# Initialize list to store cleaned records
cleaned_requests = []

# Loop through each request to remove fields with null/empty values
for request in all_service_requests:
    cleaned = {
        key: value
        for key, value in request.items()
        if value not in [None, "", [], {}]  # Skip empty fields
    }
    if cleaned:  # Only keep non-empty dictionaries
        cleaned_requests.append(cleaned)

print(f"Cleaned data: {len(cleaned_requests)} valid service requests")

# --- Step 3: Split into batches under 2MB each ---

# Output directory for JSON batch files
output_dir = "service_requests_batches"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Define max size limit per batch (2MB)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize batch variables
current_batch = []
current_size = 0
batch_num = 1


# Function to calculate the size of a JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Loop through all cleaned requests to split into batches
for record in cleaned_requests:
    record_size = get_json_size(record)

    # If adding this record exceeds 2MB limit, save current batch to file
    if current_size + record_size > max_file_size_bytes:
        # Write current batch to disk
        with open(os.path.join(output_dir, f"service_requests_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Prepare for the next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add the current record to the batch
    current_batch.append(record)
    current_size += record_size

# Save any remaining records in the final batch
if current_batch:
    with open(os.path.join(output_dir, f"service_requests_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

print("All service request batches created successfully.")
