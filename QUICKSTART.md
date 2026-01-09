# Quick Start Guide - PCBuild Assist

## 🚀 Quick Start (One Command)

**Already set up?** Just run:

```bash
run.bat
```

This will automatically:
- ✅ Activate the Python virtual environment
- ✅ Start the FastAPI backend server (port 5000)
- ✅ Start the Vite frontend dev server (port 5173)
- ✅ Open the app in your browser

**First time?** Follow the manual setup below:

---

## 🛠️ Manual Setup (First Time)

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Algolia account (free)

### Step 1: Get Algolia Credentials

1. Visit [algolia.com](https://www.algolia.com) and sign up
2. Create a new application
3. Go to **API Keys** and copy:
   - Application ID
   - Search-Only API Key
   - Admin API Key
4. Keep these safe - you'll need them next!

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `backend/.env` file:

```env
ALGOLIA_APP_ID=your_app_id_here
ALGOLIA_SEARCH_API_KEY=your_search_api_key_here
ALGOLIA_ADMIN_API_KEY=your_admin_api_key_here
BACKEND_PORT=5000
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

**⚠️ Replace the placeholders with your actual Algolia credentials!**

### Step 4: Index Data to Algolia

```bash
# Still in backend directory with venv activated
python scripts/index_data.py
```

You should see:
```
🚀 Starting data indexing to Algolia...
📄 Processing cpu.csv (CPU)...
   Found 1415 rows
   ✅ Processed 1415 components
...
🎉 Indexing complete!
📊 Total components indexed: 10000+
```

This process takes 1-2 minutes. It uploads all PC component data to Algolia.

### Step 5: Start Backend Server

```bash
# In backend directory
uvicorn app.main:app --reload --port 5000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
INFO:     Application startup complete.
```

**✅ Test it!** Visit http://localhost:5000/docs to see the API documentation.

### Step 6: Setup Frontend (Optional for now)

```bash
# Open NEW terminal
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

## 🧪 Test the API

### Test 1: Search for CPUs

Open http://localhost:5000/docs and try:

**Endpoint:** `GET /api/components/search`
**Parameters:**
- q: "Intel i9"
- component_type: "CPU"
- max_price: 500

Or use curl:
```bash
curl "http://localhost:5000/api/components/search?q=Intel%20i9&component_type=CPU&max_price=500"
```

### Test 2: Get Compatible Motherboards

Find a CPU ID from the search above, then:

**Endpoint:** `GET /api/suggestions/compatible-motherboard/{cpu_id}`

Example:
```bash
curl "http://localhost:5000/api/suggestions/compatible-motherboard/cpu_0"
```

You should get motherboards with matching sockets!

### Test 3: Check Build Compatibility

**Endpoint:** `POST /api/compatibility/check-build`

Using the Swagger UI at /docs, or:

```bash
curl -X POST "http://localhost:5000/api/compatibility/check-build" \
  -H "Content-Type: application/json" \
  -d '{
    "cpu_id": "cpu_0",
    "motherboard_id": "mb_0"
  }'
```

Response shows socket compatibility and recommendations!

## 📖 API Examples

### Search by Type
```bash
# Get all GPUs under $500
curl "http://localhost:5000/api/components/type/GPU?max_price=500"

# Get all AM5 motherboards
curl "http://localhost:5000/api/components/type/Motherboard?socket=AM5"
```

### Get Suggestions
```bash
# Suggest RAM for a specific motherboard
curl "http://localhost:5000/api/suggestions/ram/mb_0"

# Get PSU recommendations for 400W system
curl "http://localhost:5000/api/suggestions/psu?total_power=400"
```

## 🎯 What's Working

✅ **Full-text search** - Search any component by name
✅ **Filtering** - By type, brand, price, socket, memory type
✅ **Compatibility checking** - Socket matching, power calculations
✅ **Smart suggestions** - Auto-suggest next compatible components
✅ **Fast results** - Algolia returns results in <50ms

## ⚠️ Common Issues

### "Module not found" error
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### "Missing Algolia credentials" error
- Check that `.env` file exists in `backend/` directory
- Verify credentials are correct (no extra quotes or spaces)
- Make sure you're using ADMIN API key for indexing

### "Index is empty" when searching
- Run `python scripts/index_data.py` again
- Check Algolia dashboard to confirm data is indexed
- Wait 30 seconds after indexing before searching

### Port already in use
```bash
# Backend (change port in .env)
BACKEND_PORT=5001

# Or kill the process using the port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 🎨 What's Next?

The **backend is fully functional** and ready to use! Next steps:

1. **Frontend UI** - Build React components for component selection
2. **Visual Design** - Add modern styling and animations
3. **User Flow** - Implement step-by-step build wizard
4. **Deployment** - Deploy to Vercel/Railway for live testing

## 💡 Tips

- Use the **Swagger UI** (/docs) to explore all endpoints interactively
- Check **Algolia Dashboard** to see search analytics
- Read `IMPLEMENTATION_SUMMARY.md` for technical details
- Review `plan.md` for complete project roadmap

## 🆘 Need Help?

- **API Docs**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **Check Logs**: Watch uvicorn terminal output
- **Algolia Dashboard**: Check if data is indexed properly

---

**You're all set!** 🎉  
The backend API is running and ready to power the PCBuild Assist frontend.
