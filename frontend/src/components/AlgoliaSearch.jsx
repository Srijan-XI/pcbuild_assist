import { liteClient as algoliasearch } from 'algoliasearch/lite'
import { InstantSearch, SearchBox, Hits, Highlight, Configure } from 'react-instantsearch'
import { X } from 'lucide-react'

const APP_ID = import.meta.env.VITE_ALGOLIA_APP_ID
const SEARCH_KEY = import.meta.env.VITE_ALGOLIA_SEARCH_KEY

const searchClient = algoliasearch(APP_ID, SEARCH_KEY)

function Hit({ hit, onSelect }) {
  return (
    <div
      onClick={() => onSelect(hit)}
      className="p-4 hover:bg-slate-800/50 cursor-pointer transition-colors rounded-lg border border-transparent hover:border-blue-500/30"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-white font-semibold text-sm mb-1 truncate">
            <Highlight attribute="name" hit={hit} />
          </h3>
          {hit.brand && (
            <p className="text-slate-400 text-xs mb-1">
              <Highlight attribute="brand" hit={hit} />
            </p>
          )}
          {hit.type && (
            <span className="inline-block text-xs text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded">
              {hit.type}
            </span>
          )}
        </div>
        <div className="text-right flex-shrink-0">
          {hit.price && (
            <div className="text-white font-bold text-sm">${hit.price.toFixed(2)}</div>
          )}
          {hit.socket && (
            <div className="text-slate-500 text-xs mt-1">{hit.socket}</div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function AlgoliaSearch({
  applicationId = APP_ID,
  apiKey = SEARCH_KEY,
  indexName = 'pc_components',
  onSelectComponent,
  componentType,
  darkMode = true
}) {
  const [isOpen, setIsOpen] = useState(false)
  const searchBoxRef = useRef(null)

  useEffect(() => {
    if (isOpen && searchBoxRef.current) {
      const input = searchBoxRef.current.querySelector('input')
      if (input) {
        input.focus()
      }
    }

    // Add ESC key listener
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen])

  const handleSelect = (hit) => {
    if (onSelectComponent) {
      onSelectComponent(hit)
    }
    setIsOpen(false)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(true)}
        className="w-full bg-slate-900/60 border border-white/10 rounded-xl px-4 py-3 text-left text-slate-400 hover:border-blue-500/50 transition-all focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20"
      >
        Search with Algolia {componentType ? `(${componentType})` : ''}...
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
            onClick={() => setIsOpen(false)}
          />

          {/* Search Modal */}
          <div className="fixed inset-x-4 top-20 md:left-1/2 md:-translate-x-1/2 md:max-w-2xl z-50 bg-slate-900/95 backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl max-h-[70vh] flex flex-col">
            <InstantSearch searchClient={searchClient} indexName={indexName}>
              <Configure
                hitsPerPage={10}
                {...(componentType && { filters: `type:${componentType}` })}
              />

              {/* Header */}
              <div className="p-4 border-b border-white/10 flex items-center gap-3">
                <div className="flex-1" ref={searchBoxRef}>
                  <SearchBox
                    placeholder={`Search ${componentType || 'components'}...`}
                    classNames={{
                      root: 'w-full',
                      form: 'relative',
                      input: 'w-full bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20',
                      submit: 'absolute left-3 top-1/2 -translate-y-1/2 hidden',
                      reset: 'absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white',
                      loadingIndicator: 'absolute right-12 top-1/2 -translate-y-1/2',
                    }}
                  />
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                >
                  <X size={20} />
                </button>
              </div>

              {/* Results */}
              <div className="flex-1 overflow-y-auto p-4">
                <Hits
                  hitComponent={({ hit }) => <Hit hit={hit} onSelect={handleSelect} />}
                  classNames={{
                    root: 'space-y-2',
                    list: 'space-y-2',
                    item: 'list-none',
                  }}
                />
              </div>

              {/* Footer */}
              <div className="p-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-500">
                <span>Powered by Algolia</span>
                <span>Press ESC to close</span>
              </div>
            </InstantSearch>
          </div>
        </>
      )}
    </div>
  )
}
