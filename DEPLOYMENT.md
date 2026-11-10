# Deployment plan

This first release is intended to run locally before public deployment.

## Recommended next deployment sequence

1. Push the repository to GitHub and verify the CI workflow.
2. Deploy the FastAPI backend to a Python hosting service.
3. Configure a managed PostgreSQL database and set `DATABASE_URL`.
4. Configure `ALLOWED_ORIGINS` to the exact deployed frontend origin.
5. Deploy the React frontend as a static site with `VITE_API_BASE_URL` pointing to the backend.
6. Replace in-memory dataset storage with durable, access-controlled storage before accepting real user datasets.
7. Add authentication, rate limits, request logging, retention and deletion controls before public multi-user use.

Do not expose the local demo publicly with sensitive datasets. The current backend has no authentication and uses process-local dataset sessions.
