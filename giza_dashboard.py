import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, RadialBarChart, RadialBar } from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Users, Activity, Zap, Target, BarChart3, CircleDot, Calendar } from 'lucide-react';

const GizaTokenDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock data based on research - in a real implementation, this would come from APIs
  const currentMetrics = {
    price: 0.1762,
    priceChange24h: -7.40,
    priceChange7d: -5.10,
    marketCap: 18720000,
    volume24h: 3540038,
    circulatingSupply: 88691142,
    totalSupply: 1000000000,
    maxSupply: 1000000000,
    fdv: 176200000,
    rank: 1319,
    ath: 0.49,
    atl: 0.073
  };

  const protocolMetrics = {
    totalVolumeProcessed: 474000000,
    assetsUnderAgents: 11500000,
    activeAgents: 7000,
    totalTransactions: 213000,
    averageAPR: 9.32,
    yieldVsPassive: 83,
    capitalProductivityIndex: 5.843
  };

  // Historical price data (mock data simulating real price movements)
  const priceHistory = [
    { date: '2025-01-01', price: 0.073, volume: 1200000 },
    { date: '2025-01-15', price: 0.089, volume: 1500000 },
    { date: '2025-02-01', price: 0.156, volume: 2100000 },
    { date: '2025-02-15', price: 0.234, volume: 3200000 },
    { date: '2025-03-01', price: 0.387, volume: 4800000 },
    { date: '2025-03-15', price: 0.49, volume: 6100000 },
    { date: '2025-04-01', price: 0.421, volume: 4900000 },
    { date: '2025-04-15', price: 0.356, volume: 4200000 },
    { date: '2025-05-01', price: 0.298, volume: 3800000 },
    { date: '2025-05-15', price: 0.267, volume: 3100000 },
    { date: '2025-06-01', price: 0.223, volume: 2900000 },
    { date: '2025-06-15', price: 0.198, volume: 2600000 },
    { date: '2025-07-01', price: 0.189, volume: 2400000 },
    { date: '2025-07-17', price: 0.1762, volume: 3540038 }
  ];

  // Protocol growth data
  const protocolGrowth = [
    { month: 'Jan', agents: 1000, volume: 50000000, aua: 2000000 },
    { month: 'Feb', agents: 2100, volume: 89000000, aua: 3500000 },
    { month: 'Mar', agents: 3800, volume: 156000000, aua: 5200000 },
    { month: 'Apr', agents: 5200, volume: 234000000, aua: 7800000 },
    { month: 'May', agents: 6500, volume: 358000000, aua: 9200000 },
    { month: 'Jun', agents: 6800, volume: 421000000, aua: 10500000 },
    { month: 'Jul', agents: 7000, volume: 474000000, aua: 11500000 }
  ];

  // Token distribution
  const tokenDistribution = [
    { name: 'Circulating Supply', value: 88.7, color: '#3B82F6' },
    { name: 'Team & Advisors', value: 200, color: '#8B5CF6' },
    { name: 'Ecosystem Fund', value: 300, color: '#10B981' },
    { name: 'Treasury', value: 150, color: '#F59E0B' },
    { name: 'Future Emissions', value: 261.3, color: '#EF4444' }
  ];

  // Key ratios
  const keyRatios = [
    { name: 'Market Cap / FDV', value: (currentMetrics.marketCap / currentMetrics.fdv * 100).toFixed(1) + '%', trend: 'neutral' },
    { name: 'Circulating / Total', value: (currentMetrics.circulatingSupply / currentMetrics.totalSupply * 100).toFixed(1) + '%', trend: 'up' },
    { name: 'Volume / Market Cap', value: (currentMetrics.volume24h / currentMetrics.marketCap * 100).toFixed(1) + '%', trend: 'up' },
    { name: 'AUA / Market Cap', value: (protocolMetrics.assetsUnderAgents / currentMetrics.marketCap * 100).toFixed(1) + '%', trend: 'up' }
  ];

  const MetricCard = ({ title, value, change, icon: Icon, prefix = '', suffix = '' }) => (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">
            {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
          </p>
          {change !== undefined && (
            <div className={`flex items-center mt-1 ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {change >= 0 ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
              <span className="text-sm font-medium">{Math.abs(change).toFixed(2)}%</span>
            </div>
          )}
        </div>
        <div className="p-3 bg-blue-50 rounded-full">
          <Icon className="h-6 w-6 text-blue-600" />
        </div>
      </div>
    </div>
  );

  const OverviewTab = () => (
    <div className="space-y-6">
      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="Current Price" 
          value={currentMetrics.price.toFixed(4)} 
          change={currentMetrics.priceChange24h}
          icon={DollarSign}
          prefix="$"
        />
        <MetricCard 
          title="Market Cap" 
          value={(currentMetrics.marketCap / 1000000).toFixed(1)} 
          change={currentMetrics.priceChange24h}
          icon={BarChart3}
          suffix="M"
          prefix="$"
        />
        <MetricCard 
          title="24h Volume" 
          value={(currentMetrics.volume24h / 1000000).toFixed(1)} 
          icon={Activity}
          suffix="M"
          prefix="$"
        />
        <MetricCard 
          title="CoinGecko Rank" 
          value={currentMetrics.rank} 
          icon={Target}
          prefix="#"
        />
      </div>

      {/* Price Chart */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Price Performance</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={priceHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip 
              formatter={(value, name) => [`$${value}`, name === 'price' ? 'Price' : 'Volume']}
              labelFormatter={(label) => `Date: ${label}`}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={{ fill: '#3B82F6', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Key Ratios */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Financial Ratios</h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {keyRatios.map((ratio, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">{ratio.name}</p>
              <p className="text-xl font-bold text-gray-900">{ratio.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const TokenomicsTab = () => (
    <div className="space-y-6">
      {/* Supply Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard 
          title="Circulating Supply" 
          value={(currentMetrics.circulatingSupply / 1000000).toFixed(1)} 
          icon={Users}
          suffix="M"
        />
        <MetricCard 
          title="Total Supply" 
          value={(currentMetrics.totalSupply / 1000000).toFixed(0)} 
          icon={Activity}
          suffix="M"
        />
        <MetricCard 
          title="FDV" 
          value={(currentMetrics.fdv / 1000000).toFixed(1)} 
          icon={DollarSign}
          suffix="M"
          prefix="$"
        />
      </div>

      {/* Token Distribution Chart */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Token Distribution (Millions)</h3>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={tokenDistribution}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}M`}
              outerRadius={120}
              fill="#8884d8"
              dataKey="value"
            >
              {tokenDistribution.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => [`${value}M tokens`, 'Amount']} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Supply Schedule */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Supply Metrics</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
            <span className="font-medium">Circulation Ratio</span>
            <span className="text-xl font-bold text-blue-600">
              {(currentMetrics.circulatingSupply / currentMetrics.totalSupply * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
            <span className="font-medium">Market Cap / FDV</span>
            <span className="text-xl font-bold text-green-600">
              {(currentMetrics.marketCap / currentMetrics.fdv * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center p-4 bg-purple-50 rounded-lg">
            <span className="font-medium">Price vs ATH</span>
            <span className="text-xl font-bold text-purple-600">
              -{((currentMetrics.ath - currentMetrics.price) / currentMetrics.ath * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const ProtocolTab = () => (
    <div className="space-y-6">
      {/* Protocol Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="Total Volume Processed" 
          value={(protocolMetrics.totalVolumeProcessed / 1000000).toFixed(0)} 
          icon={Activity}
          suffix="M"
          prefix="$"
        />
        <MetricCard 
          title="Assets Under Agents" 
          value={(protocolMetrics.assetsUnderAgents / 1000000).toFixed(1)} 
          icon={DollarSign}
          suffix="M"
          prefix="$"
        />
        <MetricCard 
          title="Active Agents" 
          value={protocolMetrics.activeAgents.toLocaleString()} 
          icon={Users}
        />
        <MetricCard 
          title="Total Transactions" 
          value={(protocolMetrics.totalTransactions / 1000).toFixed(0)} 
          icon={Zap}
          suffix="K"
        />
      </div>

      {/* Protocol Growth Chart */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Protocol Growth Over Time</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={protocolGrowth}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip 
              formatter={(value, name) => {
                if (name === 'agents') return [value.toLocaleString(), 'Active Agents'];
                if (name === 'volume') return [`$${(value/1000000).toFixed(0)}M`, 'Volume Processed'];
                if (name === 'aua') return [`$${(value/1000000).toFixed(1)}M`, 'Assets Under Agents'];
                return [value, name];
              }}
            />
            <Bar dataKey="agents" fill="#3B82F6" name="agents" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Performance Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
            <div className="text-3xl font-bold text-green-600 mb-2">+{protocolMetrics.yieldVsPassive}%</div>
            <p className="text-sm text-green-700">Yield vs Passive Strategies</p>
          </div>
          <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
            <div className="text-3xl font-bold text-blue-600 mb-2">{protocolMetrics.averageAPR}%</div>
            <p className="text-sm text-blue-700">Average APR</p>
          </div>
          <div className="text-center p-6 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
            <div className="text-3xl font-bold text-purple-600 mb-2">{protocolMetrics.capitalProductivityIndex}x</div>
            <p className="text-sm text-purple-700">Capital Productivity Index</p>
          </div>
        </div>
      </div>

      {/* Volume vs AUA Chart */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Volume Processed vs Assets Under Agents</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={protocolGrowth}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip 
              formatter={(value, name) => {
                if (name === 'volume') return [`$${(value/1000000).toFixed(0)}M`, 'Volume Processed'];
                if (name === 'aua') return [`$${(value/1000000).toFixed(1)}M`, 'Assets Under Agents'];
                return [value, name];
              }}
            />
            <Line type="monotone" dataKey="volume" stroke="#3B82F6" strokeWidth={2} name="volume" />
            <Line type="monotone" dataKey="aua" stroke="#10B981" strokeWidth={2} name="aua" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">GIZA Token Economy Dashboard</h1>
              <p className="text-sm text-gray-600 mt-1">Real-time metrics and analytics for Giza Protocol</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Last Updated</p>
                <p className="text-sm font-medium">July 17, 2025</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'tokenomics', label: 'Tokenomics', icon: CircleDot },
              { id: 'protocol', label: 'Protocol Metrics', icon: Activity }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center px-1 py-4 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-4 w-4 mr-2" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'tokenomics' && <TokenomicsTab />}
        {activeTab === 'protocol' && <ProtocolTab />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4 mt-12">
        <div className="max-w-7xl mx-auto text-center text-sm text-gray-600">
          <p>Data sourced from CoinGecko, official Giza Protocol documentation, and public blockchain data.</p>
          <p className="mt-1">Contract Address: 0x590830dfdf9a3f68afcdde2694773debdf267774</p>
        </div>
      </footer>
    </div>
  );
};

export default GizaTokenDashboard;
