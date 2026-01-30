import { useState, useEffect } from 'react'
import {
    Cpu, Menu, Search as SearchIcon, ChevronDown,
    Monitor, Gamepad2, CircuitBoard, MemoryStick,
    Plug, HardDrive, Rocket, CheckCircle, Lightbulb,
    Zap, Shield, ArrowRight, Star, X, Github, Twitter, Plus
} from 'lucide-react'
import Builder from './Builder'
import Search from "@/components/search"
import './css/App.css'
import './css/components-education.css'
import './css/builder-styles.css'
import './css/tailwind-fallback.css'
import './css/ui-enhancements.css'

// PC Component educational data with images
const componentInfo = [
    {
        id: 'cpu',
        name: 'CPU (Processor)',
        icon: Cpu,
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
        icon: Gamepad2,
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
        icon: CircuitBoard,
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
        icon: MemoryStick,
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
        icon: Plug,
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
        icon: HardDrive,
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
    const [scrolled, setScrolled] = useState(false)

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20)
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [])

    const menuItems = [
        { label: 'Builder', onClick: () => { onNavigate('builder'); setMobileMenuOpen(false) } },
        { label: 'Learn', onClick: () => { document.querySelector('#learn')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false) } },
        { label: 'Guides', onClick: () => { document.querySelector('#guides')?.scrollIntoView({ behavior: 'smooth' }); setMobileMenuOpen(false) } },
        { label: 'Community', onClick: () => { setMobileMenuOpen(false) } }
    ]

    return (
        <nav className={`fixed w-full z-40 transition-all duration-300 ${scrolled ? 'bg-slate-950/95 backdrop-blur-xl shadow-lg shadow-black/20' : 'bg-slate-950/80 backdrop-blur-md'} border-b border-white/5`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20">
                    <div className="flex items-center space-x-3 cursor-pointer group" onClick={() => onNavigate('home')}>
                        <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl shadow-lg shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-all group-hover:scale-105">
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
                                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all duration-200 relative group"
                            >
                                {item.label}
                                <span className="absolute bottom-1 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-blue-500 group-hover:w-1/2 transition-all duration-200" />
                            </button>
                        ))}
                    </div>

                    <div className="flex items-center gap-3">
                        <button className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900/80 border border-white/10 text-slate-400 hover:text-white hover:border-white/20 hover:bg-slate-800/80 transition-all text-sm group shadow-lg">
                            <SearchIcon size={16} className="group-hover:text-blue-400 transition-colors" />
                            <span className="mr-6">Search...</span>
                            <kbd className="pointer-events-none hidden h-5 select-none items-center gap-1 rounded border border-white/10 bg-white/5 px-1.5 font-mono text-[10px] font-medium text-slate-400 sm:flex">
                                <span className="text-xs">⌘</span>K
                            </kbd>
                        </button>
                        <button className="md:hidden p-2.5 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
                            <SearchIcon size={20} />
                        </button>
                        <button 
                            className="md:hidden p-2.5 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-all" 
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            {mobileMenuOpen ? <X /> : <Menu />}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="md:hidden absolute top-20 left-0 right-0 bg-slate-900/98 backdrop-blur-xl border-b border-white/10 shadow-2xl animate-in slide-in-from-top-2 duration-200">
                        <div className="px-4 py-4 space-y-1">
                            {menuItems.map((item) => (
                                <button
                                    key={item.label}
                                    onClick={item.onClick}
                                    className="w-full text-left px-4 py-3 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-xl transition-all flex items-center justify-between group"
                                >
                                    {item.label}
                                    <ArrowRight size={16} className="text-slate-600 group-hover:text-blue-400 group-hover:translate-x-1 transition-all" />
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
                <h1 className="flex items-center justify-center gap-3">
                    <Monitor className="text-blue-500" size={40} />
                    PCBuild Assist
                </h1>
                <p>Smart PC Component Builder with Algolia</p>
                <div className="status">
                    API Status: <span className={`status-badge ${apiStatus === 'checking' ? 'checking' : apiStatus}`}>
                        {isCheckingApi ? 'Checking...' : apiStatus}
                    </span>
                </div>
            </header>

            <main className="app-main">
                <section className="hero">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-6">
                        <Zap size={14} className="animate-pulse" />
                        <span>Powered by Algolia Instant Search</span>
                    </div>
                    
                    <h2 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight mb-4">
                        Build Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">Perfect PC</span>
                    </h2>
                    <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto">
                        Get intelligent component suggestions with real-time compatibility checking
                    </p>

                    <div className="features mt-16">
                        <div className="feature group">
                            <span className="icon-wrapper bg-blue-500/10 p-5 rounded-2xl mb-6 inline-block group-hover:bg-blue-500/20 group-hover:scale-110 transition-all duration-300">
                                <SearchIcon className="text-blue-500" size={36} />
                            </span>
                            <h3 className="text-xl font-bold mb-3">Smart Search</h3>
                            <p className="text-slate-400">Find components instantly with Algolia-powered search featuring typo-tolerance and faceted filtering</p>
                        </div>
                        <div className="feature group">
                            <span className="icon-wrapper bg-green-500/10 p-5 rounded-2xl mb-6 inline-block group-hover:bg-green-500/20 group-hover:scale-110 transition-all duration-300">
                                <Shield className="text-green-500" size={36} />
                            </span>
                            <h3 className="text-xl font-bold mb-3">Compatibility Check</h3>
                            <p className="text-slate-400">Automatic validation of socket, memory type, and power requirements in real-time</p>
                        </div>
                        <div className="feature group">
                            <span className="icon-wrapper bg-purple-500/10 p-5 rounded-2xl mb-6 inline-block group-hover:bg-purple-500/20 group-hover:scale-110 transition-all duration-300">
                                <Star className="text-purple-500" size={36} />
                            </span>
                            <h3 className="text-xl font-bold mb-3">Smart Suggestions</h3>
                            <p className="text-slate-400">Get compatible component recommendations based on your selections and budget</p>
                        </div>
                    </div>

                    <div className="max-w-xl mx-auto mt-16 mb-10">
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
                        className="search-btn group flex items-center justify-center gap-3"
                    >
                        <Rocket size={22} className="group-hover:rotate-12 transition-transform" /> 
                        <span>Start Building Now</span>
                        <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                    </button>
                    
                    {/* Trust indicators */}
                    <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500">
                        <span className="flex items-center gap-2">
                            <CheckCircle size={16} className="text-green-500" />
                            1000+ Components
                        </span>
                        <span className="flex items-center gap-2">
                            <Zap size={16} className="text-yellow-500" />
                            Instant Results
                        </span>
                        <span className="flex items-center gap-2">
                            <Shield size={16} className="text-blue-500" />
                            Compatibility Verified
                        </span>
                    </div>
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
                                    <div className="component-image-wrapper relative flex items-center justify-center bg-slate-800 rounded-lg overflow-hidden">
                                        <img
                                            src={comp.image}
                                            alt={comp.name}
                                            className="component-image"
                                            onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
                                        />
                                        {/* Fallback Icon (hidden by default, shown on error) */}
                                        <div className="absolute inset-0 hidden items-center justify-center bg-slate-800 text-slate-400">
                                            <comp.icon size={64} strokeWidth={1} />
                                        </div>
                                    </div>
                                    <div className="component-title">
                                        <span className="component-icon text-blue-400">
                                            <comp.icon size={24} />
                                        </span>
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
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium mb-6">
                        <Lightbulb size={14} />
                        <span>Quick Start Guide</span>
                    </div>
                    <h2 className="text-3xl md:text-4xl font-bold mb-4">Getting Started</h2>
                    <p className="text-slate-400 mb-12 max-w-xl mx-auto">Build your dream PC in 4 simple steps</p>
                    <div className="steps">
                        {[
                            { title: 'Select Your CPU', desc: 'Choose from Intel or AMD processors', icon: Cpu, color: 'blue' },
                            { title: 'Get Motherboard Suggestions', desc: "We'll show you compatible motherboards for your CPU socket", icon: HardDrive, color: 'green' },
                            { title: 'Add Components', desc: 'RAM, GPU, PSU, and storage - all validated for compatibility', icon: Plus, color: 'purple' },
                            { title: 'Review & Build', desc: 'See your complete build with total cost and power requirements', icon: CheckCircle, color: 'orange' }
                        ].map((step, idx) => {
                            const IconComponent = step.icon
                            return (
                                <div key={idx} className="step group">
                                    <div className={`step-number bg-${step.color}-500/20 text-${step.color}-400 group-hover:bg-${step.color}-500 group-hover:text-white`}>
                                        <IconComponent size={20} />
                                    </div>
                                    <div className="step-content">
                                        <h3 className="font-semibold text-lg mb-1">{step.title}</h3>
                                        <p className="text-slate-400 text-sm">{step.desc}</p>
                                    </div>
                                    {idx < 3 && <div className="step-connector" />}
                                </div>
                            )
                        })}
                    </div>
                    
                    <button
                        onClick={() => setCurrentPage('builder')}
                        className="mt-12 px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 rounded-xl font-semibold text-white flex items-center gap-3 mx-auto shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 transition-all group"
                    >
                        <Rocket size={20} className="group-hover:rotate-12 transition-transform" />
                        Start Building
                        <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                    </button>
                </section>
            </main>

            <footer className="app-footer">
                <div className="footer-content">
                    <div className="footer-brand">
                        <div className="flex items-center gap-2 mb-4">
                            <Monitor className="text-blue-500" size={24} />
                            <span className="text-xl font-bold">
                                PCBuild<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Assist</span>
                            </span>
                        </div>
                        <p className="text-slate-500 text-sm">Smart PC Component Builder powered by Algolia's instant search technology.</p>
                    </div>
                    
                    <div className="footer-links">
                        <div className="footer-column">
                            <h4 className="text-sm font-semibold text-white mb-4">Quick Links</h4>
                            <ul className="space-y-2 text-sm text-slate-400">
                                <li><button onClick={() => setCurrentPage('builder')} className="hover:text-blue-400 transition-colors">Builder</button></li>
                                <li><a href="#learn" className="hover:text-blue-400 transition-colors">Learn Components</a></li>
                                <li><a href="#guides" className="hover:text-blue-400 transition-colors">Getting Started</a></li>
                            </ul>
                        </div>
                        <div className="footer-column">
                            <h4 className="text-sm font-semibold text-white mb-4">Technologies</h4>
                            <ul className="space-y-2 text-sm text-slate-400">
                                <li>Algolia InstantSearch</li>
                                <li>React + Vite</li>
                                <li>FastAPI Backend</li>
                                <li>TailwindCSS</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div className="footer-bottom">
                    <p className="text-slate-500 text-sm">Built for Algolia Dev Challenge 2025</p>
                    <div className="flex items-center gap-4">
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-500 hover:text-white transition-colors">
                            <Github size={20} />
                        </a>
                        <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-slate-500 hover:text-white transition-colors">
                            <Twitter size={20} />
                        </a>
                    </div>
                </div>
            </footer>
        </div>
    )
}

export default App
