import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  Monitor, 
  HardDrive, 
  Layers, 
  Zap, 
  Box, 
  Trash2, 
  CheckCircle, 
  AlertCircle, 
  ShoppingCart, 
  Menu, 
  X, 
  Plus, 
  Info,
  Save,
  RotateCcw,
  ChevronRight,
  Search
} from 'lucide-react';

// --- Mock Data ---
const PARTS_DB = {
  cpu: [
    { id: 'c1', name: 'Intel Core i9-14900K', price: 599, brand: 'Intel', specs: '24 Cores, 6.0 GHz', power: 253, image: 'cpu-intel' },
    { id: 'c2', name: 'AMD Ryzen 9 7950X3D', price: 649, brand: 'AMD', specs: '16 Cores, 5.7 GHz', power: 120, image: 'cpu-amd' },
    { id: 'c3', name: 'Intel Core i5-13600K', price: 319, brand: 'Intel', specs: '14 Cores, 5.1 GHz', power: 181, image: 'cpu-intel' },
    { id: 'c4', name: 'AMD Ryzen 7 7800X3D', price: 399, brand: 'AMD', specs: '8 Cores, 5.0 GHz', power: 120, image: 'cpu-amd' },
    { id: 'c5', name: 'Intel Core i3-13100F', price: 119, brand: 'Intel', specs: '4 Cores, 4.5 GHz', power: 89, image: 'cpu-intel' },
  ],
  gpu: [
    { id: 'g1', name: 'NVIDIA GeForce RTX 4090', price: 1599, brand: 'NVIDIA', specs: '24GB GDDR6X', power: 450, image: 'gpu-nvidia' },
    { id: 'g2', name: 'AMD Radeon RX 7900 XTX', price: 999, brand: 'AMD', specs: '24GB GDDR6', power: 355, image: 'gpu-amd' },
    { id: 'g3', name: 'NVIDIA GeForce RTX 4070', price: 599, brand: 'NVIDIA', specs: '12GB GDDR6X', power: 200, image: 'gpu-nvidia' },
    { id: 'g4', name: 'AMD Radeon RX 7600', price: 269, brand: 'AMD', specs: '8GB GDDR6', power: 165, image: 'gpu-amd' },
  ],
  motherboard: [
    { id: 'm1', name: 'ASUS ROG Maximus Z790', price: 699, brand: 'ASUS', specs: 'E-ATX, LGA1700, DDR5', image: 'mobo-asus' },
    { id: 'm2', name: 'MSI MAG B650 Tomahawk', price: 219, brand: 'MSI', specs: 'ATX, AM5, DDR5', image: 'mobo-msi' },
    { id: 'm3', name: 'Gigabyte B760M AORUS', price: 169, brand: 'Gigabyte', specs: 'mATX, LGA1700, DDR4', image: 'mobo-gigabyte' },
  ],
  ram: [
    { id: 'r1', name: 'G.Skill Trident Z5 RGB 32GB', price: 139, brand: 'G.Skill', specs: 'DDR5-6000 CL30', image: 'ram-gskill' },
    { id: 'r2', name: 'Corsair Vengeance 32GB', price: 99, brand: 'Corsair', specs: 'DDR5-5600 CL36', image: 'ram-corsair' },
    { id: 'r3', name: 'Kingston Fury Beast 16GB', price: 59, brand: 'Kingston', specs: 'DDR4-3200 CL16', image: 'ram-kingston' },
  ],
  storage: [
    { id: 's1', name: 'Samsung 990 PRO 2TB', price: 169, brand: 'Samsung', specs: 'NVMe Gen4, 7450 MB/s', image: 'ssd-samsung' },
    { id: 's2', name: 'WD_BLACK SN850X 1TB', price: 89, brand: 'Western Digital', specs: 'NVMe Gen4, 7300 MB/s', image: 'ssd-wd' },
    { id: 's3', name: 'Crucial P3 Plus 1TB', price: 59, brand: 'Crucial', specs: 'NVMe Gen4, 5000 MB/s', image: 'ssd-crucial' },
  ],
  psu: [
    { id: 'p1', name: 'Corsair RM1000x', price: 189, brand: 'Corsair', specs: '1000W 80+ Gold, Fully Modular', image: 'psu-corsair' },
    { id: 'p2', name: 'EVGA SuperNOVA 850 GT', price: 129, brand: 'EVGA', specs: '850W 80+ Gold, Fully Modular', image: 'psu-evga' },
    { id: 'p3', name: 'Thermaltake Smart 600W', price: 49, brand: 'Thermaltake', specs: '600W 80+ White', image: 'psu-tt' },
  ],
  case: [
    { id: 'case1', name: 'Lian Li O11 Dynamic Evo', price: 159, brand: 'Lian Li', specs: 'ATX Mid Tower, Dual Chamber', image: 'case-lianli' },
    { id: 'case2', name: 'NZXT H5 Flow', price: 94, brand: 'NZXT', specs: 'ATX Mid Tower, High Airflow', image: 'case-nzxt' },
    { id: 'case3', name: 'Fractal Design North', price: 139, brand: 'Fractal', specs: 'ATX Mid Tower, Wood Front', image: 'case-fractal' },
  ]
};

