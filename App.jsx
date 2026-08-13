import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell 
} from 'recharts';
import { 
  Package, DollarSign, AlertTriangle, ShoppingCart, User, 
  LayoutDashboard, BarChart3, Settings, Sparkles, PlusCircle, CheckCircle2,
  Search, Filter, Download, RefreshCw, ShieldAlert, ArrowUpRight, ArrowDownRight,
  Bell, Database, Lock, Globe, HardDrive, Cpu, Zap, Sliders, Layers, FileText, Check
} from 'lucide-react';

const inventoryData = [
  { name: "Dec '23", value: 2100000, units: 18000 },
  { name: "Jan '24", value: 2300000, units: 19500 },
  { name: "Feb '24", value: 2600000, units: 21000 },
  { name: "Mar '24", value: 2800000, units: 23000 },
  { name: "Apr '24", value: 3000000, units: 24500 },
  { name: "May '24", value: 3240600, units: 25430 },
];

const categoryData = [
  { name: 'Grains', value: 40, color: '#3b82f6' },
  { name: 'Sweets', value: 25, color: '#ec4899' },
  { name: 'Oils', value: 20, color: '#eab308' },
  { name: 'Beverages', value: 15, color: '#06b6d4' },
];

const comprehensiveInventory = [
  { id: 1, name: "Assorted Sweets", category: "Sweets", stock: 5, unitValue: 350, supplier: "Mithaiwala Corp", status: "Critical Low", turnover: "High" },
  { id: 2, name: "Wheat Flour (10kg)", category: "Grains", stock: 12, unitValue: 450, supplier: "AgriPro Ltd", status: "Optimal", turnover: "Medium" },
  { id: 3, name: "Cooking Oil (1L)", category: "Oils", stock: 8, unitValue: 140, supplier: "PureFoods", status: "Low Stock", turnover: "High" },
  { id: 4, name: "Basmati Rice (5kg)", category: "Grains", stock: 120, unitValue: 650, supplier: "AgriPro Ltd", status: "Optimal", turnover: "High" },
  { id: 5, name: "Green Tea Pack", category: "Beverages", stock: 45, unitValue: 220, supplier: "Herbals Inc", status: "Optimal", turnover: "Low" },
  { id: 6, name: "Jaggery Blocks", category: "Sweets", stock: 19, unitValue: 120, supplier: "Organic Farms", status: "Low Stock", turnover: "Medium" },
];

const aiRecommendations = [
  { id: 1, product: "Assorted Sweets", currentStock: 5, forecast: 20, reason: "Local Holiday Surge Expected", action: "Reorder High Priority", urgency: "high" },
  { id: 2, product: "Wheat Flour (10kg)", currentStock: 12, forecast: 2, reason: "School Lunch Program Ended", action: "Do Not Reorder", urgency: "low" },
  { id: 3, product: "Cooking Oil (1L)", currentStock: 8, forecast: 15, reason: "Upcoming Wedding Season Demand", action: "Reorder Medium Priority", urgency: "medium" },
  { id: 4, product: "Green Tea Pack", currentStock: 45, forecast: 50, reason: "Stable Consumer Run-rate", action: "Maintain Stock", urgency: "low" }
];

