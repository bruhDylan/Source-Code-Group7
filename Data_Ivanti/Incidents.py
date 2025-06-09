import requests
import json
import os

# --- Step 1: Fetch all incidents with pagination ---

# Set the base API URL with filter to only fetch 'Resolved' incidents, limiting to 100 per page
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/Incidents?$filter=Status eq 'Resolved'&$top=100"

# Set the request headers, including authorization key (replace ****** with actual key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# Initialize an empty list to store all fetched incidents
all_incidents = []
url = base_url  # Start with the base URL

# Loop through paginated API responses
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break  # Exit loop if API call fails

    # Parse JSON response
    data = response.json()
    incidents = data.get("value", [])  # Get incidents list
    all_incidents.extend(incidents)    # Add to total incidents

    # Get the next page URL if available
    url = data.get("@odata.nextLink", None)

print(f"Fetched {len(all_incidents)} total incidents")

# --- Step 2: Clean the data ---

# Initialize a list to hold cleaned incidents
cleaned_incidents = []

# Remove keys with None, empty string, empty list, or empty dict values
for incident in all_incidents:
    cleaned = {key: value for key, value in incident.items() if value not in [None, "", [], {}]}
    if cleaned:  # Only add non-empty cleaned incidents
        cleaned_incidents.append(cleaned)

print(f"Cleaned data: {len(cleaned_incidents)} valid incidents")

# --- Step 3: Split into batches under 2MB each ---

# Define directory to save output batches
output_dir = "incidents_batches"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Define maximum file size (2MB in bytes)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables for batching
current_batch = []
current_size = 0
batch_num = 1

# Helper function to calculate size of JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

# Loop through all cleaned records
for record in cleaned_incidents:
    record_size = get_json_size(record)

    # Check if adding the current record would exceed 2MB
    if current_size + record_size > max_file_size_bytes:
        # Save the current batch to a JSON file
        with open(os.path.join(output_dir, f"incidents_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Reset for next batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add record to current batch
    current_batch.append(record)
    current_size += record_size

# Save any remaining records in the final batch
if current_batch:
    with open(os.path.join(output_dir, f"incidents_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

print("All batches created successfully.")
