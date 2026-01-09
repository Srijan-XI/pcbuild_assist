# PCBuild Assist - Algolia Dev Challenge

A smart PC component builder that uses **Algolia Agent Studio** to proactively suggest compatible components based on user selections.

## 🎯 Project Overview

This application demonstrates how contextual data retrieval can enhance user experience **without requiring conversational interaction**. Users can build a complete PC by selecting components, and the system will:

- ✅ Validate compatibility automatically
- 🔍 Suggest compatible components proactively  
- 💡 Calculate power requirements and total cost
- ⚡ Provide fast, relevant search with Algolia

## 🚀 Features

### 1. Smart Component Search
- Real-time search across 25+ component categories
- Advanced filtering (price range, brand, performance tier)
- Instant results powered by Algolia

### 2. Compatibility Validation
- **CPU-Motherboard Socket Matching**
- **RAM Type Verification** (DDR4 vs DDR5)
- **Power Supply Wattage Calculation**
- **PCIe Compatibility Checks**

### 3. Proactive Suggestions
- Compatible motherboards for selected CPU
- Matching RAM for motherboard
- Balanced GPU recommendations
- Appropriate PSU based on power needs

### 4. Build Management
- Real-time price tracking
- Power consumption calculator
- Component list with specifications

## 🛠️ Tech Stack

### Backend
- **Python FastAPI** - Fast, modern API framework
- **Algolia Python SDK** - Search and indexing
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Vanilla CSS** - Styling
- **Algolia InstantSearch** (optional) - Search UI components

### Data
- **25+ CSV datasets** with PC components
- 10,000+ components across all categories

## 📦 Project Structure

```
pcbuild-assist/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   │   ├── algolia_service.py
│   │   │   ├── compatibility_service.py
│   │   │   └── suggestion_service.py
│   │   └── main.py
│   ├── data/                # Component datasets
│   ├── scripts/             # Data processing scripts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API clients
│   │   └── hooks/           # Custom React hooks
│   └── package.json
├── docs/                    # Documentation
└── README.md
```

## 🔧 Setup Instructions

### Quick Start (Recommended)

**Already configured?** Start both frontend and backend with one command:

```bash
run.bat
```

This will:
- ✅ Activate Python virtual environment
- ✅ Start FastAPI backend (port 5000)
- ✅ Start React frontend (port 5173)
- ✅ Open browser automatically

**First time?** Follow the detailed setup below:

### Prerequisites
- Python 3.9+
- Node.js 18+
- Algolia Account (Free Build Plan)

### Backend Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd pcbuild-assist
```

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your Algolia credentials
```

5. **Index data to Algolia**
```bash
python scripts/index_data.py
```

6. **Run backend server**
```bash
uvicorn app.main:app --reload --port 5000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
# Add your API URL and Algolia keys
```

4. **Run development server**
```bash
npm run dev
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### Key Endpoints

#### Component Search
```
GET /api/components/search?q=Intel+i9&component_type=CPU
```

#### Compatibility Check
```
POST /api/compatibility/check-build
Body: { "cpu_id": "cpu_001", "motherboard_id": "mb_001" }
```

#### Smart Suggestions
```
GET /api/suggestions/compatible-motherboard/{cpu_id}
```

## 🎨 User Flow

1. **Start with CPU Selection**
   - Search for CPUs by name, brand, or specifications
   - Filter by price range and performance tier

2. **Get Motherboard Suggestions**
   - System automatically suggests compatible motherboards
   - Filters by socket type (AM5, LGA1700, etc.)

3. **Add RAM**
   - Suggests RAM compatible with motherboard
   - Matches DDR4/DDR5 and speed requirements

4. **Select GPU**
   - Recommends balanced GPUs for CPU tier
   - Checks PCIe compatibility

5. **Calculate PSU Needs**
   - Calculates total power consumption
   - Suggests PSU with proper wattage headroom

6. **Review & Finalize**
   - See complete build summary
   - View total cost and compatibility status

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Data Sources

Component data sourced from:
- PCPartPicker exports
- Manufacturer specifications
- Tech review aggregation

**Total Components**: 10,000+
- CPUs: 1,415
- Motherboards: 4,975
- Video Cards: 1,000+
- Memory: 2,000+
- Power Supplies: 500+
- Storage: 1,000+
- And more...

## 🌟 Algolia Integration

### Search Features
- **Typo tolerance** - "i9-13900k" matches "i9 13900K"
- **Faceted search** - Filter by brand, socket, tier
- **Instant results** - Sub-50ms search latency
- **Ranking** - Performance tier, price, release date

### Agent Studio Usage
- Contextual component suggestions
- Compatibility-based filtering
- Smart ranking based on user selections

## 🚢 Deployment

### Backend (Railway/Heroku)
```bash
# Railway
railway up

# Heroku
heroku create pcbuild-assist-api
git push heroku main
```

### Frontend (Vercel/Netlify)
```bash
# Vercel
vercel

# Netlify
netlify deploy --prod
```

## 📝 License

MIT License - feel free to use for learning and development

## 👥 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 🔗 Links

- **Live Demo**: [Coming Soon]
- **API Docs**: [Coming Soon]
- **Algolia Dashboard**: [Your Dashboard]

## 📧 Contact

For questions or feedback about this Algolia Dev Challenge submission:
- **Email**: your-email@example.com
- **GitHub**: @your-username

---

**Built for the Algolia Dev Challenge 2025** 🚀
Demonstrating consumer-facing, non-conversational AI experiences
