# Deployment Plan: PCBuild Assist (100% Free on Vercel)

This detailed guide explains how to deploy both your **Frontend** and **Backend** to **Vercel** for free. Vercel is an excellent platform that supports both static sites (your React frontend) and serverless functions (your Python backend).

---

## Prerequisites
1.  **Vercel Account**: Sign up for free at [vercel.com](https://vercel.com/signup).
2.  **GitHub Repository**: Ensure your code is pushed to GitHub.
3.  **Algolia Keys**: Have your Application ID and API Keys ready from your Algolia Dashboard.

---

## Part 1: Local Preparation (One-Time)
Since Vercel's serverless environment is lightweight, we moved the heavy data processing tools to a separate file so they don't break the production build.

1.  **Open your terminal** in the project folder.
2.  **Navigate to the backend**:
    ```poweshell
    cd backend
    ```
3.  **Install development tools**:
    ```powershell
    pip install -r dev-requirements.txt
    ```
4.  **Index your data to Algolia**:
    (Make sure your `backend/.env` file has the `ALGOLIA_ADMIN_API_KEY`)
    ```powershell
    python scripts/index_data.py
    ```
    *You should see a success message saying components were uploaded.*

---

## Part 2: Deploy the Backend (The API)

1.  **Log in** to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click the **"Add New..."** button (top right) and select **"Project"**.
3.  **Import Git Repository**:
    *   Find your `pcbuild_assist` repository in the list and click **"Import"**.
4.  **Configure Project** (Crucial Step):
    *   **Project Name**: Enter `pcbuild-backend`.
    *   **Root Directory**: Click "Edit" and select the `backend` folder.
    *   **Framework Preset**: Leave as "Other" (Vercel usually detects Python automatically).
5.  **Environment Variables**:
    *   Expand the "Environment Variables" section.
    *   Add the following pairs (copy values from your local `.env`):
        *   `ALGOLIA_APP_ID` : `Your_App_ID`
        *   `ALGOLIA_SEARCH_API_KEY` : `Your_Search_Key`
        *   `ALGOLIA_ADMIN_API_KEY` : `Your_Admin_Key`
6.  Click **"Deploy"**.
    *   Wait for the build to complete. It might take a minute.
    *   Once done, you will see a big "Congratulations!" screen.
7.  **Get your Backend URL**:
    *   Click "Continue to Dashboard".
    *   On the top left, under "Domains", copy the URL (e.g., `https://pcbuild-backend.vercel.app`).
    *   *Test it*: Open a new tab and go to `https://pcbuild-backend.vercel.app/docs`. You should see the API documentation.

---

## Part 3: connect Frontend to Backend

Now we need to tell your frontend code where to find the live backend we just deployed.

1.  **Go back to your code editor**.
2.  Open the file `frontend/vercel.json`.
3.  **Update the URL**:
    *   Replace `https://REPLACE_WITH_YOUR_RENDER_BACKEND_URL` with the URL you just copied (e.g., `https://pcbuild-backend.vercel.app`).
    *   Make sure to keep the `/api/:path*` part at the end.
    
    *Example:*
    ```json
    {
      "rewrites": [
        {
          "source": "/api/:path*",
          "destination": "https://pcbuild-backend.vercel.app/api/:path*"
        },
        {
          "source": "/health",
          "destination": "https://pcbuild-backend.vercel.app/health"
        }
      ]
    }
    ```
4.  **Save, Commit and Push**:
    ```powershell
    git add frontend/vercel.json
    git commit -m "Update backend URL for production"
    git push
    ```

---

## Part 4: Deploy the Frontend

1.  Go back to your **Vercel Dashboard**.
2.  Click **"Add New..."** -> **"Project"**.
3.  **Import the SAME repository again**:
    *   Click "Import" next to `pcbuild_assist`.
4.  **Configure Project**:
    *   **Project Name**: Enter `pcbuild-frontend`.
    *   **Root Directory**: Click "Edit" and select the `frontend` folder.
    *   **Framework Preset**: It should auto-detect **"Vite"**. If not, select it.
5.  **Environment Variables**:
    *   Add these variables (from your `frontend/.env`):
        *   `VITE_ALGOLIA_APP_ID`: `Your_App_ID`
        *   `VITE_ALGOLIA_SEARCH_KEY`: `Your_Search_Key`
        *   `VITE_ALGOLIA_INDEX_NAME`: `pc_components`
6.  Click **"Deploy"**.
    *   Wait for the build to finish.
7.  **Done!**
    *   Click the domain link (e.g., `https://pcbuild-frontend.vercel.app`).
    *   Your App is now live! The search should work, and the "API Status" in the header should say "Healthy".

---

## Troubleshooting

-   **Backend 404 on home page**: This is normal if you don't have a root route (`/`). Check `/docs` or `/health` to verify it's running.
-   **Frontend API Status "Offline"**:
    *   Double-check your `frontend/vercel.json` file. Did you push the change?
    *   Check the Network tab in your browser dev tools. Are requests going to `/api/...`?
