import React, { useState, useEffect, useCallback } from 'react';
import {
  Camera,
  Mic,
  LayoutGrid,
  List,
  ChefHat,
  Settings,
  Plus,
  Minus,
  Trash2,
  AlertTriangle,
  Cloud,
  Wifi,
  Battery,
  Search,
  X,
  Check,
  Thermometer,
  Droplets,
  RefreshCw
} from 'lucide-react';

// --- Configuration ---
const API_BASE = 'http://localhost:8000';
// NOTE: If testing on a real Pi remotely, replace localhost with the Pi's IP address.

// --- Helper Functions ---

const getDaysRemaining = (expiryDate) => {
  if (!expiryDate) return 0;
  const today = new Date();
  const expiry = new Date(expiryDate);
  const diffTime = expiry - today;
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

const getStatusColor = (days) => {
  if (days < 0) return 'bg-gray-500/20 text-gray-400 border-gray-600';
  if (days <= 2) return 'bg-red-500/20 text-red-200 border-red-500/50';
  if (days <= 5) return 'bg-yellow-500/20 text-yellow-200 border-yellow-500/50';
  return 'bg-green-500/20 text-green-200 border-green-500/50';
};

// --- Components ---

const StatusBar = () => (
  <div className="flex justify-between items-center px-6 py-2 bg-slate-900/90 text-slate-400 text-sm border-b border-slate-800">
    <div className="flex items-center space-x-4">
      <span className="font-mono">{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
      <span className="flex items-center space-x-1"><Thermometer size={14} /> <span>4°C</span></span>
      <span className="flex items-center space-x-1"><Droplets size={14} /> <span>45%</span></span>
    </div>
    <div className="flex items-center space-x-4">
      <Wifi size={16} />
      <Cloud size={16} />
      <span className="text-xs bg-blue-600/30 text-blue-300 px-2 py-0.5 rounded-full border border-blue-500/30">System Online</span>
    </div>
  </div>
);

const Sidebar = ({ activeTab, setActiveTab, onMicClick }) => {
  const menuItems = [
    { id: 'dashboard', icon: LayoutGrid, label: 'Dashboard' },
    { id: 'inventory', icon: List, label: 'Inventory' },
    { id: 'scan', icon: Camera, label: 'Scan In' },
    { id: 'recipes', icon: ChefHat, label: 'Recipes' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="w-24 bg-slate-900 border-r border-slate-800 flex flex-col items-center py-4 space-y-4 h-full z-20">
      <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-900/50 mb-2 shrink-0">
        <div className="text-white font-bold text-lg">OS</div>
      </div>

      <div className="flex-1 flex flex-col space-y-2 w-full px-2 overflow-y-auto scrollbar-hide">
        {menuItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center justify-center p-2 rounded-xl transition-all duration-300 shrink-0 ${isActive
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'text-slate-500 hover:bg-slate-800 hover:text-slate-300'
                }`}
            >
              <item.icon size={20} />
              <span className="text-[9px] mt-0.5 font-medium">{item.label}</span>
            </button>
          );
        })}
      </div>

      <button
        onClick={() => onMicClick(true)}
        className="p-3 rounded-full bg-slate-800 text-purple-400 hover:bg-purple-900/30 transition-colors relative group active:scale-95 shrink-0"
        title="Voice Assistant"
      >
        <div className="relative">
          <Mic size={20} />
          <div className="absolute -top-1 -right-1 w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
        </div>
        <span className="sr-only">Voice</span>
      </button>
    </div>
  );
};

const DashboardView = ({ inventory, setActiveTab, isLoading, error }) => {
  const expiringSoon = inventory.filter(i => getDaysRemaining(i.expiry_date) <= 3 && getDaysRemaining(i.expiry_date) >= 0);

  if (error) {
    return (
      <div className="h-full flex items-center justify-center flex-col text-red-400">
        <AlertTriangle size={48} className="mb-4" />
        <p className="text-lg font-bold">Connection Error</p>
        <p className="text-sm opacity-70">Ensure Python backend is running at {API_BASE}</p>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 h-full overflow-y-auto">
      <h1 className="text-2xl text-white font-bold">Good Morning</h1>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-1 bg-gradient-to-br from-red-900/40 to-slate-900 p-5 rounded-2xl border border-red-500/20 flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <div className="bg-red-500/20 p-2 rounded-lg text-red-400"><AlertTriangle size={24} /></div>
            <span className="text-3xl font-bold text-white">{isLoading ? '-' : expiringSoon.length}</span>
          </div>
          <div>
            <p className="text-slate-300 font-medium">Expiring Soon</p>
            <p className="text-slate-500 text-sm">Action needed</p>
          </div>
        </div>

        <div className="col-span-1 bg-gradient-to-br from-blue-900/40 to-slate-900 p-5 rounded-2xl border border-blue-500/20 flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <div className="bg-blue-500/20 p-2 rounded-lg text-blue-400"><List size={24} /></div>
            <span className="text-3xl font-bold text-white">{isLoading ? '-' : inventory.length}</span>
          </div>
          <div>
            <p className="text-slate-300 font-medium">Total Items</p>
            <p className="text-slate-500 text-sm">In stock</p>
          </div>
        </div>

        <div className="col-span-1 bg-gradient-to-br from-emerald-900/40 to-slate-900 p-5 rounded-2xl border border-emerald-500/20 flex flex-col justify-between cursor-pointer hover:bg-emerald-900/30 transition-colors" onClick={() => setActiveTab('recipes')}>
          <div className="flex justify-between items-start">
            <div className="bg-emerald-500/20 p-2 rounded-lg text-emerald-400"><ChefHat size={24} /></div>
            <span className="text-3xl font-bold text-white">3</span>
          </div>
          <div>
            <p className="text-slate-300 font-medium">Recipes</p>
            <p className="text-slate-500 text-sm">Available to cook</p>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg text-white font-semibold">Priority Items</h2>
          <button onClick={() => setActiveTab('inventory')} className="text-blue-400 text-sm hover:underline">View All</button>
        </div>
        <div className="space-y-3">
          {isLoading && <p className="text-slate-500 text-center">Loading inventory...</p>}
          {!isLoading && expiringSoon.length === 0 && <p className="text-slate-500 text-center py-4">Everything looks fresh!</p>}
          {expiringSoon.map(item => (
            <div key={item.id} className="flex items-center justify-between bg-slate-800 p-3 rounded-xl border border-slate-700">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{item.image_icon}</span>
                <div>
                  <p className="text-white font-medium capitalize">{item.name}</p>
                  <p className="text-red-400 text-xs">{getDaysRemaining(item.expiry_date)} days left</p>
                </div>
              </div>
              <button className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1.5 rounded-lg text-xs">
                Consume
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const InventoryView = ({ inventory, refreshInventory, onDelete }) => {
  const [filter, setFilter] = useState('all');

  const filteredInventory = inventory.filter(item => {
    if (filter === 'all') return true;
    // Simple mapping for demo, in real app backend categories should match frontend
    if (filter === 'Fruit' && item.category === '水果') return true;
    if (filter === 'Veg' && item.category === '蔬菜') return true;
    if (filter === 'Dairy' && item.category === '乳制品') return true;
    return item.category === filter;
  });

  const categories = ['all', 'Fruit', 'Veg', 'Dairy', 'Seafood', 'Eggs'];

  return (
    <div className="p-6 h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl text-white font-bold">Inventory</h2>
        <button
          onClick={refreshInventory}
          className="bg-slate-700 hover:bg-slate-600 text-white p-2 rounded-xl"
        >
          <RefreshCw size={16} />
        </button>
      </div>

      <div className="flex space-x-3 overflow-x-auto pb-4 scrollbar-hide">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${filter === cat
              ? 'bg-slate-100 text-slate-900 font-medium'
              : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
          >
            {cat === 'all' ? 'All' : cat}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto grid grid-cols-2 gap-4 pb-20">
        {filteredInventory.length === 0 && (
          <div className="col-span-2 text-center text-slate-500 mt-10">No items found.</div>
        )}
        {filteredInventory.map(item => {
          const days = getDaysRemaining(item.expiry_date);
          const statusClass = getStatusColor(days);

          return (
            <div key={item.id} className={`bg-slate-800/80 p-4 rounded-2xl border flex flex-col relative group ${statusClass.split(' ')[2]}`}>
              <button
                onClick={() => onDelete(item.id)}
                className="absolute top-2 right-2 p-1.5 bg-slate-900/50 rounded-full text-slate-400 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <Trash2 size={14} />
              </button>

              <div className="flex justify-between items-start mb-2">
                <span className="text-3xl">{item.image_icon}</span>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border ${statusClass}`}>
                  {days < 0 ? 'Expired' : `${days} days`}
                </span>
              </div>
              <h3 className="text-white font-bold text-lg capitalize">{item.name}</h3>
              <p className="text-slate-400 text-[10px] mb-3">Added: {item.purchase_date}</p>

              <div className="mt-auto flex justify-between items-center bg-slate-900/50 rounded-lg p-1">
                <button className="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-white rounded-md hover:bg-slate-700">
                  <Minus size={14} />
                </button>
                <span className="text-white font-mono font-medium text-sm">{item.quantity} {item.unit}</span>
                <button className="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-white rounded-md hover:bg-slate-700">
                  <Plus size={14} />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const ScanView = ({ onAddItem, setActiveTab }) => {
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Auto-Scan Polling for Continuous Vision
  useEffect(() => {
    let intervalId;

    // Only poll if we don't have a result and aren't manually scanning
    if (!result && !scanning) {
      intervalId = setInterval(async () => {
        try {
          // Silent fetch
          const response = await fetch(`${API_BASE}/api/scan/live`);
          if (response.ok) {
            const data = await response.json();
            if (data.found) {
              setResult(data);
              // Beep or visual feedback could go here
            }
          }
        } catch (err) {
          // Ignore connection errors during background polling
        }
      }, 800); // Check every 800ms
    }

    return () => clearInterval(intervalId);
  }, [result, scanning]);

  const handleScan = async () => {
    setScanning(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/scan/live`);
      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();

      if (data.found) {
        setResult(data);
      } else {
        setError("No recognizable items found. Please try again.");
      }
    } catch (err) {
      console.error(err);
      setError("Failed to connect to camera AI service.");
    } finally {
      setScanning(false);
    }
  };

  const handleConfirm = () => {
    if (result) {
      onAddItem({
        name: result.name,
        category: result.category,
        quantity: 1,
        unit: result.unit,
        expiry_date: result.expiry_date,
        image_icon: result.image_icon
      });
      setActiveTab('inventory');
    }
  };

  return (
    <div className="h-full flex flex-col relative bg-black">
      {/* Viewport */}
      <div className="flex-1 relative overflow-hidden bg-slate-900">

        {/* Live Video Feed */}
        <div className="absolute inset-0 flex items-center justify-center">
          <img
            src={`${API_BASE}/api/video_feed`}
            alt="Live Feed"
            className="w-full h-full object-cover opacity-80"
            onError={(e) => {
              e.target.style.display = 'none'; // Hide if broken
              // You could show a placeholder here
            }}
          />
          {/* Fallback text if image hidden via error */}
          <div className="absolute inset-0 flex items-center justify-center -z-10">
            <p className="text-slate-500">Connecting to Camera...</p>
          </div>
        </div>

        {/* Overlay Grid */}
        {!result && (
          <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
            <div className="w-64 h-64 border-2 border-white/30 rounded-3xl relative">
              <div className="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-blue-500 rounded-tl-xl"></div>
              <div className="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-blue-500 rounded-tr-xl"></div>
              <div className="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-blue-500 rounded-bl-xl"></div>
              <div className="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-blue-500 rounded-br-xl"></div>
              {scanning && (
                <div className="absolute top-0 left-0 right-0 h-1 bg-blue-500/80 shadow-[0_0_15px_rgba(59,130,246,0.8)] animate-scan"></div>
              )}
            </div>
          </div>
        )}

        {/* Error Toast */}
        {error && (
          <div className="absolute top-4 left-0 right-0 flex justify-center z-50">
            <div className="bg-red-500/90 text-white px-6 py-2 rounded-full text-sm font-medium backdrop-blur-sm shadow-lg animate-bounce">
              {error}
            </div>
          </div>
        )}

        {/* Result Modal */}
        {result && (
          <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/80 backdrop-blur-md p-6 animate-fade-in">
            <div className="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-3xl p-6 shadow-2xl">
              <div className="flex justify-center -mt-12 mb-4">
                <div className="w-20 h-20 bg-slate-800 rounded-full border-4 border-slate-900 flex items-center justify-center text-5xl shadow-lg">
                  {result.image_icon}
                </div>
              </div>

              <div className="text-center mb-6">
                <h2 className="text-2xl text-white font-bold capitalize">{result.name}</h2>
                <p className="text-green-400 text-sm mt-1">Confidence: {Math.round(result.confidence * 100)}%</p>
              </div>

              <div className="bg-slate-800/50 rounded-xl p-4 mb-6 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Category</span>
                  <span className="text-white">{result.category}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Expiry</span>
                  <span className="text-white">{result.expiry_date}</span>
                </div>
                <div className="flex justify-between items-center pt-2 border-t border-slate-700/50">
                  <span className="text-slate-400">Quantity</span>
                  <div className="flex items-center space-x-3">
                    <button className="text-slate-400 hover:text-white"><Minus size={16} /></button>
                    <span className="text-white font-bold">1 {result.unit}</span>
                    <button className="text-slate-400 hover:text-white"><Plus size={16} /></button>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setResult(null)} className="py-3 rounded-xl bg-slate-800 text-slate-300 font-medium hover:bg-slate-700">Retry</button>
                <button onClick={handleConfirm} className="py-3 rounded-xl bg-blue-600 text-white font-medium hover:bg-blue-500 shadow-lg shadow-blue-900/50">Add Item</button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      {!result && (
        <div className="h-24 bg-slate-900/90 border-t border-slate-800 flex items-center justify-center px-8 z-30">
          <p className="absolute bottom-28 text-white/70 font-medium bg-black/50 px-4 py-1 rounded-full backdrop-blur-sm">
            {scanning ? 'Analyzing...' : 'Place item in frame'}
          </p>
          <button
            onClick={handleScan}
            disabled={scanning}
            className={`w-16 h-16 rounded-full border-4 flex items-center justify-center transition-all ${scanning
              ? 'border-gray-600 bg-gray-800 cursor-not-allowed'
              : 'border-white bg-white/10 hover:bg-white/20 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]'
              }`}
          >
            <div className={`w-12 h-12 rounded-full ${scanning ? 'bg-gray-500' : 'bg-white'}`}></div>
          </button>
        </div>
      )}
    </div>
  );
};

const RecipeView = ({ inventory }) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateRecipes = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/recipes/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inventory)
      });
      const data = await res.json();
      setRecipes(data);
    } catch (e) {
      console.error(e);
      alert("Failed to generate recipes");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 h-full overflow-y-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl text-white font-bold">Smart Recommendations</h2>
          <p className="text-slate-400 text-sm">Based on your current stock</p>
        </div>
        <button
          onClick={generateRecipes}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center space-x-2 disabled:opacity-50"
        >
          {loading ? <RefreshCw size={16} className="animate-spin" /> : <ChefHat size={16} />}
          <span>{loading ? 'Thinking...' : 'Generate New'}</span>
        </button>
      </div>

      {recipes.length === 0 && !loading && (
        <div className="text-center text-slate-500 mt-20">
          <ChefHat size={48} className="mx-auto mb-4 opacity-50" />
          <p>Click "Generate New" to ask AI for recipes!</p>
        </div>
      )}

      <div className="space-y-4">
        {recipes.map((recipe, idx) => (
          <div key={idx} className="bg-slate-800 rounded-2xl p-4 border border-slate-700 flex space-x-4 animate-fade-in">
            <div className="w-24 h-24 bg-slate-700 rounded-xl flex items-center justify-center text-3xl">
              {recipe.type === 'seafood' ? '🐟' : recipe.type === 'egg' ? '🍳' : '🥗'}
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-start">
                <h3 className="text-white font-bold text-lg">{recipe.name}</h3>
                <span className="bg-slate-900 text-slate-300 text-xs px-2 py-1 rounded-md">{recipe.time}</span>
              </div>

              <div className="mt-2 mb-3 text-xs text-slate-400">
                <p className="line-clamp-2">{recipe.instructions}</p>
              </div>

              <div className="flex space-x-2">
                <button className="flex-1 bg-blue-600/20 text-blue-300 hover:bg-blue-600/30 py-1.5 rounded-lg text-xs font-medium border border-blue-500/20">
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// --- Main App Component ---

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [inventory, setInventory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Voice State
  const [isListening, setIsListening] = useState(false);
  const [voiceReply, setVoiceReply] = useState(null);

  const fetchInventory = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/inventory`);
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setInventory(data);
      setError(null);
    } catch (err) {
      console.error("Connection failed:", err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchInventory();
  }, [fetchInventory]);

  const handleMicClick = (isDevice = false) => {
    if (isDevice) {
      // DEVICE MIC LOGIC
      setIsListening(true);
      setVoiceReply("Listening on Device...");

      fetch(`${API_BASE}/api/voice/device_listen`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inventory)
      })
        .then(res => res.json())
        .then(data => {
          setIsListening(false);
          if (data.status === 'success') {
            setVoiceReply(`You: "${data.query}"\n\nAI: "${data.reply}"`);
          } else {
            setVoiceReply(`Error: ${data.message}`);
          }
        })
        .catch(err => {
          setIsListening(false);
          setVoiceReply("Device Connection Error");
        });
      return;
    }

    // BROWSER MIC LOGIC REMOVED as per user request
    // fallback if needed later
    console.warn("Browser mic disabled");
  };

  const handleAddItem = async (newItem) => {
    try {
      const res = await fetch(`${API_BASE}/api/inventory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newItem.name,
          category: newItem.category || 'Other',
          quantity: newItem.quantity || 1,
          unit: newItem.unit || 'pcs',
          purchase_date: new Date().toISOString().split('T')[0],
          expiry_date: newItem.expiry_date,
          image_icon: newItem.image_icon
        })
      });
      if (res.ok) {
        fetchInventory(); // Refresh list
      }
    } catch (err) {
      console.error("Failed to add item", err);
    }
  };

  const handleDeleteItem = async (id) => {
    try {
      await fetch(`${API_BASE}/api/inventory/${id}`, { method: 'DELETE' });
      setInventory(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      console.error("Failed to delete", err);
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-900 p-4 font-sans select-none">
      {/* Device Frame */}
      <div className="w-[900px] h-[500px] bg-black rounded-[30px] p-3 shadow-2xl relative border border-slate-800 ring-8 ring-slate-900">

        {/* Screen Content */}
        <div className="w-full h-full bg-slate-950 rounded-[20px] overflow-hidden flex flex-col relative">

          <StatusBar />

          <div className="flex-1 flex overflow-hidden">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} onMicClick={handleMicClick} />

            <main className="flex-1 relative bg-gradient-to-br from-slate-900 to-slate-950">
              {activeTab === 'dashboard' && <DashboardView inventory={inventory} setActiveTab={setActiveTab} isLoading={isLoading} error={error} />}
              {activeTab === 'inventory' && <InventoryView inventory={inventory} refreshInventory={fetchInventory} onDelete={handleDeleteItem} />}
              {activeTab === 'scan' && <ScanView onAddItem={handleAddItem} setActiveTab={setActiveTab} />}
              {activeTab === 'recipes' && <RecipeView inventory={inventory} />}
              {activeTab === 'settings' && (
                <div className="flex items-center justify-center h-full text-slate-500 flex-col">
                  <Settings size={48} className="mb-4 opacity-50" />
                  <p>System Settings</p>
                  <p className="text-xs mt-2 opacity-50">API Connected: {error ? 'No' : 'Yes'}</p>
                </div>
              )}
            </main>
          </div>

          {/* Voice Overlay */}
          {isListening && (
            <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
              <div className="flex flex-col items-center">
                <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center animate-pulse shadow-[0_0_30px_rgba(37,99,235,0.6)]">
                  <Mic size={40} className="text-white" />
                </div>
                <p className="text-white mt-4 font-medium text-lg">Listening...</p>
              </div>
            </div>
          )}

          {/* Voice Reply Modal */}
          {voiceReply && (
            <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-8 animate-fade-in" onClick={() => setVoiceReply(null)}>
              <div className="bg-slate-900 border border-slate-700 p-6 rounded-2xl max-w-lg shadow-2xl relative" onClick={e => e.stopPropagation()}>
                <button onClick={() => setVoiceReply(null)} className="absolute top-2 right-2 text-slate-500 hover:text-white"><X size={20} /></button>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-blue-600 rounded-lg"><Mic size={20} className="text-white" /></div>
                  <h3 className="text-white font-bold text-lg">Assistant</h3>
                </div>
                <p className="text-slate-300 leading-relaxed">{voiceReply}</p>
              </div>
            </div>
          )}

        </div>
      </div>

      <style>{`
        @keyframes scan {
          0% { top: 0; opacity: 0; }
          20% { opacity: 1; }
          90% { opacity: 1; }
          100% { top: 100%; opacity: 0; }
        }
        .animate-scan {
          animation: scan 2s linear infinite;
        }
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
      `}</style>
    </div>
  );
};

export default App;
