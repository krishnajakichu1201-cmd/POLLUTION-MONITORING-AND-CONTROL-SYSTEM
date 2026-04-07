import json
import os

def generate():
    data_path = 'dashboard/src/dashboard_data.json'
    html_template_path = 'dashboard.html'
    output_path = 'dashboard_standalone.html'
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Define the HTML template directly here to ensure it's perfect
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pollution Monitoring Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/recharts/umd/Recharts.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #050505;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            margin: 0;
            overflow-x: hidden;
        }}
        .glass {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1.5rem;
        }}
        .card-hover:hover {{
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}
        .tag {{
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .tag-good {{ background: rgba(16, 185, 129, 0.1); color: var(--accent-green); border: 1px solid rgba(16, 185, 129, 0.2); }}
        .tag-moderate {{ background: rgba(245, 158, 11, 0.1); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.2); }}
        .tag-bad {{ background: rgba(239, 68, 68, 0.1); color: var(--accent-red); border: 1px solid rgba(239, 68, 68, 0.2); }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-fade-in {{
            animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }}
    </style>
</head>
<body>
    <div id="root"></div>

    <script>
        // EMBEDDED DATA
        window.pollutionData = {json.dumps(data)};
    </script>

    <script type="text/babel">
        const {{ useState, useMemo, useEffect }} = React;
        const {{ 
            LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area,
            BarChart, Bar, Cell, PieChart, Pie
        }} = Recharts;

        const StatCard = ({{ title, value, iconName, color, trend }}) => {{
            useEffect(() => {{
                if (window.lucide) lucide.createIcons();
            }}, []);

            return (
                <div className="glass p-6 card-hover transition-all duration-300">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">{{title}}</p>
                            <h2 className="text-3xl font-bold">{{value}}</h2>
                            {{trend !== undefined && (
                                <p className={{`text-xs mt-2 font-semibold ${{trend > 0 ? 'text-red-400' : 'text-emerald-400'}}`}}>
                                    {{trend > 0 ? '↑' : '↓'}} {{Math.abs(trend)}}% from last year
                                </p>
                            )}}
                        </div>
                        <div className="p-3 rounded-2xl" style={{ background: `${{color}}15`, color }}>
                            <i data-lucide={{iconName}}></i>
                        </div>
                    </div>
                </div>
            );
        }};

        const App = () => {{
            const [data] = useState(window.pollutionData);
            const [selectedCity, setSelectedCity] = useState('All');

            useEffect(() => {{
                if (window.lucide) lucide.createIcons();
            }}, [selectedCity]);

            const filteredAir = useMemo(() => {{
                if (!data) return [];
                if (selectedCity === 'All') return data.air;
                return data.air.filter(d => d.City === selectedCity);
            }}, [selectedCity]);

            const airTrends = useMemo(() => {{
                if (!data) return [];
                const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                return months.map(m => {{
                    const monthLines = filteredAir.filter(d => d.Month === m);
                    return {{
                        name: m,
                        AQI: monthLines.length ? Math.round(monthLines.reduce((a, b) => a + b.AQI, 0) / monthLines.length) : 0
                    }};
                }});
            }}, [filteredAir]);

            if (!data) return (
                <div className="flex items-center justify-center min-h-screen">
                    <div className="text-xl font-medium animate-pulse text-slate-400">Loading Data...</div>
                </div>
            );

            return (
                <div className="max-w-7xl mx-auto px-6 py-12 animate-fade-in">
                    <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                        <div>
                            <h1 className="text-4xl font-bold tracking-tight text-white mb-2">Kerala Pollution Metrics</h1>
                            <p className="text-slate-400 text-lg uppercase tracking-wide font-medium text-xs opacity-60">Environmental Intelligence Dashboard</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="glass px-5 py-2.5 flex items-center gap-3">
                                <i data-lucide="map-pin" className="text-blue-500 w-5 h-5"></i>
                                <span className="font-bold text-sm">State: Kerala</span>
                            </div>
                            <div className="glass px-5 py-2.5 flex items-center gap-3">
                                <i data-lucide="filter" className="text-amber-500 w-5 h-5"></i>
                                <select 
                                    className="bg-transparent border-none text-white focus:outline-none font-bold text-sm cursor-pointer"
                                    value={{selectedCity}}
                                    onChange={{(e) => setSelectedCity(e.target.value)}}
                                >
                                    <option value="All">All Cities</option>
                                    {{data.cities.map(city => <option key={{city}} value={{city}}>{{city}}</option>)}}
                                </select>
                            </div>
                        </div>
                    </header>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                        <StatCard title="Avg Air Quality (AQI)" value={{Math.round(filteredAir.reduce((a, b) => a + b.AQI, 0) / filteredAir.length)}} iconName="wind" color="#3b82f6" trend={{-4.2}} />
                        <StatCard title="Water Potability" value={{`${{data.summary.water_safe_percentage}}%`}} iconName="droplets" color="#10b981" />
                        <StatCard title="Soil Toxicity" value={{`${{data.summary.soil_contaminated_percentage}}%`}} iconName="mountain" color="#f59e0b" trend={{1.8}} />
                        <StatCard title="Monitoring Points" value={{data.districts.length + data.rivers.length}} iconName="activity" color="#ef4444" />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
                        <div className="glass p-8 h-[450px]">
                            <div className="flex items-center gap-3 mb-8">
                                <i data-lucide="wind" className="text-blue-500"></i>
                                <h3 className="text-xl font-bold">Air Quality Trends (AQI Index)</h3>
                            </div>
                            <ResponsiveContainer width="100%" height="85%">
                                <AreaChart data={{airTrends}}>
                                    <defs>
                                        <linearGradient id="colorAqi" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={{0.3}}/>
                                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={{0}}/>
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid vertical={{false}} stroke="rgba(255,255,255,0.05)" />
                                    <XAxis dataKey="name" axisLine={{false}} tickLine={{false}} tick={{{{fill: '#94a3b8', fontSize: 13}}}} dy={{15}} />
                                    <YAxis axisLine={{false}} tickLine={{false}} tick={{{{fill: '#94a3b8', fontSize: 13}}}} dx={{-10}} />
                                    <Tooltip 
                                        contentStyle={{{{background: '#0a0a0a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', padding: '12px'}}}}
                                        itemStyle={{{{color: '#3b82f6', fontWeight: 'bold'}}}}
                                    />
                                    <Area type="monotone" dataKey="AQI" stroke="#3b82f6" strokeWidth={{4}} fillOpacity={{1}} fill="url(#colorAqi)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="glass p-8 h-[450px]">
                            <div className="flex items-center gap-3 mb-8">
                                <i data-lucide="droplets" className="text-emerald-500"></i>
                                <h3 className="text-xl font-bold">River Bio-Oxygen Demand</h3>
                            </div>
                            <ResponsiveContainer width="100%" height="85%">
                                <BarChart data={{data.water.slice(0, 10)}}>
                                    <CartesianGrid vertical={{false}} stroke="rgba(255,255,255,0.05)" />
                                    <XAxis dataKey="River" axisLine={{false}} tickLine={{false}} tick={{{{fill: '#94a3b8', fontSize: 11}}}} dy={{15}} />
                                    <YAxis axisLine={{false}} tickLine={{false}} tick={{{{fill: '#94a3b8', fontSize: 13}}}} dx={{-10}} />
                                    <Tooltip 
                                        cursor={{{{fill: 'rgba(255,255,255,0.03)'}}}}
                                        contentStyle={{{{background: '#0a0a0a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px'}}}}
                                    />
                                    <Bar dataKey="BOD(mg/L)" fill="#10b981" radius={{[10, 10, 0, 0]}} barSize={{34}}>
                                        {{data.water.slice(0, 10).map((entry, index) => (
                                            <Cell key={{index}} fill={{entry['BOD(mg/L)'] > 15 ? '#ef4444' : '#10b981'}} />
                                        ))}}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    <div className="glass p-8 overflow-hidden">
                        <div className="flex items-center gap-3 mb-8">
                            <i data-lucide="mountain" className="text-amber-500"></i>
                            <h3 className="text-xl font-bold">Soil Contamination Registry</h3>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead>
                                    <tr className="border-b border-white/5 text-slate-500 text-xs font-bold uppercase tracking-widest">
                                        <th className="pb-5 px-4 text-xs">District</th>
                                        <th className="pb-5 px-4">Land Categorization</th>
                                        <th className="pb-5 px-4">pH Metrics</th>
                                        <th className="pb-5 px-4">Lead PPM</th>
                                        <th className="pb-5 px-4 text-right">Class</th>
                                    </tr>
                                </thead>
                                <tbody className="text-sm">
                                    {{data.soil.slice(0, 8).map((item, i) => (
                                        <tr key={{i}} className="border-b border-white/5 hover:bg-white/5 transition-all duration-200">
                                            <td className="py-5 px-4 font-bold text-white">{{item.District}}</td>
                                            <td className="py-5 px-4 text-slate-400 font-medium">{{item.Land_Use}}</td>
                                            <td className="py-5 px-4 font-mono text-emerald-400">{{item.pH}}</td>
                                            <td className="py-5 px-4 font-mono text-slate-300">{{item['Lead(mg/kg)']}}</td>
                                            <td className="py-5 px-4 text-right">
                                                <span className={{`tag ${{item.Soil_Quality_Class.includes('Heavily') ? 'tag-bad' : 'tag-good'}}`}}>
                                                    {{item.Soil_Quality_Class}}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <footer className="mt-16 text-center text-slate-600 text-xs font-bold uppercase tracking-widest pb-12">
                        <p>&copy; 2026 Environmental Analytics Division, Kerala. Verified Systems.</p>
                    </footer>
                </div>
            );
        }};

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Standalone dashboard generated successfully at {output_path}")

if __name__ == "__main__":
    generate()
