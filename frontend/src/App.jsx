import { useState, useEffect } from 'react'
import { Cpu, Menu, Search as SearchIcon, ChevronDown } from 'lucide-react'
import Builder from './Builder'
import Search from "@/components/search"
import './css/App.css'
import './css/components-education.css'
import './css/builder-styles.css'
import './css/tailwind-fallback.css'

// PC Component educational data with images
const componentInfo = [
    {
        id: 'cpu',
        name: 'CPU (Processor)',
        icon: '🧠',
        image: '/images/cpu.png',
        description: 'The brain of your PC - handles all calculations and instructions',
        details: [
            'Determines overall system performance',
            'Key specs: Cores, Threads, Clock Speed',
            'Popular brands: Intel Core & AMD Ryzen',
            'Socket type must match motherboard'
        ],
        keyFactors: ['Performance Tier', 'Core Count', 'Socket Type', 'TDP (Power)']
    },
    {
        id: 'gpu',
        name: 'GPU (Graphics Card)',
        icon: '🎮',
        image: '/images/gpu.png',
        description: 'Powers gaming, video editing, and visual workloads',
        details: [
            'Critical for gaming performance',
            'Handles graphics rendering & AI tasks',
            'Popular: NVIDIA RTX & AMD Radeon',
            'Memory (VRAM) affects resolution/settings'
        ],
        keyFactors: ['VRAM Size', 'Performance Class', 'Power Requirements', 'Cooling']
    },
    {
        id: 'motherboard',
        name: 'Motherboard',
        icon: '🔌',
        image: '/images/motherboard.png',
        description: 'The backbone connecting all components together',
        details: [
            'Must match CPU socket type',
            'Determines RAM type (DDR4/DDR5)',
            'Controls expansion options (PCIe, M.2)',
            'Chipset affects features & performance'
        ],
        keyFactors: ['Socket Type', 'Form Factor', 'RAM Support', 'Connectivity']
    },
    {
        id: 'ram',
        name: 'RAM (Memory)',
        icon: '⚡',
        image: '/images/ram.png',
        description: 'High-speed temporary storage for active tasks',
        details: [
            'More RAM = Better multitasking',
            'Speed (MHz) impacts performance',
            'DDR4 vs DDR5 compatibility crucial',
            '16GB minimum for gaming, 32GB+ for content creation'
        ],
        keyFactors: ['Capacity (GB)', 'Speed (MHz)', 'Type (DDR4/DDR5)', 'Latency']
    },
    {
        id: 'psu',
        name: 'PSU (Power Supply)',
        icon: '🔋',
        image: '/images/psu.png',
        description: 'Provides stable power to all components',
        details: [
            'Wattage must exceed total system power',
            '80+ certification = efficiency rating',
            'Modular cables for cleaner builds',
            'Quality PSU prevents component damage'
        ],
        keyFactors: ['Wattage', 'Efficiency Rating', 'Modularity', 'Reliability']
    },
    {
        id: 'storage',
        name: 'Storage (SSD/HDD)',
        icon: '💾',
        image: '/images/storage.png',
        description: 'Permanent storage for OS, games, and files',
        details: [
            'NVMe SSD: Fastest (OS & games)',
            'SATA SSD: Fast & affordable',
            'HDD: Cheap bulk storage',
            'M.2 form factor saves space'
        ],
        keyFactors: ['Type (NVMe/SATA)', 'Capacity', 'Read/Write Speed', 'Form Factor']
    }
]