const CATEGORIES = [
  { key: 'cpu', label: 'CPU', icon: Cpu },
  { key: 'motherboard', label: 'Motherboard', icon: Layers },
  { key: 'gpu', label: 'GPU', icon: Monitor },
  { key: 'ram', label: 'Memory', icon: Box },
  { key: 'storage', label: 'Storage', icon: HardDrive },
  { key: 'psu', label: 'Power Supply', icon: Zap },
  { key: 'case', label: 'Case', icon: Box },
];

// --- Components ---

const PartCard = ({ part, onAdd, isSelected }) => (
  <div className={`relative group rounded-2xl p-5 border transition-all duration-300 backdrop-blur-sm
    ${isSelected 
      ? 'bg-blue-900/10 border-blue-500 shadow-[0_0_30px_rgba(59,130,246,0.15)] ring-1 ring-blue-500/50' 
      : 'bg-slate-900/60 border-white/5 hover:border-white/20 hover:bg-slate-800/80 hover:-translate-y-1 hover:shadow-xl'
    }`}
  >
    <div className="flex justify-between items-start mb-4">
      <div className={`h-14 w-14 rounded-xl flex items-center justify-center text-slate-300 shadow-inner
        ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800'}`}>
         <Box size={28} strokeWidth={1.5} />
      </div>
      <div className="text-right">
        <span className="block text-2xl font-bold text-white tracking-tight">${part.price}</span>
        {part.power && (
          <span className="inline-flex items-center justify-end mt-1 px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-500 text-[10px] font-bold uppercase tracking-wider border border-yellow-500/20">
            <Zap size={10} className="mr-1 fill-yellow-500" /> {part.power}W
          </span>
        )}
      </div>
    </div>
    
    <div className="mb-4">
      <h3 className="text-lg font-bold text-white mb-2 leading-tight group-hover:text-blue-400 transition-colors">{part.name}</h3>
      <div className="flex flex-wrap gap-2">
        {part.specs.split(', ').map((spec, i) => (
          <span key={i} className="text-xs text-slate-400 bg-slate-950/50 px-2 py-1 rounded border border-white/5">
            {spec}
          </span>
        ))}
      </div>
    </div>

    <button 
      onClick={() => onAdd(part)}
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
);

const CategorySelector = ({ activeCategory, setActiveCategory, buildState }) => (
  <div className="sticky top-20 z-20 -mx-4 px-4 py-4 mb-4 bg-slate-950/80 backdrop-blur-xl border-y border-white/5 lg:static lg:bg-transparent lg:border-none lg:p-0 lg:mx-0">
    <div className="flex overflow-x-auto gap-3 pb-2 scrollbar-hide snap-x">
      {CATEGORIES.map((cat) => {
        const Icon = cat.icon;
        const isSelected = buildState[cat.key];
        const isActive = activeCategory === cat.key;
        
        return (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className={`
              flex items-center space-x-3 px-5 py-3 rounded-2xl whitespace-nowrap transition-all duration-300 snap-start border
              ${isActive 
                ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-900/50 scale-105' 
                : isSelected 
                  ? 'bg-slate-900 border-green-500/30 text-green-400 shadow-[0_0_10px_rgba(74,222,128,0.1)]' 
                  : 'bg-slate-900 border-white/5 text-slate-400 hover:bg-slate-800 hover:border-slate-700 hover:text-slate-200'
              }
            `}
          >
            <Icon size={20} strokeWidth={isActive ? 2 : 1.5} />
            <span className={`font-medium ${isActive ? 'text-base' : 'text-sm'}`}>{cat.label}</span>
            {isSelected && !isActive && <div className="h-1.5 w-1.5 rounded-full bg-green-400 ml-1 animate-pulse" />}
          </button>
        );
      })}
    </div>
  </div>
);

