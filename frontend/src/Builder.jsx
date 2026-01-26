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
        <div className="flex flex-col lg:flex-row max-w-7xl mx-auto pt-24 lg:pt-32 min-h-screen relative z-10">
            <main className="flex-1 px-4 sm:px-6 lg:px-8 pb-24 lg:pb-12">

                {/* Header Section */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
                    <div>
                        <h1 className="text-3xl lg:text-4xl font-extrabold text-white tracking-tight flex items-center gap-3">
                            <Layers className="text-blue-500" />
                            System <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Builder</span>
                        </h1>
                        <p className="text-slate-400 text-sm mt-1">Assemble your ultimate gaming rig.</p>
                    </div>

                    <div className="flex items-center gap-3">
                        {/* Status Indicators */}
                        {compatibilityIssues.length > 0 ? (
                            <div className="bg-red-500/10 border border-red-500/20 rounded-full px-3 py-1 flex items-center text-red-400 text-xs font-medium animate-pulse">
                                <AlertCircle size={14} className="mr-1.5" />
                                <span>{compatibilityIssues[0].msg.substring(0, 30)}...</span>
                            </div>
                        ) : Object.keys(build).length > 0 ? (
                            <div className="hidden md:flex bg-emerald-500/10 border border-emerald-500/20 rounded-full px-3 py-1 items-center text-emerald-400 text-xs font-medium">
                                <CheckCircle size={14} className="mr-1.5" />
                                <span>Compatible</span>
                            </div>
                        ) : null}

                        <button
                            onClick={onBackHome}
                            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm rounded-lg transition-colors border border-white/5"
                        >
                            Back Home
                        </button>
                    </div>
                </div>

                {/* Search & Filter Toolbar */}
                <div className="mb-8 space-y-6">
                    {/* Algolia Global Search */}
                    <div className="w-full relative z-30">
                        <Search
                            applicationId={import.meta.env.VITE_ALGOLIA_APP_ID}
                            apiKey={import.meta.env.VITE_ALGOLIA_SEARCH_KEY}
                            indexName={import.meta.env.VITE_ALGOLIA_INDEX_NAME || 'pc_components'}
                            attributes={{
                                primaryText: "name",
                                secondaryText: "brand",
                                ternaryText: "price",
                                url: "",
                                image: "image"
                            }}
                            filters={`type:"${activeCategory}"`}
                            darkMode={true}
                            onSelect={(hit) => togglePart(activeCategory, hit)}
                            className="shadow-2xl"
                        />
                    </div>

                    {/* Local Filter & Category Nav Row */}
                    <div className="flex flex-col xl:flex-row gap-4">
                        {/* Category Nav - Scrollable */}
                        <div className="flex-1 overflow-x-auto pb-4 -mx-4 px-4 xl:mx-0 xl:px-0 xl:pb-0 scrollbar-hide">
                            <div className="flex space-x-2 min-w-max">
                                {CATEGORIES.map((cat) => {
                                    const Icon = cat.icon
                                    const isSelected = build[cat.key]
                                    const isActive = activeCategory === cat.key

                                    return (
                                        <button
                                            key={cat.key}
                                            onClick={() => setActiveCategory(cat.key)}
                                            className={`
                                                flex items-center space-x-2 px-5 py-3 rounded-xl transition-all duration-200 border select-none
                                                ${isActive
                                                    ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-500/25 scale-105'
                                                    : isSelected
                                                        ? 'bg-slate-800 border-green-500/50 text-green-400 shadow-[inset_0_0_10px_rgba(74,222,128,0.1)]'
                                                        : 'bg-slate-900/60 border-white/5 text-slate-400 hover:bg-slate-800 hover:text-slate-200 hover:border-white/10'
                                                }
                                            `}
                                        >
                                            <Icon size={18} />
                                            <span className="text-sm font-semibold">{cat.label}</span>
                                            {isSelected && !isActive && <span className="flex h-2 w-2 rounded-full bg-green-500 ml-1.5 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>}
                                        </button>
                                    )
                                })}
                            </div>
                        </div>

                        {/* Local Filter Input */}
                        <div className="relative xl:w-72 flex-shrink-0">
                            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                            <input
                                type="text"
                                placeholder={`Filter ${activeCategory} results...`}
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full bg-slate-900/80 backdrop-blur-sm border border-white/10 rounded-xl pl-11 pr-10 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all shadow-lg"
                            />
                            {searchTerm && (
                                <button
                                    onClick={() => setSearchTerm('')}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-slate-500 hover:text-white hover:bg-white/10 rounded-full transition-colors"
                                >
                                    <X size={14} />
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                {error && (
                    <div className="mb-8 bg-red-950/30 border border-red-500/20 rounded-2xl p-4 flex items-start shadow-lg">
                        <AlertCircle size={20} className="mr-3 mt-0.5 text-red-400 flex-shrink-0" />
                        <div>
                            <p className="text-red-400 font-bold mb-1">Error Loading Components</p>
                            <p className="text-red-300/70 text-sm">{error}</p>
                        </div>
                    </div>
                )}

                {loading ? (
                    <div className="text-center py-20">
                        <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent"></div>
                        <p className="mt-4 text-slate-400 text-sm font-medium">Loading {activeCategory}s...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                        {filteredComponents.map(part => {
                            const isSelected = build[activeCategory]?.id === part.id
                            const specs = part.specs || {}
                            const reviews = part.reviews || []
                            const reviewCount = part.review_count || reviews.length || 0

                            // Helper to render spec badge
                            const SpecBadge = ({ label, value, icon: Icon }) => (
                                value ? (
                                    <div className="flex items-center text-[10px] text-slate-300 bg-slate-800/80 px-2 py-1 rounded border border-white/5">
                                        {Icon && <Icon size={10} className="mr-1.5 text-slate-400" />}
                                        <span className="opacity-70 mr-1">{label}:</span>
                                        <span className="font-semibold text-white">{value}</span>
                                    </div>
                                ) : null
                            )

                            return (
                                <div key={part.id} className={`relative group p-4 rounded-2xl border transition-all duration-300
                                    ${isSelected
                                        ? 'bg-blue-600/5 border-blue-500/50 shadow-[0_0_20px_rgba(37,99,235,0.1)]'
                                        : 'bg-slate-900/40 border-white/5 hover:border-white/10 hover:bg-slate-800/60'}`}
                                >
                                    <div className="flex justify-between items-start mb-3">
                                        <div className={`h-12 w-12 rounded-lg flex items-center justify-center text-slate-300 relative overflow-hidden
                                            ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800'}`}>
                                            {part.image ? (
                                                <img src={part.image} alt={part.name} className="h-full w-full object-cover" />
                                            ) : (
                                                <Box size={24} strokeWidth={1.5} />
                                            )}
                                        </div>
                                        <div className="text-right">
                                            <span className="block text-xl font-bold text-white tracking-tight">${part.price?.toFixed(2) || 'N/A'}</span>
                                            {part.tdp && (
                                                <span className="inline-flex items-center justify-end mt-1 px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-500 text-[10px] font-bold uppercase tracking-wider border border-yellow-500/20">
                                                    <Zap size={10} className="mr-1 fill-yellow-500" /> {part.tdp}W
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    <div className="mb-4 min-h-[4rem]">
                                        <h3 className="text-base font-bold text-white mb-2 leading-snug group-hover:text-blue-400 transition-colors line-clamp-2">{part.name}</h3>

                                        {/* Specs Grid */}
                                        <div className="flex flex-wrap gap-1.5 mb-2">
                                            <span className="text-[10px] text-white/50 bg-white/5 px-1.5 py-0.5 rounded border border-white/5 uppercase tracking-wide font-bold">
                                                {part.brand || 'Generic'}
                                            </span>

                                            {/* Dynamic Specs based on Category */}
                                            {activeCategory === 'CPU' && (
                                                <>
                                                    <SpecBadge label="Cores" value={specs.core_count} />
                                                    <SpecBadge label="Clock" value={specs.core_clock} />
                                                    <SpecBadge label="Socket" value={specs.socket} />
                                                </>
                                            )}
                                            {activeCategory === 'GPU' && (
                                                <>
                                                    <SpecBadge label="Memory" value={specs.memory} />
                                                    <SpecBadge label="Chipset" value={specs.chipset} />
                                                    <SpecBadge label="Boost" value={specs.boost_clock} />
                                                </>
                                            )}
                                            {activeCategory === 'Motherboard' && (
                                                <>
                                                    <SpecBadge label="Socket" value={specs.socket} />
                                                    <SpecBadge label="Form" value={specs.form_factor} />
                                                    <SpecBadge label="Mem" value={specs.memory_type} />
                                                </>
                                            )}
                                            {activeCategory === 'RAM' && (
                                                <>
                                                    <SpecBadge label="Speed" value={specs.speed} />
                                                    <SpecBadge label="Modules" value={specs.modules} />
                                                    <SpecBadge label="Type" value={specs.type} />
                                                </>
                                            )}
                                            {activeCategory === 'Storage' && (
                                                <>
                                                    <SpecBadge label="Capacity" value={specs.capacity} />
                                                    <SpecBadge label="Type" value={specs.type} />
                                                    <SpecBadge label="Cache" value={specs.cache} />
                                                </>
                                            )}
                                            {activeCategory === 'PSU' && (
                                                <>
                                                    <SpecBadge label="Watts" value={specs.wattage ? `${specs.wattage}W` : null} />
                                                    <SpecBadge label="Eff" value={specs.efficiency} />
                                                    <SpecBadge label="Mod" value={specs.modular} />
                                                </>
                                            )}
                                        </div>

                                        {/* Review Snippet */}
                                        {reviewCount > 0 && (
                                            <div className="mt-3 pt-3 border-t border-white/5">
                                                <div className="flex items-center gap-1.5 mb-1.5">
                                                    <div className="flex">
                                                        {[1, 2, 3, 4, 5].map(i => (
                                                            <svg key={i} className="w-3 h-3 text-yellow-500 fill-current" viewBox="0 0 20 20">
                                                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                            </svg>
                                                        ))}
                                                    </div>
                                                    <span className="text-xs text-slate-400">({reviewCount} reviews)</span>
                                                </div>
                                                {reviews[0]?.text && (
                                                    <p className="text-xs text-slate-400 italic line-clamp-2">"{reviews[0].text.substring(0, 100)}..."</p>
                                                )}
                                            </div>
                                        )}
                                    </div>

                                    <button
                                        onClick={() => togglePart(activeCategory, part)}
                                        className={`w-full py-2.5 rounded-lg font-bold text-sm transition-all flex items-center justify-center
                                            ${isSelected
                                                ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20'
                                                : 'bg-white/5 text-white hover:bg-blue-600 hover:shadow-lg hover:shadow-blue-500/20'
                                            }`}
                                    >
                                        {isSelected ? (
                                            <>
                                                <Trash2 size={16} className="mr-2" /> Remove
                                            </>
                                        ) : (
                                            <>
                                                <Plus size={16} className="mr-2" /> Add
                                            </>
                                        )}
                                    </button>
                                </div>
                            )
                        })}
                    </div>
                )
                }

                {
                    filteredComponents.length === 0 && !loading && (
                        <div className="mt-8 text-center py-16 border border-dashed border-slate-800 rounded-2xl bg-slate-900/20">
                            <div className="inline-flex bg-slate-800/50 p-4 rounded-full mb-4">
                                {searchTerm ? <SearchIcon size={32} className="text-slate-600" /> : <Filter size={32} className="text-slate-600" />}
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">
                                {searchTerm ? 'No Results Found' : 'No Components Found'}
                            </h3>
                            <p className="text-slate-500 text-sm max-w-sm mx-auto">
                                {searchTerm
                                    ? `No matches for "${searchTerm}" in ${activeCategory}.`
                                    : `We couldn't find any ${activeCategory} components. Check your API connection.`
                                }
                            </p>
                            {searchTerm && (
                                <button
                                    onClick={() => setSearchTerm('')}
                                    className="mt-4 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-sm rounded-lg transition-colors"
                                >
                                    Clear Filters
                                </button>
                            )}
                        </div>
                    )
                }
            </main >

            <div className="flex-shrink-0 lg:w-80 border-l border-white/5 bg-slate-950/30">
                <BuildSummary
                    build={build}
                    totalCost={totalCost}
                    totalPower={totalPower}
                    onRemove={removePart}
                    onClear={clearBuild}
                    compatibilityIssues={compatibilityIssues}
                />
            </div>
        </div >
    )
}

export default Builder
