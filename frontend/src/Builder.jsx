import { useState, useEffect } from 'react'
import {
    Cpu, Monitor, HardDrive, Layers, Zap, Box, Trash2, CheckCircle, AlertCircle,
    ShoppingCart, X, Plus, Info, ChevronRight, Search as SearchIcon, Filter
} from 'lucide-react'
import Search from "@/components/search"
import './css/algolia-search.css'

const CATEGORIES = [
    { key: 'CPU', label: 'CPU', icon: Cpu },
    { key: 'Motherboard', label: 'Motherboard', icon: Layers },
    { key: 'GPU', label: 'GPU', icon: Monitor },
    { key: 'RAM', label: 'Memory', icon: Box },
    { key: 'Storage', label: 'Storage', icon: HardDrive },
    { key: 'PSU', label: 'Power Supply', icon: Zap },
]

const BuildSummary = ({ build, totalCost, totalPower, onRemove, onClear, compatibilityIssues }) => {
    const [isOpen, setIsOpen] = useState(false)
    const filledSlots = Object.keys(build).length
    const totalSlots = CATEGORIES.length
    const progress = (filledSlots / totalSlots) * 100

    return (
        <>
            {/* Mobile Toggle Button */}
            <button
                onClick={() => setIsOpen(true)}
                className="lg:hidden fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-full shadow-[0_4px_20px_rgba(79,70,229,0.5)] flex items-center space-x-2 border border-white/20"
                style={{ animation: filledSlots > 0 ? 'bounce 2s infinite' : 'none' }}
            >
                <ShoppingCart size={24} />
                {filledSlots > 0 && (
                    <span className="font-bold bg-white/20 px-2 py-0.5 rounded-full text-sm">${totalCost}</span>
                )}
            </button>

            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
                    onClick={() => setIsOpen(false)}
                />
            )}

            <div className={`
        fixed inset-y-0 right-0 z-50 w-full sm:w-[400px] clay-sidebar
        transform transition-all duration-500 cubic-bezier(0.4, 0, 0.2, 1)
        ${isOpen ? 'translate-x-0' : 'translate-x-full'} lg:translate-x-0 lg:static lg:h-[calc(100vh-100px)] lg:rounded-3xl lg:w-96 lg:block lg:sticky lg:top-24
      `}>
                <div className="h-full flex flex-col p-6">
                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h2 className="text-2xl font-bold text-white tracking-tight">Your Build</h2>
                            <p className="text-slate-400 text-sm mt-1">{filledSlots} of {totalSlots} components</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <button onClick={onClear} className="p-2 hover:bg-white/5 rounded-lg text-slate-400 hover:text-red-400 transition-colors" title="Clear Build">
                                <Trash2 size={18} />
                            </button>
                            <button onClick={() => setIsOpen(false)} className="lg:hidden p-2 hover:bg-white/5 rounded-lg text-slate-400">
                                <X size={24} />
                            </button>
                        </div>
                    </div>

                    <div className="mb-8 relative group">
                        <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-700 ease-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
                                style={{ width: `${progress}%` }}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="bg-slate-950/50 p-4 rounded-2xl border border-white/5">
                            <span className="text-xs text-slate-400 font-medium uppercase tracking-wider block mb-1">Total Cost</span>
                            <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-500">${totalCost}</span>
                        </div>
                        <div className="bg-slate-950/50 p-4 rounded-2xl border border-white/5">
                            <span className="text-xs text-slate-400 font-medium uppercase tracking-wider block mb-1">Est. Power</span>
                            <span className="text-2xl font-bold text-yellow-400 flex items-center">
                                {totalPower} <span className="text-sm text-yellow-500/70 ml-1">W</span>
                            </span>
                        </div>
                    </div>

                    {compatibilityIssues.length > 0 && (
                        <div className="mb-4 bg-red-500/10 border border-red-500/20 rounded-xl p-3">
                            <div className="flex items-start text-red-400 text-xs">
                                <AlertCircle size={14} className="mr-2 mt-0.5 flex-shrink-0" />
                                <div className="space-y-1">
                                    {compatibilityIssues.map((issue, idx) => (
                                        <p key={idx}>{issue.msg}</p>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex-1 overflow-y-auto pr-2 -mr-2 space-y-3 custom-scrollbar">
                        {CATEGORIES.map(cat => {
                            const part = build[cat.key]
                            const Icon = cat.icon

                            if (!part) {
                                return (
                                    <div key={cat.key} className="flex items-center p-3 rounded-xl border border-white/5 border-dashed text-slate-600 bg-white/[0.02]">
                                        <Icon size={16} className="mr-3" />
                                        <span className="text-sm font-medium">Add {cat.label}</span>
                                    </div>
                                )
                            }

                            return (
                                <div key={cat.key} className="group relative bg-slate-800/50 p-3 rounded-xl border border-white/5 hover:border-blue-500/30 transition-all hover:bg-slate-800">
                                    <div className="flex items-start">
                                        <div className="h-10 w-10 bg-slate-700/50 rounded-lg flex items-center justify-center mr-3 text-slate-400 flex-shrink-0">
                                            <Icon size={18} />
                                        </div>
                                        <div className="min-w-0 flex-1">
                                            <p className="text-[10px] text-blue-400 font-bold uppercase tracking-wider mb-0.5">{cat.label}</p>
                                            <p className="text-sm text-white font-medium truncate leading-tight">{part.name}</p>
                                            <p className="text-xs text-slate-400 mt-0.5">${part.price?.toFixed(2)}</p>
                                        </div>
                                        <button
                                            onClick={() => onRemove(cat.key)}
                                            className="absolute top-2 right-2 p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-md transition-all opacity-0 group-hover:opacity-100"
                                        >
                                            <X size={14} />
                                        </button>
                                    </div>
                                </div>
                            )
                        })}
                    </div>

                    <div className="pt-6 mt-4 border-t border-white/10">
                        <button className="w-full group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-900/20 transition-all active:scale-[0.98] flex items-center justify-center">
                            <span className="mr-2">Complete Build</span>
                            <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}

function Builder({ onBackHome }) {
    const [components, setComponents] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [build, setBuild] = useState({})
    const [activeCategory, setActiveCategory] = useState('CPU')
    const [compatibilityIssues, setCompatibilityIssues] = useState([])
    const [searchTerm, setSearchTerm] = useState('')
    const [filteredComponents, setFilteredComponents] = useState([])

    useEffect(() => {
        const issues = []
        if (build.CPU && build.Motherboard) {
            const cpuSocket = build.CPU.socket || build.CPU.specs?.socket
            const mbSocket = build.Motherboard.socket || build.Motherboard.specs?.socket
            if (cpuSocket && mbSocket && cpuSocket !== mbSocket) {
                issues.push({ level: 'error', msg: `Socket mismatch: CPU ${cpuSocket} vs MB ${mbSocket}` })
            }
        }
        if (build.Motherboard && build.RAM) {
            const mbMemType = build.Motherboard.memory_type || (build.Motherboard.specs?.memory_type)
            const ramType = build.RAM.type || build.RAM.specs?.type
            if (mbMemType && ramType && mbMemType !== ramType) {
                issues.push({ level: 'error', msg: `Memory type mismatch: ${mbMemType} vs ${ramType}` })
            }
        }
        setCompatibilityIssues(issues)
    }, [build])

    const searchComponents = async (type = 'CPU') => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch(`/api/components/type/${type}?limit=20`)

            if (!response.ok) {
                throw new Error(`Failed to fetch components (${response.status})`)
            }

            const data = await response.json()
            setComponents(data.results || [])
        } catch (error) {
            console.error('Search error:', error)
            setError(error.message || 'Failed to load components. Please check if the backend server is running.')
            setComponents([])
        } finally {
            setLoading(false)
        }
    }

    const togglePart = (category, part) => {
        setBuild(prev => {
            const newBuild = { ...prev }
            if (newBuild[category] && newBuild[category].id === part.id) {
                delete newBuild[category]
            } else {
                newBuild[category] = part
            }
            return newBuild
        })
    }

    const removePart = (category) => {
        setBuild(prev => {
            const newBuild = { ...prev }
            delete newBuild[category]
            return newBuild
        })
    }

    const clearBuild = () => setBuild({})

    const totalCost = Object.values(build).reduce((sum, part) => sum + (part.price || 0), 0)
    const totalPower = Object.values(build).reduce((sum, part) => sum + (part.tdp || part.power || 0), 0) + 50

    useEffect(() => {
        if (activeCategory) {
            searchComponents(activeCategory)
        }
    }, [activeCategory])

    useEffect(() => {
        if (searchTerm.trim() === '') {
            setFilteredComponents(components)
        } else {
            const filtered = components.filter(comp =>
                comp.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                comp.brand?.toLowerCase().includes(searchTerm.toLowerCase())
            )
            setFilteredComponents(filtered)
        }
    }, [searchTerm, components])



    return (
        <div className="flex flex-col lg:flex-row max-w-7xl mx-auto pt-24 lg:pt-28 min-h-screen relative z-10">
            <main className="flex-1 px-4 sm:px-6 lg:px-8 pb-24 lg:pb-12">
                <div className="mb-8 space-y-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl lg:text-5xl font-extrabold text-white tracking-tight mb-2">
                                System <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Builder</span>
                            </h1>
                            <p className="text-slate-400 text-lg">Assemble your ultimate gaming rig with real-time compatibility checking.</p>
                        </div>
                        <button
                            onClick={onBackHome}
                            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
                        >
                            ← Back to Home
                        </button>
                    </div>

                    <div className="flex flex-wrap gap-4 items-center min-h-[50px]">
                        {compatibilityIssues.length > 0 ? (
                            <div className="bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 flex items-center text-red-400 text-sm font-medium animate-pulse">
                                <AlertCircle size={18} className="mr-2.5" />
                                <span>{compatibilityIssues[0].msg}</span>
                            </div>
                        ) : Object.keys(build).length > 2 ? (
                            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-4 py-3 flex items-center text-emerald-400 text-sm font-medium">
                                <CheckCircle size={18} className="mr-2.5" />
                                <span>All parts compatible</span>
                            </div>
                        ) : (
                            <div className="flex items-center text-slate-500 text-sm bg-white/5 rounded-xl px-4 py-3">
                                <Info size={18} className="mr-2.5" />
                                Start by selecting a processor
                            </div>
                        )}
                    </div>
                </div>

                {error && (
                    <div className="mb-6 bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-start">
                        <AlertCircle size={20} className="mr-3 mt-0.5 text-red-400 flex-shrink-0" />
                        <div>
                            <p className="text-red-400 font-medium mb-1">Error Loading Components</p>
                            <p className="text-red-300/80 text-sm">{error}</p>
                        </div>
                    </div>
                )}

                <div className="mb-8">
                    <Search
                        applicationId={import.meta.env.VITE_ALGOLIA_APP_ID}
                        apiKey={import.meta.env.VITE_ALGOLIA_SEARCH_KEY}
                        indexName={import.meta.env.VITE_ALGOLIA_INDEX_NAME || 'pc_components'}
                        attributes={{
                            primaryText: "name",
                            secondaryText: "brand",
                            tertiaryText: "price",
                            url: "",
                            image: "image"
                        }}
                        filters={`type:"${activeCategory}"`}
                        darkMode={true}
                        onSelect={(hit) => togglePart(activeCategory, hit)}
                        className="shadow-lg"
                    />
                </div>

                <div className="mb-8">
                    <div className="relative">
                        <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                        <input
                            type="text"
                            placeholder={`Filter ${activeCategory} locally...`}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full bg-slate-900/60 border border-white/10 rounded-xl pl-12 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                        />
                        {searchTerm && (
                            <button
                                onClick={() => setSearchTerm('')}
                                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                            >
                                <X size={18} />
                            </button>
                        )}
                    </div>
                </div>

                <div className="sticky top-20 z-20 -mx-4 px-4 py-6 mb-8 bg-slate-950/90 backdrop-blur-xl border-y border-white/5 lg:static lg:bg-transparent lg:border-none lg:p-0 lg:mx-0 lg:mb-8">
                    <div className="flex overflow-x-auto gap-3 pb-2 scrollbar-hide snap-x">
                        {CATEGORIES.map((cat) => {
                            const Icon = cat.icon
                            const isSelected = build[cat.key]
                            const isActive = activeCategory === cat.key

                            return (
                                <button
                                    key={cat.key}
                                    onClick={() => setActiveCategory(cat.key)}
                                    className={`
                                        flex items-center space-x-3 px-5 py-3 rounded-2xl whitespace-nowrap transition-all duration-300 snap-start clay-category-btn
                                        ${isActive
                                            ? 'active text-white scale-105'
                                            : isSelected
                                                ? 'text-green-400 border-green-500/30 shadow-[inset_0_0_10px_rgba(74,222,128,0.1)]'
                                                : 'text-slate-400 hover:text-slate-200'
                                        }
                                    `}
                                >
                                    <Icon size={20} strokeWidth={isActive ? 2 : 1.5} />
                                    <span className={`font-medium ${isActive ? 'text-base' : 'text-sm'}`}>{cat.label}</span>
                                    {isSelected && !isActive && <div className="h-1.5 w-1.5 rounded-full bg-green-400 ml-1 animate-pulse" />}
                                </button>
                            )
                        })}
                    </div>
                </div>

                {loading ? (
                    <div className="text-center py-20">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                        <p className="mt-4 text-slate-400">Loading components...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
                        {filteredComponents.map(part => {
                            const isSelected = build[activeCategory]?.id === part.id
                            return (
                                <div key={part.id} className={`relative group p-5 transition-all duration-300 clay-card-interactive
                                    ${isSelected ? 'selected' : ''}`}
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className={`h-14 w-14 rounded-xl flex items-center justify-center text-slate-300 shadow-inner
                                            ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800'}`}>
                                            <Box size={28} strokeWidth={1.5} />
                                        </div>
                                        <div className="text-right">
                                            <span className="block text-2xl font-bold text-white tracking-tight">${part.price?.toFixed(2) || 'N/A'}</span>
                                            {part.tdp && (
                                                <span className="inline-flex items-center justify-end mt-1 px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-500 text-[10px] font-bold uppercase tracking-wider border border-yellow-500/20">
                                                    <Zap size={10} className="mr-1 fill-yellow-500" /> {part.tdp}W
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    <div className="mb-4">
                                        <h3 className="text-lg font-bold text-white mb-2 leading-tight group-hover:text-blue-400 transition-colors">{part.name}</h3>
                                        <div className="flex flex-wrap gap-2">
                                            <span className="text-xs text-slate-400 bg-slate-950/50 px-2 py-1 rounded border border-white/5">
                                                {part.brand || 'Unknown'}
                                            </span>
                                            {part.socket && (
                                                <span className="text-xs text-slate-400 bg-slate-950/50 px-2 py-1 rounded border border-white/5">
                                                    {part.socket}
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => togglePart(activeCategory, part)}
                                        className={`w-full py-3 rounded-xl font-bold text-sm tracking-wide transition-all shadow-lg flex items-center justify-center
                                            ${isSelected
                                                ? 'bg-red-500/10 text-red-500 border border-red-500/30 hover:bg-red-500/20 shadow-red-500/10'
                                                : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-500 hover:to-indigo-500 shadow-blue-500/20'
                                            }`}
                                    >
                                        {isSelected ? (
                                            <>
                                                <Trash2 size={16} className="mr-2" /> Remove
                                            </>
                                        ) : (
                                            <>
                                                <Plus size={16} className="mr-2" /> Add to Build
                                            </>
                                        )}
                                    </button>
                                </div>
                            )
                        })}
                    </div>
                )}

                {filteredComponents.length === 0 && !loading && (
                    <div className="mt-12 text-center py-20 border-2 border-dashed border-slate-800 rounded-3xl bg-slate-900/30">
                        <div className="inline-flex bg-slate-800/50 p-5 rounded-full mb-6">
                            {searchTerm ? <SearchIcon size={40} className="text-slate-600" /> : <Plus size={40} className="text-slate-600" />}
                        </div>
                        <h3 className="text-2xl font-bold text-white mb-2">
                            {searchTerm ? 'No Results Found' : 'No Components Found'}
                        </h3>
                        <p className="text-slate-400 max-w-md mx-auto">
                            {searchTerm
                                ? `No ${activeCategory} components match "${searchTerm}". Try a different search term.`
                                : 'Try selecting a different component category or check if the API is running.'
                            }
                        </p>
                        {searchTerm && (
                            <button
                                onClick={() => setSearchTerm('')}
                                className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
                            >
                                Clear Search
                            </button>
                        )}
                    </div>
                )}
            </main>

            <div className="flex-shrink-0 lg:w-96 lg:pl-8">
                <BuildSummary
                    build={build}
                    totalCost={totalCost}
                    totalPower={totalPower}
                    onRemove={removePart}
                    onClear={clearBuild}
                    compatibilityIssues={compatibilityIssues}
                />
            </div>
        </div>
    )
}

export default Builder