const Navbar = ({ onNavigate }) => {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const menuItems = [
        { label: 'Builder', onClick: () => { onNavigate('builder'); setMobileMenuOpen(false) } },
        { label: 'Learn', onClick: () => { document.querySelector('#learn')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false) } },
        { label: 'Guides', onClick: () => { document.querySelector('#guides')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false) } },
        { label: 'Community', onClick: () => { setMobileMenuOpen(false) } }
    ]

    return (
        <nav className="fixed w-full z-40 bg-slate-950/80 backdrop-blur-md border-b border-white/5">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20">
                    <div className="flex items-center space-x-3 cursor-pointer" onClick={() => onNavigate('home')}>
                        <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-xl shadow-lg shadow-blue-500/20">
                            <Cpu className="h-6 w-6 text-white" strokeWidth={2} />
                        </div>
                        <span className="text-2xl font-bold text-white tracking-tight">
                            PCBuild<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Assist</span>
                        </span>
                    </div>

                    <div className="hidden md:flex items-center space-x-1">
                        {menuItems.map((item) => (
                            <button
                                key={item.label}
                                onClick={item.onClick}
                                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                            >
                                {item.label}
                            </button>
                        ))}
                    </div>

                    <div className="flex items-center gap-4">
                        <button className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/50 border border-white/10 text-slate-400 hover:text-white hover:border-white/20 transition-all text-sm group">
                            <SearchIcon size={16} className="group-hover:text-white transition-colors" />
                            <span className="mr-4">Search...</span>
                            <kbd className="pointer-events-none hidden h-5 select-none items-center gap-1 rounded border border-white/10 bg-white/5 px-1.5 font-mono text-[10px] font-medium text-slate-400 opacity-100 sm:flex">
                                <span className="text-xs">⌘</span>K
                            </kbd>
                        </button>
                        <button className="md:hidden p-2 text-slate-400 hover:text-white transition-colors">
                            <SearchIcon size={20} />
                        </button>
                        <button className="md:hidden p-2" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
                            <Menu className="text-slate-300" />
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="md:hidden absolute top-20 left-0 right-0 bg-slate-900/95 backdrop-blur-lg border-b border-white/10 shadow-xl">
                        <div className="px-4 py-4 space-y-2">
                            {menuItems.map((item) => (
                                <button
                                    key={item.label}
                                    onClick={item.onClick}
                                    className="w-full text-left px-4 py-3 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                                >
                                    {item.label}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </nav>
    )
}

function App() {
    const [apiStatus, setApiStatus] = useState('checking')
    const [isCheckingApi, setIsCheckingApi] = useState(true)
    const [selectedComponent, setSelectedComponent] = useState(null)
    const [currentPage, setCurrentPage] = useState('home') // 'home' or 'builder'

    useEffect(() => {
        setIsCheckingApi(true)
        fetch('/health')
            .then(res => res.json())
            .then(data => {
                setApiStatus(data.status)
                setIsCheckingApi(false)
            })
            .catch(() => {
                setApiStatus('offline')
                setIsCheckingApi(false)
            })
    }, [])

    if (currentPage === 'builder') {
        return (
            <div className="min-h-screen bg-slate-950 text-slate-200">
                <div className="fixed inset-0 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[100px]" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px]" />
                </div>

                <Navbar onNavigate={setCurrentPage} />
                <Builder onBackHome={() => setCurrentPage('home')} />
            </div>
        )
    }

    return (
        <div className="App relative z-10">
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[100px]" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px]" />
            </div>

            <Navbar onNavigate={setCurrentPage} />

            <header className="app-header mt-20">
                <h1>🖥️ PCBuild Assist</h1>
                <p>Smart PC Component Builder with Algolia</p>
                <div className="status">
                    API Status: <span className={`status-badge ${apiStatus === 'checking' ? 'checking' : apiStatus}`}>
                        {isCheckingApi ? 'Checking...' : apiStatus}
                    </span>
                </div>
            </header>

            <main className="app-main">
                <section className="hero">
                    <h2>Build Your Perfect PC</h2>
                    <p>Get intelligent component suggestions with real-time compatibility checking</p>

                    <div className="features">
                        <div className="feature">
                            <span className="icon">🔍</span>
                            <h3>Smart Search</h3>
                            <p>Find components instantly with Algolia-powered search</p>
                        </div>
                        <div className="feature">
                            <span className="icon">✅</span>
                            <h3>Compatibility Check</h3>
                            <p>Automatic validation of socket, memory, and power compatibility</p>
                        </div>
                        <div className="feature">
                            <span className="icon">💡</span>
                            <h3>Proactive Suggestions</h3>
                            <p>Get compatible component recommendations as you build</p>
                        </div>
                    </div>

                    <div className="max-w-xl mx-auto mt-12 mb-8">
                        <Search
                            applicationId={import.meta.env.VITE_ALGOLIA_APP_ID}
                            apiKey={import.meta.env.VITE_ALGOLIA_SEARCH_KEY}
                            indexName={import.meta.env.VITE_ALGOLIA_INDEX_NAME || 'pc_components'}
                            attributes={{
                                primaryText: "name",
                                secondaryText: "brand",
                                ternaryText: "price",
                                image: "image"
                            }}
                            darkMode={true}
                            className="shadow-2xl"
                        />
                    </div>

                    <button
                        onClick={() => setCurrentPage('builder')}
                        className="search-btn"
                    >
                        🚀 Start Building Now
                    </button>
                </section>

                <section className="components-education" id="learn">
                    <h2>Understanding PC Components</h2>
                    <p className="section-subtitle">Learn about the essential parts that make up your dream PC</p>

                    <div className="component-cards">
                        {componentInfo.map((comp) => (
                            <div
                                key={comp.id}
                                className={`component-info-card ${selectedComponent === comp.id ? 'selected' : ''}`}
                                onClick={() => setSelectedComponent(selectedComponent === comp.id ? null : comp.id)}
                            >
                                <div className="component-header">
                                    <div className="component-image-wrapper">
                                        <img
                                            src={comp.image}
                                            alt={comp.name}
                                            className="component-image"
                                            onError={(e) => { e.target.style.display = 'none'; e.target.parentElement.innerHTML = `<div style="font-size: 3rem; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%;">${comp.icon}</div>` }}
                                        />
                                    </div>
                                    <div className="component-title">
                                        <span className="component-icon">{comp.icon}</span>
                                        <h3>{comp.name}</h3>
                                    </div>
                                </div>
                                <p className="component-description">{comp.description}</p>

                                <div className={`component-details ${selectedComponent === comp.id ? 'expanded' : ''}`}>
                                    <div className="details-list">
                                        <h4>What You Need to Know:</h4>
                                        <ul>
                                            {comp.details.map((detail, idx) => (
                                                <li key={idx}>{detail}</li>
                                            ))}
                                        </ul>
                                    </div>
                                    <div className="key-factors">
                                        <h4>Key Factors:</h4>
                                        <div className="factors-grid">
                                            {comp.keyFactors.map((factor, idx) => (
                                                <span key={idx} className="factor-badge">{factor}</span>
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                <button className="learn-more-btn">
                                    {selectedComponent === comp.id ? (
                                        <>Show Less <ChevronDown className="inline ml-1" size={16} style={{ transform: 'rotate(180deg)' }} /></>
                                    ) : (
                                        <>Learn More <ChevronDown className="inline ml-1" size={16} /></>
                                    )}
                                </button>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="getting-started" id="guides">
                    <h2>Getting Started</h2>
                    <div className="steps">
                        {[
                            { title: 'Select Your CPU', desc: 'Choose from Intel or AMD processors' },
                            { title: 'Get Motherboard Suggestions', desc: "We'll show you compatible motherboards for your CPU socket" },
                            { title: 'Add Components', desc: 'RAM, GPU, PSU, and storage - all validated for compatibility' },
                            { title: 'Review & Build', desc: 'See your complete build with total cost and power requirements' }
                        ].map((step, idx) => (
                            <div key={idx} className="step">
                                <span className="step-number">{idx + 1}</span>
                                <div className="step-content">
                                    <h3>{step.title}</h3>
                                    <p>{step.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </main>

            <footer className="app-footer">
                <p>Built for Algolia Dev Challenge 2025</p>
                <p>Powered by Algolia • FastAPI • React</p>
            </footer>
        </div>
    )
}

export default App
