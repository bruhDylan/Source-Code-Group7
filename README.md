﻿
# Source-Code-Group7





## 5. Build & Deployment

### Current Deployment Status

Due to time constraints, the model was not fully deployed on Azure.  
The current version of the chatbot is deployed on the **Lovable website** for demonstration purposes.

All API endpoints and backend logic are stored in GitHub, with sensitive credentials (API keys, endpoints) managed through environment variables in a `.env` file.

### Data Access

The chatbot retrieves data from an **Azure Cognitive Search index** (RAG pipeline).  
All responses are generated based on documents retrieved from this RAG index.  
No external APIs or additional databases were used.

---

## CI/CD Pipeline

While a full Azure DevOps Pipeline was not implemented, this is the intended structure based on our architecture:

```yaml
# Example Azure Pipeline
stages:
  - build_frontend: npm install && npm run build
  - deploy_backend: docker push thinktank-api:v1.0
  - run_tests: pytest /backend/tests
```

**Current Implementation:**
- The React frontend is built locally and deployed on the Lovable website.
- The backend is tested and run locally via FastAPI.
- The backend API code is container-ready (Dockerfile prepared), though full Azure deployment is pending.

---

## Environment Variables

Environment variables are stored securely in GitHub using a `.env` file (not committed to the repository).

| Variable                | Production Value                                  | Purpose                            |
|-------------------------|--------------------------------------------------|------------------------------------|
| `AZURE_SEARCH_ENDPOINT` | `https://thinktank-search.search.windows.net`     | Azure Cognitive Search endpoint    |
| `AZURE_SEARCH_API_KEY`  | `[Stored in .env / Key Vault]`                    | Cognitive Search API authentication |
| `AZURE_OPENAI_ENDPOINT` | `https://gpt.openai.azure.com` (planned)          | GPT-4 model API endpoint           |
| `AZURE_OPENAI_API_KEY`  | `[Stored in .env / Key Vault]`                    | GPT-4 model API authentication     |

**Note:** `ES_HOST` and `IVANTI_KEY` were part of the initial plan but were not required in the final RAG-based implementation.
 
 ---


### Flow Summary

1. User types a question in the React Chatbot UI.
2. The frontend sends the question via REST API to the FastAPI backend.
3. The backend first queries the Azure Cognitive Search index (RAG pipeline).
4. Retrieved documents are sent along with the question to Azure OpenAI GPT-4 API.
5. GPT-4 generates a response grounded in the retrieved content.
6. The response is returned to the user via the React Chat UI.

---

## Summary

- The system is deployed on **Lovable** for demonstration purposes.  
- Backend and API are fully implemented and version-controlled in **GitHub**.  
- Data flow relies on the **RAG pipeline** with Cognitive Search and GPT-4 via API.  
- CI/CD is prepared but full automated deployment is still a future step.
