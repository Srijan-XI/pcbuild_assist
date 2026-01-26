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
            className="p-3 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer transition-colors rounded-md border border-transparent hover:border-blue-500/30 group"
        >
            <div className="flex items-center gap-3">
                {imageUrl && (
                    <div className="h-10 w-10 flex-shrink-0 bg-slate-200 dark:bg-slate-700 rounded-md overflow-hidden flex items-center justify-center">
                        <img src={imageUrl} alt={primaryText} className="h-full w-full object-cover" onError={(e) => e.target.style.display = 'none'} />
                    </div>
                )}
                <div className="flex-1 min-w-0">
                    <h3 className="text-foreground font-medium text-sm truncate">
                        {/* If we strictly follow attributes for highlighting, we'd need dynamic Highlight props. 
                For now, we'll try to highlight the primary text attribute if it matches known keys. */}
                        {attributes?.primaryText ? (
                            <Highlight attribute={attributes.primaryText} hit={hit} />
                        ) : (
                            <Highlight attribute="name" hit={hit} />
                        )}
                    </h3>
                    {secondaryText && (
                        <p className="text-muted-foreground text-xs truncate">
                            {secondaryText}
                        </p>
                    )}
                </div>
                <div className="text-right flex-shrink-0">
                    {Number.isFinite(price) && (
                        <div className="text-foreground font-semibold text-sm">${price.toFixed(2)}</div>
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
                    "w-full flex items-center rounded-2xl px-5 py-4 text-left transition-all outline-none ring-offset-0",
                    "bg-slate-900/80 backdrop-blur-xl border border-white/10 text-slate-400 shadow-xl",
                    "hover:bg-slate-800 hover:border-blue-500/30 hover:text-slate-200 hover:shadow-blue-500/10",
                    "focus:ring-2 focus:ring-blue-500/50",
                    className
                )}
            >
                <SearchIcon className="mr-3 h-5 w-5 text-blue-500" />
                {isAlgoliaConfigured ? (
                    <span className="text-sm font-medium text-slate-300">Search for components...</span>
                ) : (
                    <span className="text-xs font-mono text-red-400 bg-red-500/10 px-2 py-0.5 rounded ml-auto">Algolia Not Configured</span>
                )}
                {isAlgoliaConfigured && <span className="ml-auto text-xs text-slate-500 font-mono bg-white/5 px-2 py-1 rounded border border-white/5">⌘K</span>}
            </button>

            {isOpen && (
                <div className={cn("fixed inset-0 z-50 flex items-start justify-center sm:px-6 sm:pb-6 sm:pt-24", darkMode && "dark")}>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity"
                        onClick={() => setIsOpen(false)}
                    />

                    {/* Search Modal */}
                    <div className="relative z-50 w-full max-w-lg transform overflow-hidden rounded-2xl border bg-card text-card-foreground shadow-2xl transition-all border-white/10">
                        {isAlgoliaConfigured ? (
                            <InstantSearch searchClient={searchClient} indexName={indexName}>
                                <Configure hitsPerPage={8} filters={filters} />

                                {/* Header */}
                                <div className="flex items-center border-b px-3" ref={searchBoxRef}>
                                    <SearchIcon className="mr-2 h-4 w-4 shrink-0 opacity-50" />
                                    <SearchBox
                                        placeholder="Type to search..."
                                        classNames={{
                                            root: 'flex-1 h-14',
                                            form: 'relative h-full',
                                            input: 'w-full h-full bg-transparent border-none text-sm outline-none placeholder:text-muted-foreground focus:ring-0 px-2',
                                            submit: 'hidden',
                                            reset: 'hidden',
                                            loadingIndicator: 'hidden',
                                        }}
                                    />
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        className="ml-2 rounded-md bg-secondary px-1.5 py-0.5 text-xs font-semibold uppercase text-secondary-foreground hover:bg-secondary/80"
                                    >
                                        Esc
                                    </button>
                                </div>

                                {/* Results */}
                                <div className="max-h-[60vh] overflow-y-auto p-2">
                                    <Hits
                                        hitComponent={({ hit }) => <Hit hit={hit} onSelect={handleSelect} attributes={attributes} />}
                                        classNames={{
                                            root: 'space-y-1',
                                            list: 'space-y-1',
                                            item: 'list-none',
                                        }}
                                    />
                                    <div className="px-2 py-4 text-center text-sm text-muted-foreground">
                                        <img src="https://www.algolia.com/doc/assets/algolia-logo-blue.svg" alt="Algolia" className="h-3 inline-block mr-1 opacity-50" />
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
