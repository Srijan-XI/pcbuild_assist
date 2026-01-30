import { liteClient as algoliasearch } from 'algoliasearch/lite'
import { InstantSearch, SearchBox, Hits, Highlight, Configure } from 'react-instantsearch'
import { X, Search as SearchIcon } from 'lucide-react'
import { useEffect, useMemo, useRef, useState } from 'react'
import { cn } from "@/lib/utils"

function buildAlgoliaSearchClient(applicationId, apiKey) {
    if (!applicationId || !apiKey) return null
    return algoliasearch(applicationId, apiKey)
}

function Hit({ hit, onSelect, attributes }) {
    // Extract values based on the attribute mapping provided in props
    const primaryText = attributes?.primaryText ? hit[attributes.primaryText] : hit.name
    // Secondary text could be brand or type if not specified
    const secondaryText = attributes?.secondaryText ? hit[attributes.secondaryText] : (hit.brand || hit.type)

    const price = Number(hit.price)
    const imageUrl = attributes?.image ? hit[attributes.image] : (hit.image || hit.img)

    return (
        <div
            onClick={() => onSelect && onSelect(hit)}
            className="p-3.5 hover:bg-gradient-to-r hover:from-blue-500/10 hover:to-indigo-500/5 cursor-pointer transition-all duration-200 rounded-xl border border-transparent hover:border-blue-500/30 group"
        >
            <div className="flex items-center gap-4">
                {imageUrl && (
                    <div className="h-12 w-12 flex-shrink-0 bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl overflow-hidden flex items-center justify-center shadow-lg group-hover:shadow-blue-500/20 transition-shadow">
                        <img src={imageUrl} alt={primaryText} className="h-full w-full object-cover" onError={(e) => e.target.style.display = 'none'} />
                    </div>
                )}
                <div className="flex-1 min-w-0">
                    <h3 className="text-white font-semibold text-sm truncate group-hover:text-blue-400 transition-colors">
                        {/* If we strictly follow attributes for highlighting, we'd need dynamic Highlight props. 
                For now, we'll try to highlight the primary text attribute if it matches known keys. */}
                        {attributes?.primaryText ? (
                            <Highlight attribute={attributes.primaryText} hit={hit} />
                        ) : (
                            <Highlight attribute="name" hit={hit} />
                        )}
                    </h3>
                    {secondaryText && (
                        <p className="text-slate-400 text-xs truncate mt-0.5">
                            {secondaryText}
                        </p>
                    )}
                </div>
                <div className="text-right flex-shrink-0">
                    {Number.isFinite(price) && (
                        <div className="text-emerald-400 font-bold text-sm">${price.toFixed(0)}</div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default function Search({
    applicationId,
    apiKey,
    indexName,
    attributes,
    filters,
    darkMode = false,
    onSelect,
    className
}) {
    const [isOpen, setIsOpen] = useState(false)
    const searchBoxRef = useRef(null)

    const searchClient = useMemo(
        () => buildAlgoliaSearchClient(applicationId, apiKey),
        [applicationId, apiKey]
    )

    const isAlgoliaConfigured = Boolean(searchClient)

    useEffect(() => {
        if (isOpen && searchBoxRef.current) {
            const input = searchBoxRef.current.querySelector('input')
            if (input) {
                input.focus()
            }
        }

        const handleEscape = (e) => {
            if (e.key === 'Escape' && isOpen) {
                setIsOpen(false)
            }
        }

        if (isOpen) {
            document.addEventListener('keydown', handleEscape)
            // Prevent body scroll when modal is open
            document.body.style.overflow = 'hidden'
        } else {
            document.body.style.overflow = 'unset'
        }

        return () => {
            document.removeEventListener('keydown', handleEscape)
            document.body.style.overflow = 'unset'
        }
    }, [isOpen])

    const handleSelect = (hit) => {
        if (onSelect) {
            onSelect(hit)
        }
        setIsOpen(false)
    }

    return (
        <div className={cn("relative w-full", className)}>
            <button
                onClick={() => setIsOpen(true)}
                className={cn(
                    "w-full flex items-center rounded-2xl px-6 py-4 text-left transition-all duration-300 outline-none group",
                    "bg-gradient-to-r from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-slate-700/50 text-slate-400 shadow-xl shadow-black/20",
                    "hover:from-slate-800 hover:to-slate-850 hover:border-blue-500/40 hover:text-slate-200 hover:shadow-blue-500/10 hover:shadow-2xl",
                    "focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50",
                    className
                )}
            >
                <div className="p-2 bg-blue-500/20 rounded-lg mr-4 group-hover:bg-blue-500/30 transition-colors">
                    <SearchIcon className="h-5 w-5 text-blue-400" />
                </div>
                {isAlgoliaConfigured ? (
                    <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Search for components...</span>
                ) : (
                    <span className="text-xs font-mono text-red-400 bg-red-500/10 px-2 py-0.5 rounded ml-auto">Algolia Not Configured</span>
                )}
                {isAlgoliaConfigured && (
                    <span className="ml-auto text-xs text-slate-500 font-mono bg-slate-700/50 px-3 py-1.5 rounded-lg border border-slate-600/50 group-hover:border-blue-500/30 group-hover:text-slate-300 transition-all">⌘K</span>
                )}
            </button>

            {isOpen && (
                <div className={cn("fixed inset-0 z-50 flex items-start justify-center sm:px-6 sm:pb-6 sm:pt-20", darkMode && "dark")}>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 bg-slate-950/90 backdrop-blur-md transition-opacity"
                        onClick={() => setIsOpen(false)}
                    />

                    {/* Search Modal */}
                    <div className="relative z-50 w-full max-w-2xl transform overflow-hidden rounded-3xl border bg-gradient-to-b from-slate-900 to-slate-950 shadow-2xl shadow-black/50 transition-all border-slate-700/50">
                        {isAlgoliaConfigured ? (
                            <InstantSearch searchClient={searchClient} indexName={indexName}>
                                <Configure hitsPerPage={8} filters={filters} />

                                {/* Header */}
                                <div className="flex items-center border-b border-slate-700/50 px-5 bg-slate-900/50" ref={searchBoxRef}>
                                    <div className="p-2 bg-blue-500/20 rounded-lg mr-3">
                                        <SearchIcon className="h-5 w-5 text-blue-400" />
                                    </div>
                                    <SearchBox
                                        placeholder="Type to search components..."
                                        classNames={{
                                            root: 'flex-1 h-16',
                                            form: 'relative h-full',
                                            input: 'w-full h-full bg-transparent border-none text-base text-white outline-none placeholder:text-slate-500 focus:ring-0 px-2 font-medium',
                                            submit: 'hidden',
                                            reset: 'hidden',
                                            loadingIndicator: 'hidden',
                                        }}
                                    />
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        className="ml-2 rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-bold uppercase text-slate-400 hover:bg-slate-700 hover:text-white transition-all border border-slate-700"
                                    >
                                        Esc
                                    </button>
                                </div>

                                {/* Results */}
                                <div className="max-h-[60vh] overflow-y-auto p-3">
                                    <Hits
                                        hitComponent={({ hit }) => <Hit hit={hit} onSelect={handleSelect} attributes={attributes} />}
                                        classNames={{
                                            root: 'space-y-1',
                                            list: 'space-y-1',
                                            item: 'list-none',
                                        }}
                                    />
                                    <div className="px-2 py-6 text-center text-sm text-slate-500 flex items-center justify-center gap-2">
                                        <span>Powered by</span>
                                        <img src="https://www.algolia.com/doc/assets/algolia-logo-blue.svg" alt="Algolia" className="h-4 opacity-60" />
                                    </div>
                                </div>

                            </InstantSearch>
                        ) : (
                            <div className="p-6 text-center text-sm">
                                <p className="font-semibold text-destructive mb-2">Algolia Config Missing</p>
                                <p className="text-muted-foreground">Please check your environment variables.</p>
                                <button
                                    onClick={() => setIsOpen(false)}
                                    className="mt-4 px-4 py-2 bg-secondary rounded-md text-secondary-foreground text-xs"
                                >
                                    Close
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}
