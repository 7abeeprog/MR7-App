import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية في ستريمليت ---
st.set_page_config(
    page_title="MR7 Elite Operations Center", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة والنمط ---
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
current_balance = st.session_state.get('cash_balance', 1250000)

# --- 3. واجهة React المتقدمة (الإصدار 11.0 - محرك العمولات ذو الـ 10 مستويات) ---
react_html = r"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <script crossorigin src="https://unpkg.com/react@18.2.0/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.23.5/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        body { 
            font-family: 'Tajawal', sans-serif; 
            margin: 0; 
            overflow-x: hidden; 
            scroll-behavior: smooth;
            transition: background-color 0.5s, color 0.5s;
            background-color: #030303;
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #FFD700; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: white;
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            border-color: #FFD700;
            box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.1);
            outline: none;
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }

        #loading-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            background: #000; color: #FFD700; display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 99999;
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px;">جاري إقلاع محرك العمولات متعدد الأجيال...</h2>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

        // --- Custom Guarded Icon Component ---
        const Icon = ({ name, size = 24, className = "", fill = "none" }) => {
            const iconRef = useRef(null);
            useEffect(() => {
                if (iconRef.current && window.lucide) {
                    iconRef.current.innerHTML = ''; 
                    const i = document.createElement('i');
                    i.setAttribute('data-lucide', name);
                    if (className) i.setAttribute('class', className);
                    i.setAttribute('fill', fill);
                    iconRef.current.appendChild(i);
                    window.lucide.createIcons({ root: iconRef.current });
                }
            }, [name, size, className, fill]);
            return <span ref={iconRef} className={`inline-flex justify-center items-center ${className}`}></span>;
        };

        const App = () => {
            const [activeTab, setActiveTab] = useState('overview');
            const [toasts, setToasts] = useState([]);
            const [balance, setBalance] = useState(Number(LEADER_BALANCE_PLACEHOLDER));

            // --- 1. Global Multi-Level Commission Config (10 Levels) ---
            const [globalCommRates, setGlobalCommRates] = useState([10, 5, 2, 1, 1, 1, 1, 1, 1, 1]);

            // --- 2. Assets Database (Logic CRUD) ---
            const [assets, setAssets] = useState([
                { 
                    id: 1, name: 'برج السيادة الإداري', stock: 5, price: 1500000, 
                    type: 'عقاري', commRates: [10, 5, 2, 1, 1, 1, 1, 1, 1, 1], 
                    discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400', 
                    desc: 'مقر قيادي عالمي يجمع نخب الاستثمار.' 
                },
                { 
                    id: 2, name: 'دبلوم هندسة الأرباح', stock: Infinity, price: 499, 
                    type: 'رقمي', commRates: [15, 7, 3, 1, 1, 1, 1, 1, 1, 1], 
                    discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400', 
                    desc: 'منهج صناعة الثروة للأجيال القادمة.' 
                }
            ]);

            // --- 3. Order Processing Logic ---
            const [orders, setOrders] = useState([
                { id: 'ORD-88', buyer: 'فهد الرشيد', item: 'برج السيادة', amount: 1500000, status: 'قيد المراجعة', date: 'منذ ساعتين' }
            ]);

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- Multi-Level Logic Handlers ---
            const handleAddAsset = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                
                // Construct the 10-level commission array from inputs
                const customComm = globalCommRates.map((_, i) => parseFloat(f.get(`comm_l${i+1}`) || 0));

                const n = {
                    id: Date.now(),
                    name: f.get('name'), price: parseFloat(f.get('price')),
                    commRates: customComm,
                    stock: f.get('type') === 'رقمي' ? Infinity : parseInt(f.get('stock')),
                    type: f.get('type'), img: f.get('img'), desc: f.get('desc'), status: 'نشط', discount: 0
                };
                setAssets([n, ...assets]);
                showToast('تم إدراج الأصل وتفعيل خارطة العمولات الـ 10');
                e.target.reset();
            };

            const updateGlobalRate = (idx, val) => {
                const newRates = [...globalCommRates];
                newRates[idx] = parseFloat(val);
                setGlobalCommRates(newRates);
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar (Command Center) --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10 shadow-2xl">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-xl"><Icon name="Network" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">محرك الأجيال</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Multilevel Engine v11.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار'},
                                {id: 'inventory', icon: 'Box', label: 'الأصول والجرد'},
                                {id: 'operations', icon: 'Zap', label: 'مركز العمليات'},
                                {id: 'marketing', icon: 'Share2', label: 'هندسة العمولات'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Workspace --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview (KPIs) */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-5">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">عمولات الأجيال المعلقة</small>
                                        <h4 className="text-3xl font-black text-yellow-500">$24,800</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500">
                                        <small className="text-gray-500 font-bold uppercase">صافي التدفق المالي</small>
                                        <h4 className="text-3xl font-black text-green-500">$3.1M</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">قوة الشبكة (ج10)</small>
                                        <h4 className="text-3xl font-black">12,540</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-purple-500">
                                        <small className="text-gray-500 font-bold uppercase">الأصول الموثقة</small>
                                        <h4 className="text-3xl font-black">{assets.length}</h4>
                                    </div>
                                </div>

                                <div className="glass-panel p-8 rounded-[3rem] mt-10">
                                    <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="TrendingUp" className="text-green-500"/> تحليل تضاعف الأجيال</h3>
                                    <div className="space-y-4">
                                        <p className="text-gray-400">نظام الذكاء الاصطناعي يراقب نمو الجيل الخامس في إقليم "مصر". معدل التحويل مرتفع بنسبة 12% هذا الأسبوع.</p>
                                        <div className="flex gap-4">
                                            <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden"><div className="bg-yellow-500 h-full w-[70%]"></div></div>
                                            <span className="text-xs font-black">الجيل 1-3: 70%</span>
                                        </div>
                                        <div className="flex gap-4">
                                            <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden"><div className="bg-blue-500 h-full w-[30%]"></div></div>
                                            <span className="text-xs font-black">الجيل 4-10: 30%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (CRUD with 10 Levels) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col xl:flex-row gap-8">
                                    {/* Asset Creator Form */}
                                    <div className="xl:w-2/5 glass-panel p-8 rounded-[2.5rem] h-fit">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="PlusCircle" className="text-yellow-500"/> هندسة أصل جديد (10 مستويات)</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="اسم الأصل الاستراتيجي..." required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="price" type="number" placeholder="القيمة ($)" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black text-sm">
                                                    <option>عقاري</option><option>منتج</option><option>رقمي</option>
                                                </select>
                                            </div>
                                            
                                            <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                                                <label className="text-[10px] font-black text-gray-500 uppercase block mb-3">تخصيص عمولات الأجيال (%)</label>
                                                <div className="grid grid-cols-5 gap-2">
                                                    {globalCommRates.map((rate, i) => (
                                                        <div key={i} className="flex flex-col">
                                                            <small className="text-[8px] text-center text-gray-600 font-black mb-1">ج{i+1}</small>
                                                            <input name={`comm_l${i+1}`} type="number" defaultValue={rate} step="0.1" className="premium-input p-1 rounded-md text-center text-xs font-bold" />
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>

                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="stock" type="number" placeholder="المخزون" className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <input name="img" placeholder="رابط الصورة..." className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            </div>
                                            <textarea name="desc" placeholder="وصف الأصل..." className="w-full premium-input p-4 rounded-xl font-bold h-20 text-sm"></textarea>
                                            <button type="submit" className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all shadow-xl">نشر الأصل في المنظومة 🚀</button>
                                        </form>
                                    </div>

                                    {/* Inventory Explorer */}
                                    <div className="xl:w-3/5 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد الأصول وعمولات الأجيال</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-[10px] border-b border-white/5 uppercase">
                                                    <th className="pb-4 text-right">الأصل</th>
                                                    <th className="pb-4 text-center">القيمة</th>
                                                    <th className="pb-4 text-center">خارطة العمولات (ج1-ج10)</th>
                                                    <th className="pb-4 text-center">إجراء</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all group">
                                                        <td className="py-4 flex items-center gap-3">
                                                            <img src={a.img} className="w-10 h-10 rounded-lg object-cover" />
                                                            <div><div className="font-bold text-sm">{a.name}</div><small className="text-[10px] text-gray-500">{a.type}</small></div>
                                                        </td>
                                                        <td className="py-4 text-center text-green-500 font-black text-sm">${a.price.toLocaleString()}</td>
                                                        <td className="py-4 text-center">
                                                            <div className="flex justify-center gap-0.5">
                                                                {a.commRates.map((r, idx) => (
                                                                    <div key={idx} title={`الجيل ${idx+1}: ${r}%`} className="w-4 h-4 bg-yellow-500/20 rounded-sm flex items-center justify-center">
                                                                        <span className="text-[6px] font-black text-yellow-500">{r}</span>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={()=>setAssets(assets.filter(as=>as.id!==a.id))} className="text-red-500 hover:scale-125 transition-transform"><Icon name="Trash2" size={16}/></button>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Operations */}
                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Activity" size={32} /> مركز السيطرة على العمليات</h2>
                                <div className="grid grid-cols-1 gap-4">
                                    {orders.map(o => (
                                        <div key={o.id} className="glass-panel p-6 rounded-[2rem] flex justify-between items-center">
                                            <div className="flex items-center gap-5">
                                                <div className="p-4 bg-yellow-500/10 text-yellow-500 rounded-2xl"><Icon name="FileText" size={24}/></div>
                                                <div>
                                                    <h4 className="font-black text-xl">{o.buyer} <small className="text-blue-500 text-xs font-bold mr-2">{o.status}</small></h4>
                                                    <p className="text-sm text-gray-500">{o.item} • {o.date}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-6">
                                                <span className="text-2xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                                <button onClick={()=>processOrder(o.id, 'مكتمل')} className="bg-yellow-500 text-black px-6 py-2.5 rounded-xl font-black text-xs hover:scale-105 transition-transform">اعتماد وتوزيع العمولات</button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing (Global Commission Engineering) */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-5xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Share2" size={32} /> هندسة العمولات العالمية</h2>
                                <p className="text-gray-500">حدد النسب الافتراضية التي ستُطبق على كافة الأصول الجديدة في متجرك.</p>
                                
                                <div className="glass-panel p-10 rounded-[3rem]">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                                        {globalCommRates.map((rate, i) => (
                                            <div key={i} className="space-y-4">
                                                <div className="flex justify-between items-center">
                                                    <label className="text-sm font-black text-gray-400 uppercase tracking-widest">عمولة الجيل {i+1}</label>
                                                    <span className="text-2xl font-black text-yellow-500">{rate}%</span>
                                                </div>
                                                <input 
                                                    type="range" min="0" max={i === 0 ? "50" : "20"} step="0.5" 
                                                    value={rate} 
                                                    onChange={(e)=>updateGlobalRate(i, e.target.value)}
                                                    className="w-full accent-yellow-500" 
                                                />
                                            </div>
                                        ))}
                                    </div>
                                    <button onClick={()=>showToast('تم حفظ خارطة العمولات العالمية للأجيال العشرة')} className="w-full mt-12 py-5 bg-white/5 border border-white/10 rounded-2xl font-black text-xl hover:bg-white/10 transition-all shadow-2xl">تثبيت القوانين المالية للشبكة 💾</button>
                                </div>
                            </div>
                        )}

                    </div>

                    {/* --- Toasts Center --- */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                                <span className="font-bold text-sm text-white">{t.msg}</span>
                            </div>
                        ))}
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ErrorBoundary><App /></ErrorBoundary>);

        function ErrorBoundary({ children }) {
            const [hasError, setHasError] = useState(false);
            if (hasError) return <div className="p-10 text-red-500 font-black text-center h-screen flex items-center justify-center">⚠️ رصد خطأ في محرك الأجيال.. جاري إعادة التهيئة..</div>;
            return children;
        }
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل آمن ---
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=1150, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
