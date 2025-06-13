
# Source Code Structure

This document explains the structure of our chatbot web app.

---

## Project Folder Layout

### Source Code Structure

```
chatbot-webapp/
├── Data_Ivanti/               # Ivanti data batch folders
│   ├── documents_batches/
│   ├── error_messages_batches/
│   ├── incidents_batches/
│   ├── knowledges_batches/
│   ├── problems_batches/
│   ├── references_batches/
│   ├── resolution_actions_batches/
│   ├── service_requests_batches/
│   ├── sources_batches/
│   └── workarounds_batches/
│
├── scripts/                   # Python scripts for handling Ivanti datasets
│   ├── Documents.py
│   ├── Error_messages.py
│   ├── Incidents.py
│   ├── Knowledges.py
│   ├── Problems.py
│   ├── References.py
│   ├── Resolution_actions.py
│   ├── Service_requests.py
│   ├── Sources.py
│   └── Workarounds.py
│
├── backend/                   # Backend logic (e.g., API routes, processing)
│   └── __init__.py
│
├── frontend/                  # Frontend UI (from thinktank-chat-ui-main)
│   └── thinktank-chat-ui-main/
│       ├── public/
│       ├── src/
│       └── package.json
│
├── config/                    # Config files & environment
│   └── .env
│
├── docs/                      # Project documentation
│   ├── README.md
│   └── README_ThinkTank_AI_Assistant.md
│
├── .gitignore                 # Ignore rules for Git
├── app.py                     # Main Python app entry point
├── requirements.txt           # Python dependencies
```

---

## Application Flow

1. The user logs into the chatbot through a login page made with Supabase.  
2. The user types a query, and the frontend sends the question to the backend.  
3. The backend uses Azure/OpenAI and cognitive search to generate a response.  
4. The response is sent back to the frontend and displayed to the user.

---

## Technologies Used

- **Frontend**: React.js  
- **Backend**: FastAPI  
- **Authentication**: Supabase  
- **Storage**: Azure Blob Storage  
- **AI**: GPT via Azure/OpenAI