export default function PrediCartDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // Interactive Feature States (20+ features embedded)
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState('All');
  const [formData, setFormData] = useState({ productName: '', stockQuantity: '', unitValue: '', category: 'Grains' });
  const [isSaved, setIsSaved] = useState(false);
  
  // Settings States
  const [aiAutopilot, setAiAutopilot] = useState(true);
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [stockThreshold, setStockThreshold] = useState(10);
  const [currencySymbol, setCurrencySymbol] = useState('₹');
  const [settingsSaved, setSettingsSaved] = useState(false);

  const handleSaveData = (e) => {
    e.preventDefault();
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const handleSaveSettings = (e) => {
    e.preventDefault();
    setSettingsSaved(true);
    setTimeout(() => setSettingsSaved(false), 3000);
  };

  const filteredItems = comprehensiveInventory.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) || item.supplier.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategoryFilter === 'All' || item.category === selectedCategoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-[#0B0F19] font-sans text-slate-100 p-4 md:p-8 selection:bg-fuchsia-500 selection:text-white pb-24">
      
      {/* 1. Global Navigation Bar */}
      <nav className="max-w-7xl mx-auto bg-white/5 border border-white/10 backdrop-blur-xl rounded-full px-6 py-4 flex justify-between items-center shadow-2xl sticky top-4 z-50">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="bg-gradient-to-br from-orange-400 to-pink-500 p-2 rounded-xl shadow-lg shadow-pink-500/20">
            <ShoppingCart className="text-white h-6 w-6" />
          </div>
          <h1 className="text-xl font-bold tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            PrediCart AI
          </h1>
        </div>
        
        <div className="flex space-x-2 bg-black/20 p-1 rounded-full border border-white/5">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center px-4 py-2 rounded-full text-sm font-medium transition-all ${activeTab === 'dashboard' ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
          >
            <LayoutDashboard className="h-4 w-4 mr-2" /> Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center px-4 py-2 rounded-full text-sm font-medium transition-all ${activeTab === 'analytics' ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
          >
            <BarChart3 className="h-4 w-4 mr-2" /> Analytics
          </button>
          <button 
            onClick={() => setActiveTab('settings')}
            className={`flex items-center px-4 py-2 rounded-full text-sm font-medium transition-all ${activeTab === 'settings' ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
          >
            <Settings className="h-4 w-4 mr-2" /> Settings
          </button>
        </div>

        <div className="flex items-center space-x-3">
          <span className="hidden lg:inline text-xs font-semibold px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-full">
            Autonomous Mode Active
          </span>
          <div className="p-2 rounded-full bg-white/10 border border-white/10 text-slate-300">
            <User className="h-5 w-5" />
          </div>
        </div>
      </nav>

      {/* ================= TAB 1: DASHBOARD ================= */}
      {activeTab === 'dashboard' && (
        <main className="max-w-7xl mx-auto mt-10 flex flex-col gap-8 animate-fadeIn">
          
          <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-fuchsia-500 to-purple-600">
                  Shopkeeper Intelligence Hub
                </span>
              </h2>
              <p className="text-slate-400 font-medium mt-1">Real-time inventory metrics, demand tracking & predictive restocking.</p>
            </div>
            <div className="flex items-center space-x-3">
              <button onClick={() => alert("Cloud Sync Complete: All local stock records updated.")} className="flex items-center px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-sm font-semibold transition-all">
                <RefreshCw className="h-4 w-4 mr-2 text-cyan-400 animate-spin-slow" /> Sync Cloud
              </button>
              <button onClick={() => alert("Export Report Generated: inventory_report_2026.csv downloaded.")} className="flex items-center px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-cyan-500/20 transition-all">
                <Download className="h-4 w-4 mr-2" /> Export Data
              </button>
            </div>
          </header>

          {/* Core Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="relative overflow-hidden bg-gradient-to-br from-emerald-400 to-teal-600 rounded-3xl p-6 shadow-lg shadow-teal-900/40 border border-white/20">
              <p className="text-emerald-50 text-xs font-bold uppercase tracking-wider mb-1">Total Stock Units</p>
              <p className="text-4xl font-black text-white">25,430</p>
              <div className="mt-3 flex items-center text-xs text-emerald-100 font-medium"><ArrowUpRight className="h-4 w-4 mr-1"/> +12.4% vs last month</div>
              <Package className="absolute bottom-4 right-4 h-14 w-14 text-white/20" />
            </div>

            <div className="relative overflow-hidden bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl p-6 shadow-lg shadow-indigo-900/40 border border-white/20">
              <p className="text-blue-100 text-xs font-bold uppercase tracking-wider mb-1">Total Asset Value</p>
              <p className="text-4xl font-black text-white">{currencySymbol}32.4L</p>
              <div className="mt-3 flex items-center text-xs text-blue-100 font-medium"><ArrowUpRight className="h-4 w-4 mr-1"/> +8.1% asset growth</div>
              <DollarSign className="absolute bottom-4 right-4 h-14 w-14 text-white/20" />
            </div>

            <div className="relative overflow-hidden bg-gradient-to-br from-orange-500 to-red-600 rounded-3xl p-6 shadow-lg shadow-red-900/40 border border-white/20">
              <p className="text-orange-100 text-xs font-bold uppercase tracking-wider mb-1">Critical Low Items</p>
              <p className="text-4xl font-black text-white">32</p>
              <div className="mt-3 flex items-center text-xs text-orange-100 font-medium"><ShieldAlert className="h-4 w-4 mr-1"/> Action required</div>
              <AlertTriangle className="absolute bottom-4 right-4 h-14 w-14 text-white/20" />
            </div>

            <div className="relative overflow-hidden bg-gradient-to-br from-fuchsia-500 to-purple-600 rounded-3xl p-6 shadow-lg shadow-purple-900/40 border border-white/20">
              <p className="text-fuchsia-100 text-xs font-bold uppercase tracking-wider mb-1">AI Accuracy Score</p>
              <p className="text-4xl font-black text-white">98.4%</p>
              <div className="mt-3 flex items-center text-xs text-fuchsia-100 font-medium"><Zap className="h-4 w-4 mr-1"/> Neural engine active</div>
              <Sparkles className="absolute bottom-4 right-4 h-14 w-14 text-white/20" />
            </div>
          </div>

          {/* Charts & Forecast Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white">Inventory Valuation Trend</h3>
                <span className="text-xs text-slate-400 bg-white/5 px-3 py-1 rounded-full border border-white/10">6-Month Moving Average</span>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={inventoryData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#a855f7" stopOpacity={1} />
                        <stop offset="100%" stopColor="#3b82f6" stopOpacity={1} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1e293b" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} dy={10} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} tickFormatter={(val) => `${currencySymbol}${val / 100000}L`} />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '12px', color: '#f8fafc' }} formatter={(v) => [`${currencySymbol}${v.toLocaleString()}`, 'Value']} />
                    <Bar dataKey="value" fill="url(#barGrad)" radius={[6, 6, 0, 0]} barSize={35} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl flex flex-col">
              <h3 className="text-lg font-bold text-white mb-6 flex items-center">
                <Sparkles className="h-5 w-5 mr-2 text-fuchsia-400" /> AI Autonomous Forecast
              </h3>
              <div className="flex-1 space-y-4 overflow-y-auto max-h-72 pr-1">
                {aiRecommendations.map((item) => (
                  <div key={item.id} className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:border-fuchsia-500/30 transition-all">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold text-slate-200 text-sm">{item.product}</h4>
                      <span className="text-xs bg-black/40 px-2 py-0.5 rounded-full border border-white/10">Stock: {item.currentStock}</span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">{item.reason}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] text-slate-500 uppercase">Target: {item.forecast} units</span>
                      <button onClick={() => alert(`Executed automated workflow: ${item.action} for ${item.product}`)} className={`text-xs font-bold px-3 py-1 rounded-full ${item.urgency === 'high' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-slate-700/50 text-slate-300'}`}>
                        {item.action}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Interactive Data Entry & Live Management Table */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Form for Data Entry */}
            <div className="bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center">
                <PlusCircle className="h-5 w-5 mr-2 text-cyan-400" /> Add Inventory Item
              </h3>
              <form onSubmit={handleSaveData} className="space-y-4">
                <div>
                  <label className="text-xs font-semibold text-slate-400 uppercase">Product Name</label>
                  <input type="text" required value={formData.productName} onChange={(e) => setFormData({...formData, productName: e.target.value})} placeholder="e.g. Organic Jaggery" className="w-full mt-1 bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-400 uppercase">Category</label>
                  <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})} className="w-full mt-1 bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500">
                    <option value="Grains" className="bg-slate-900">Grains</option>
                    <option value="Sweets" className="bg-slate-900">Sweets</option>
                    <option value="Oils" className="bg-slate-900">Oils</option>
                    <option value="Beverages" className="bg-slate-900">Beverages</option>
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 uppercase">Stock Qty</label>
                    <input type="number" required value={formData.stockQuantity} onChange={(e) => setFormData({...formData, stockQuantity: e.target.value})} placeholder="50" className="w-full mt-1 bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500" />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 uppercase">Unit Price ({currencySymbol})</label>
                    <input type="number" required value={formData.unitValue} onChange={(e) => setFormData({...formData, unitValue: e.target.value})} placeholder="150" className="w-full mt-1 bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500" />
                  </div>
                </div>
                <button type="submit" className={`w-full mt-4 py-3 rounded-xl font-bold text-sm transition-all shadow-lg flex items-center justify-center ${isSaved ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50' : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white'}`}>
                  {isSaved ? <><CheckCircle2 className="h-4 w-4 mr-2" /> Entry Recorded Successfully!</> : 'Insert Product Data'}
                </button>
              </form>
            </div>

            {/* Live Filterable Data Table */}
            <div className="lg:col-span-2 bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl flex flex-col">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <h3 className="text-xl font-bold text-white flex items-center">
                  <Database className="h-5 w-5 mr-2 text-fuchsia-400" /> Live Inventory Database
                </h3>
                <div className="flex items-center space-x-2">
                  <div className="relative">
                    <Search className="h-4 w-4 absolute left-3 top-3 text-slate-400" />
                    <input type="text" placeholder="Search items..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pl-9 pr-4 py-2 bg-black/20 border border-white/10 rounded-xl text-xs text-white focus:outline-none focus:border-fuchsia-500 w-48" />
                  </div>
                  <select value={selectedCategoryFilter} onChange={(e) => setSelectedCategoryFilter(e.target.value)} className="bg-black/20 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-fuchsia-500">
                    <option value="All" className="bg-slate-900">All Categories</option>
                    <option value="Grains" className="bg-slate-900">Grains</option>
                    <option value="Sweets" className="bg-slate-900">Sweets</option>
                    <option value="Oils" className="bg-slate-900">Oils</option>
                    <option value="Beverages" className="bg-slate-900">Beverages</option>
                  </select>
                </div>
              </div>

              <div className="overflow-x-auto flex-1">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-white/10 text-xs font-semibold text-slate-400 uppercase">
                      <th className="pb-3">Product Name</th>
                      <th className="pb-3">Category</th>
                      <th className="pb-3">Stock</th>
                      <th className="pb-3">Value</th>
                      <th className="pb-3">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {filteredItems.map((item) => (
                      <tr key={item.id} className="hover:bg-white/5 transition-colors">
                        <td className="py-3.5 font-medium text-slate-200">{item.name}</td>
                        <td className="py-3.5 text-slate-400 text-xs"><span className="px-2 py-1 bg-white/5 rounded-lg border border-white/5">{item.category}</span></td>
                        <td className="py-3.5 text-slate-300 font-bold">{item.stock} units</td>
                        <td className="py-3.5 text-cyan-400 font-semibold">{currencySymbol}{item.unitValue}</td>
                        <td className="py-3.5">
                          <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full ${item.status === 'Critical Low' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : item.status === 'Low Stock' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'}`}>
                            {item.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </main>
      )}

      {/* ================= TAB 2: ANALYTICS ================= */}
      {activeTab === 'analytics' && (
        <main className="max-w-7xl mx-auto mt-10 flex flex-col gap-8 animate-fadeIn">
          <header>
            <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500">
              Advanced Analytics & Metrics
            </h2>
            <p className="text-slate-400 font-medium mt-1">Deep-dive breakdown of category distribution and consumption velocity.</p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-6">Inventory Share by Category</h3>
              <div className="h-85 flex items-center justify-center">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie data={categoryData} cx="50%" cy="50%" innerRadius={80} outerRadius={120} paddingAngle={5} dataKey="value">
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '12px' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-4 mt-4">
                {categoryData.map((cat, idx) => (
                  <div key={idx} className="flex items-center space-x-2 bg-white/5 p-3 rounded-xl border border-white/5">
                    <span className="w-3 h-3 rounded-full" style={{ backgroundColor: cat.color }}></span>
                    <span className="text-sm font-medium text-slate-300">{cat.name}: {cat.value}%</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl flex flex-col justify-between">
              <div>
                <h3 className="text-xl font-bold text-white mb-4">Stock Turnover Velocity</h3>
                <p className="text-slate-400 text-sm mb-6">Calculated based on local seasonal footfall index and historical sales velocity.</p>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between text-sm mb-2"><span className="text-slate-300 font-medium">Grains Turnover Rate</span><span className="text-cyan-400 font-bold">88% (Fast)</span></div>
                    <div className="w-full bg-black/40 h-3 rounded-full overflow-hidden border border-white/5"><div className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full w-[88%] rounded-full"></div></div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2"><span className="text-slate-300 font-medium">Sweets & Confectionery Surge</span><span className="text-fuchsia-400 font-bold">95% (Peak)</span></div>
                    <div className="w-full bg-black/40 h-3 rounded-full overflow-hidden border border-white/5"><div className="bg-gradient-to-r from-fuchsia-500 to-pink-500 h-full w-[95%] rounded-full"></div></div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2"><span className="text-slate-300 font-medium">Oils & Staples Stable Index</span><span className="text-emerald-400 font-bold">72% (Steady)</span></div>
                    <div className="w-full bg-black/40 h-3 rounded-full overflow-hidden border border-white/5"><div className="bg-gradient-to-r from-emerald-500 to-teal-500 h-full w-[72%] rounded-full"></div></div>
                  </div>
                </div>
              </div>
              <div className="mt-8 p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-2xl flex items-center space-x-3">
                <Sparkles className="h-6 w-6 text-cyan-400 flex-shrink-0" />
                <p className="text-xs text-cyan-200">AI recommendation: Increase sweet stock buffer by 20% starting next Monday to capture high pedestrian footfall.</p>
              </div>
            </div>
          </div>
        </main>
      )}

      {/* ================= TAB 3: SETTINGS ================= */}
      {activeTab === 'settings' && (
        <main className="max-w-4xl mx-auto mt-10 flex flex-col gap-8 animate-fadeIn">
          <header>
            <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-400 to-purple-500">
              System Configuration & Preferences
            </h2>
            <p className="text-slate-400 font-medium mt-1">Manage AI automation rules, alert thresholds, and currency preferences.</p>
          </header>

          <div className="bg-[#131B2C]/80 backdrop-blur-xl p-8 rounded-3xl border border-white/10 shadow-2xl">
            <form onSubmit={handleSaveSettings} className="space-y-6">
              
              <div className="flex items-center justify-between py-4 border-b border-white/10">
                <div>
                  <h4 className="font-semibold text-white">AI Autonomous Restocking Autopilot</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Let AI automatically issue reorder requests when items hit critical thresholds.</p>
                </div>
                <button type="button" onClick={() => setAiAutopilot(!aiAutopilot)} className={`w-14 h-8 flex items-center rounded-full p-1 transition-colors ${aiAutopilot ? 'bg-cyan-500' : 'bg-slate-700'}`}>
                  <div className={`bg-white w-6 h-6 rounded-full shadow-md transform transition-transform ${aiAutopilot ? 'translate-x-6' : 'translate-x-0'}`}></div>
                </button>
              </div>

              <div className="flex items-center justify-between py-4 border-b border-white/10">
                <div>
                  <h4 className="font-semibold text-white">SMS & Email Inventory Alerts</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Receive instant notifications when stock levels fall below acceptable limits.</p>
                </div>
                <button type="button" onClick={() => setEmailAlerts(!emailAlerts)} className={`w-14 h-8 flex items-center rounded-full p-1 transition-colors ${emailAlerts ? 'bg-cyan-500' : 'bg-slate-700'}`}>
                  <div className={`bg-white w-6 h-6 rounded-full shadow-md transform transition-transform ${emailAlerts ? 'translate-x-6' : 'translate-x-0'}`}></div>
                </button>
              </div>

              <div className="py-4 border-b border-white/10 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                <div>
                  <h4 className="font-semibold text-white">Low Stock Warning Threshold</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Trigger warning labels when product units fall below this number.</p>
                </div>
                <input type="number" value={stockThreshold} onChange={(e) => setStockThreshold(e.target.value)} className="bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-fuchsia-500" />
              </div>

              <div className="py-4 border-b border-white/10 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                <div>
                  <h4 className="font-semibold text-white">Preferred Currency Display</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Select currency symbol used across charts and data cards.</p>
                </div>
                <select value={currencySymbol} onChange={(e) => setCurrencySymbol(e.target.value)} className="bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-fuchsia-500">
                  <option value="₹" className="bg-slate-900">₹ (INR - Indian Rupee)</option>
                  <option value="$" className="bg-slate-900">$ (USD - US Dollar)</option>
                  <option value="€" className="bg-slate-900">€ (EUR - Euro)</option>
                </select>
              </div>

              <div className="pt-4 flex items-center justify-between">
                <span className="text-xs text-slate-500">System Version: PrediCart v4.2.0-stable</span>
                <button type="submit" className={`py-3 px-8 rounded-xl font-bold text-sm transition-all shadow-lg flex items-center ${settingsSaved ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50' : 'bg-gradient-to-r from-fuchsia-500 to-purple-600 hover:from-fuchsia-400 hover:to-purple-500 text-white'}`}>
                  {settingsSaved ? <><Check className="h-4 w-4 mr-2" /> Settings Saved Successfully!</> : 'Save Configuration'}
                </button>
              </div>

            </form>
          </div>
        </main>
      )}

    </div>
  );
}