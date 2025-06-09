import requests
import json
import os

# --- Step 1: Fetch all documents with pagination ---

# Base URL for the API endpoint to get all knowledge documents
base_url = "https://trainer.thinktanks.co.za/HEAT/api/odata/businessobject/FRS_Knowledge__Documents"

# Authorization headers (replace ****** with your actual API key)
headers = {
    "Authorization": "rest_api_key=918E6C7ABA274AEFA0B3B1009168C459"
}

# Initialize list to store all fetched documents
all_documents = []
url = base_url  # Start with the base URL

# Loop to fetch paginated results
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)

    # If the request failed, print error and stop
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        break

    # Parse JSON response
    data = response.json()

    # Get the documents from this page
    documents_page = data.get("value", [])

    # Append to the master list
    all_documents.extend(documents_page)

    # Get the next page URL if it exists
    url = data.get("@odata.nextLink", None)

# Log total documents fetched
print(f"Fetched {len(all_documents)} total documents")

# --- Step 2: Clean the data ---

# Initialize list to hold cleaned (non-empty) document entries
cleaned_documents = []

# Remove any fields in each document that are empty, null, or unnecessary
for doc in all_documents:
    cleaned = {
        key: value
        for key, value in doc.items()
        if value not in [None, "", [], {}]  # Filter out empty values
    }
    if cleaned:  # Only keep non-empty documents
        cleaned_documents.append(cleaned)

# Log total cleaned records
print(f"Cleaned data: {len(cleaned_documents)} valid documents")

# --- Step 3: Split into batches under 2MB each ---

# Output directory to save the document batches
output_dir = "documents_batches"
os.makedirs(output_dir, exist_ok=True)  # Create it if it doesn't exist

# Maximum file size per batch (2MB)
max_file_size_bytes = 2 * 1024 * 1024

# Initialize variables for batching
current_batch = []
current_size = 0
batch_num = 1


# Helper function to calculate size of a JSON object in bytes
def get_json_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))


# Go through each cleaned document and batch appropriately
for record in cleaned_documents:
    record_size = get_json_size(record)

    # If adding this record exceeds the batch size, write current batch to file
    if current_size + record_size > max_file_size_bytes:
        with open(os.path.join(output_dir, f"documents_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
            json.dump(current_batch, f, indent=2, ensure_ascii=False)
        print(f"Wrote batch {batch_num} with {len(current_batch)} records")

        # Start a new batch
        batch_num += 1
        current_batch = []
        current_size = 0

    # Add record to current batch
    current_batch.append(record)
    current_size += record_size

# Write the final batch to disk (if it has any data)
if current_batch:
    with open(os.path.join(output_dir, f"documents_batch_{batch_num}.json"), "w", encoding="utf-8") as f:
        json.dump(current_batch, f, indent=2, ensure_ascii=False)
    print(f"Wrote final batch {batch_num} with {len(current_batch)} records")

# Log success
print("All batches created successfully.")