const BuildSummary = ({ build, totalCost, totalPower, onRemove, onClear }) => {
  const [isOpen, setIsOpen] = useState(false);
  const filledSlots = Object.keys(build).length;
  const totalSlots = CATEGORIES.length;
  const progress = (filledSlots / totalSlots) * 100;

  return (
    <>
      {/* Mobile Toggle Button */}
      <button 
        onClick={() => setIsOpen(true)}
        className="lg:hidden fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-full shadow-[0_4px_20px_rgba(79,70,229,0.5)] flex items-center space-x-2 animate-bounce-slow border border-white/20"
      >
        <ShoppingCart size={24} />
        <span className="font-bold bg-white/20 px-2 py-0.5 rounded-full text-sm">${totalCost}</span>
      </button>

      {/* Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Panel */}
      <div className={`
        fixed inset-y-0 right-0 z-50 w-full sm:w-[400px] bg-slate-900/95 backdrop-blur-xl border-l border-white/10 shadow-2xl
        transform transition-all duration-500 cubic-bezier(0.4, 0, 0.2, 1)
        ${isOpen ? 'translate-x-0' : 'translate-x-full'} lg:translate-x-0 lg:static lg:h-[calc(100vh-100px)] lg:bg-slate-900/50 lg:rounded-3xl lg:border lg:w-96 lg:block lg:sticky lg:top-24
      `}>
        <div className="h-full flex flex-col p-6">
          {/* Header */}
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

          {/* Progress Bar */}
          <div className="mb-8 relative group">
            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-700 ease-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
                style={{ width: `${progress}%` }}
              />
            </div>
            <div className="absolute top-4 left-0 right-0 text-center opacity-0 group-hover:opacity-100 transition-opacity text-xs text-blue-400 font-medium">
              {Math.round(progress)}% Complete
            </div>
          </div>

          {/* Stats Grid */}
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

          {/* Scrollable Parts List */}
          <div className="flex-1 overflow-y-auto pr-2 -mr-2 space-y-3 custom-scrollbar">
            {CATEGORIES.map(cat => {
              const part = build[cat.key];
              const Icon = cat.icon;
              
              if (!part) {
                return (
                  <div key={cat.key} className="flex items-center p-3 rounded-xl border border-white/5 border-dashed text-slate-600 bg-white/[0.02]">
                    <Icon size={16} className="mr-3" />
                    <span className="text-sm font-medium">Add {cat.label}</span>
                  </div>
                );
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
                      <p className="text-xs text-slate-400 mt-0.5">${part.price}</p>
                    </div>
                    <button 
                      onClick={() => onRemove(cat.key)}
                      className="absolute top-2 right-2 p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-md transition-all opacity-0 group-hover:opacity-100"
                    >
                      <X size={14} />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Footer Action */}
          <div className="pt-6 mt-4 border-t border-white/10">
            <button className="w-full group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-900/20 transition-all active:scale-[0.98] flex items-center justify-center">
              <span className="mr-2">Complete Build</span>
              <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

const Navbar = () => (
  <nav className="fixed w-full z-40 bg-slate-950/80 backdrop-blur-md border-b border-white/5">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-20">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-xl shadow-lg shadow-blue-500/20">
            <Cpu className="h-6 w-6 text-white" strokeWidth={2} />
          </div>
          <span className="text-2xl font-bold text-white tracking-tight">PCBuild<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Assist</span></span>
        </div>
        
        <div className="hidden md:flex items-center space-x-1">
          {['Builder', 'Pre-Built', 'Guides', 'Community'].map((item) => (
            <a key={item} href="#" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
              {item}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 text-slate-400 hover:text-white transition-colors">
            <Search size={20} />
          </button>
          <div className="md:hidden">
            <Menu className="text-slate-300" />
          </div>
        </div>
      </div>
    </div>
  </nav>
);

const App = () => {
  const [build, setBuild] = useState({});
  const [activeCategory, setActiveCategory] = useState('cpu');
  const [compatibilityIssues, setCompatibilityIssues] = useState([]);

  // Logic remains the same...
  const togglePart = (category, part) => {
    setBuild(prev => {
      const newBuild = { ...prev };
      if (newBuild[category] && newBuild[category].id === part.id) {
        delete newBuild[category];
      } else {
        newBuild[category] = part;
      }
      return newBuild;
    });
  };

  const removePart = (category) => {
    setBuild(prev => {
      const newBuild = { ...prev };
      delete newBuild[category];
      return newBuild;
    });
  };

  const clearBuild = () => setBuild({});

  const totalCost = Object.values(build).reduce((sum, part) => sum + part.price, 0);
  const totalPower = Object.values(build).reduce((sum, part) => sum + (part.power || 0), 0) + 50;

  useEffect(() => {
    const issues = [];
    if (build.cpu && build.motherboard) {
      if (build.cpu.brand === 'Intel' && !build.motherboard.specs.includes('LGA1700')) {
        issues.push({ level: 'error', msg: 'Incompatible CPU and Motherboard socket.' });
      }
      if (build.cpu.brand === 'AMD' && !build.motherboard.specs.includes('AM5')) {
        issues.push({ level: 'error', msg: 'Incompatible CPU and Motherboard socket.' });
      }
    }
    if (build.motherboard && build.ram) {
      if (build.motherboard.specs.includes('DDR5') && !build.ram.specs.includes('DDR5')) {
        issues.push({ level: 'error', msg: 'Motherboard requires DDR5 RAM.' });
      }
      if (build.motherboard.specs.includes('DDR4') && !build.ram.specs.includes('DDR4')) {
        issues.push({ level: 'error', msg: 'Motherboard requires DDR4 RAM.' });
      }
    }
    if (build.psu && totalPower > parseInt(build.psu.specs)) {
      issues.push({ level: 'warning', msg: 'Estimated wattage exceeds PSU capacity.' });
    }
    setCompatibilityIssues(issues);
  }, [build, totalPower]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30 overflow-x-hidden">
      {/* Background Ambience */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px]" />
      </div>

      <Navbar />

      <div className="flex flex-col lg:flex-row max-w-7xl mx-auto pt-24 lg:pt-28 min-h-screen relative z-10">
        
        {/* Main Content Area */}
        <main className="flex-1 px-4 sm:px-6 lg:px-8 pb-24 lg:pb-12">
          
          {/* Header & Status */}
          <div className="mb-8 space-y-4">
            <div>
              <h1 className="text-4xl lg:text-5xl font-extrabold text-white tracking-tight mb-2">
                System <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Builder</span>
              </h1>
              <p className="text-slate-400 text-lg">Assemble your ultimate gaming rig with real-time compatibility checking.</p>
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

          <CategorySelector 
            activeCategory={activeCategory} 
            setActiveCategory={setActiveCategory}
            buildState={build} 
          />

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {PARTS_DB[activeCategory].map(part => (
              <PartCard 
                key={part.id} 
                part={part} 
                onAdd={(p) => togglePart(activeCategory, p)}
                isSelected={build[activeCategory]?.id === part.id}
              />
            ))}
          </div>

          {Object.keys(build).length === 0 && (
            <div className="mt-12 text-center py-20 border-2 border-dashed border-slate-800 rounded-3xl bg-slate-900/30">
              <div className="inline-flex bg-slate-800/50 p-5 rounded-full mb-6">
                <Plus size={40} className="text-slate-600" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Your Build is Empty</h3>
              <p className="text-slate-400 max-w-md mx-auto">
                Select a component from the list above to begin your journey to PC Master Race glory.
              </p>
            </div>
          )}
        </main>

        {/* Sidebar Summary */}
        <div className="flex-shrink-0 lg:w-96 lg:pl-8">
           <BuildSummary 
             build={build} 
             totalCost={totalCost} 
             totalPower={totalPower}
             onRemove={removePart}
             onClear={clearBuild}
           />
        </div>
      </div>
    </div>
  );
};

export default App;