import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية في ستريمليت ---
st.set_page_config(
    page_title="MR7 Diamond Merchant Hub", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة والنمط ---
fb_config_str = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
current_balance = st.session_state.get('cash_balance', 1250000)

# --- 3. واجهة React المتقدمة (نظام العمليات الشامل 7.0 - الماركتينج والولاء) ---
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
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            transition: all 0.5s;
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: white;
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            border-color: #FFD700;
            outline: none;
            background: rgba(255, 255, 255, 0.05);
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        .offer-badge {
            background: linear-gradient(90deg, #FF4B4B, #FF9068);
            padding: 2px 10px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 900;
            color: white;
            animation: pulse-red 2s infinite;
        }

        @keyframes pulse-red {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }

        #loading-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            background: #000; color: #FFD700; display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 99999;
            font-family: 'Tajawal', sans-serif;
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px;">جاري مزامنة أدوات التسويق النخبوية...</h2>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

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

        const translations = {
            ar: {
                title: "مركز الإدارة الماسية", marketing: "التسويق والولاء", 
                inventory: "المخزون والأصول", ops: "العمليات", loyalty: "نقاط الولاء",
                offers: "العروض المحدودة", discounts: "إدارة الخصومات", stocks: "عداد المخزون"
            },
            en: {
                title: "Diamond Admin Desk", marketing: "Marketing & Loyalty", 
                inventory: "Assets & Stocks", ops: "Operations", loyalty: "Loyalty Points",
                offers: "Limited Offers", discounts: "Discounts Mgmt", stocks: "Stock Counter"
            }
        };

        const App = () => {
            const [activeTab, setActiveTab] = useState('overview');
            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // بيانات الأصول مع العدادات والخصومات
            const [assets, setAssets] = useState([
                { id: 'p1', name: 'برج السيادة الإداري', stock: 5, price: 1500000, discount: 5, hasOffer: true, offerTime: '02:45:12' },
                { id: 'p2', name: 'دبلوم هندسة الأرباح', stock: 999, price: 499, discount: 0, hasOffer: false },
                { id: 'p3', name: 'منظومة الطاقة X10', stock: 12, price: 12500, discount: 15, hasOffer: true, offerTime: '12:00:00' }
            ]);

            // إعدادات نقاط الولاء
            const [loyaltyConfig, setLoyaltyConfig] = useState({ pointsPerDollar: 1, minToRedeem: 1000 });

            // التنبيهات
            const [notifications, setNotifications] = useState([
                { id: 1, text: "نفاد مخزون 'برج السيادة' قريباً (المتبقي: 2)", type: 'warning' },
                { id: 2, text: "عرض 'منظومة الطاقة' ينتهي خلال ساعة", type: 'offer' }
            ]);

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            const isRTL = lang === 'ar';

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar (القائمة المطورة) --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.9)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-xl"><Icon name="Crown" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase">{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">MR7 Marketing V7.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار الاستراتيجي'},
                                {id: 'marketing', icon: 'Megaphone', label: t.marketing},
                                {id: 'inventory', icon: 'Box', label: t.inventory},
                                {id: 'finance', icon: 'Gift', label: t.loyalty}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === btn.id ? 'bg-white/10 border-r-4 border-yellow-500 text-yellow-500' : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={20} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Area --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* KPI Grid (Top Stats) */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                            <div className="glass-panel p-6 rounded-[2rem] border-r-4 border-yellow-500">
                                <small className="text-gray-500 font-black uppercase">إجمالي نقاط الولاء الموزعة</small>
                                <h4 className="text-3xl font-black mt-2 text-yellow-500">1.2M <small className="text-xs">نقطة</small></h4>
                            </div>
                            <div className="glass-panel p-6 rounded-[2rem] border-r-4 border-red-500">
                                <small className="text-gray-500 font-black uppercase">العروض النشطة</small>
                                <h4 className="text-3xl font-black mt-2 text-red-500">4 <small className="text-xs">عروض</small></h4>
                            </div>
                            <div className="glass-panel p-6 rounded-[2rem] border-r-4 border-green-500">
                                <small className="text-gray-500 font-black uppercase">متوسط الخصومات</small>
                                <h4 className="text-3xl font-black mt-2 text-green-500">12%</h4>
                            </div>
                            <div className="glass-panel p-6 rounded-[2rem] border-r-4 border-blue-500">
                                <small className="text-gray-500 font-black uppercase">الأصول تحت المراجعة</small>
                                <h4 className="text-3xl font-black mt-2 text-blue-500">15</h4>
                            </div>
                        </div>

                        {/* --- Tab: Marketing (Discounts & Offers) --- */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black border-b border-white/10 pb-6 flex items-center gap-4"><Icon name="Zap" className="text-red-500" size={32} /> هندسة العروض والخصومات</h2>
                                
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    {/* 1. قائمة الأصول وتعديل الخصومات */}
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">تحكم بخصومات الأصول</h3>
                                        <div className="space-y-4">
                                            {assets.map(asset => (
                                                <div key={asset.id} className="flex justify-between items-center bg-white/5 p-4 rounded-2xl border border-white/5">
                                                    <div>
                                                        <h5 className="font-bold">{asset.name}</h5>
                                                        <span className="text-[10px] text-gray-400">السعر الأصلي: ${asset.price.toLocaleString()}</span>
                                                    </div>
                                                    <div className="flex items-center gap-3">
                                                        <input type="number" value={asset.discount} className="w-16 premium-input rounded-lg p-2 text-center font-black" />
                                                        <span className="text-sm font-black">% خصم</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* 2. إدارة العروض المؤقتة */}
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">برمجة العروض السريعة (Flash)</h3>
                                        <div className="space-y-6">
                                            <div className="space-y-2">
                                                <label className="text-[10px] text-gray-500 uppercase font-black">اختيار الأصل للعرض</label>
                                                <select className="w-full premium-input rounded-xl p-3 font-bold bg-black">
                                                    {assets.map(a => <option key={a.id}>{a.name}</option>)}
                                                </select>
                                            </div>
                                            <div className="grid grid-cols-2 gap-4">
                                                <div className="space-y-2">
                                                    <label className="text-[10px] text-gray-500 uppercase font-black">مدة العرض (ساعات)</label>
                                                    <input type="number" placeholder="24" className="w-full premium-input rounded-xl p-3 font-bold" />
                                                </div>
                                                <div className="space-y-2">
                                                    <label className="text-[10px] text-gray-500 uppercase font-black">النسبة الاستثنائية %</label>
                                                    <input type="number" placeholder="20" className="w-full premium-input rounded-xl p-3 font-bold" />
                                                </div>
                                            </div>
                                            <button className="w-full py-4 bg-red-500 text-white rounded-2xl font-black text-lg hover:brightness-110 transition-all">إطلاق العرض الصاعق ⚡</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* --- Tab: Inventory (Stock Counter) --- */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black border-b border-white/10 pb-6 flex items-center gap-4"><Icon name="Box" className="text-yellow-500" size={32} /> رادار عداد المنتجات والمخزون</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {assets.map(asset => (
                                        <div key={asset.id} className="glass-panel p-6 rounded-[2.5rem] relative group">
                                            {asset.hasOffer && <span className="absolute top-4 left-4 offer-badge">عرض محدود</span>}
                                            <div className="flex flex-col h-full">
                                                <h4 className="text-xl font-black mb-2">{asset.name}</h4>
                                                <div className="mt-4 mb-6">
                                                    <div className="flex justify-between text-xs font-bold mb-2">
                                                        <span className="text-gray-400">المخزون المتوفر</span>
                                                        <span className={asset.stock < 10 ? 'text-red-500' : 'text-green-500'}>{asset.stock} وحدة</span>
                                                    </div>
                                                    <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                                                        <div className={`h-full ${asset.stock < 10 ? 'bg-red-500' : 'bg-yellow-500'} transition-all`} style={{width: `${Math.min(asset.stock, 100)}%`}}></div>
                                                    </div>
                                                </div>
                                                <div className="flex gap-2">
                                                    <button className="flex-1 bg-white/5 p-2 rounded-xl border border-white/10 font-black text-xs hover:bg-white/10 transition-all">+ زيادة</button>
                                                    <button className="flex-1 bg-white/5 p-2 rounded-xl border border-white/10 font-black text-xs hover:bg-white/10 transition-all">- خصم</button>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* --- Tab: Loyalty Points --- */}
                        {activeTab === 'finance' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black border-b border-white/10 pb-6 flex items-center gap-4"><Icon name="Star" className="text-green-500" size={32} /> هندسة نقاط الولاء السيادية</h2>
                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                    <div className="lg:col-span-1 glass-panel p-8 rounded-[2.5rem] space-y-6">
                                        <h3 className="text-xl font-black">إعدادات النقاط</h3>
                                        <div>
                                            <label className="text-[10px] text-gray-500 font-black block mb-2">نقاط مقابل كل $1 ضخ مالي</label>
                                            <input type="number" value={loyaltyConfig.pointsPerDollar} className="w-full premium-input rounded-xl p-3 font-black" />
                                        </div>
                                        <div>
                                            <label className="text-[10px] text-gray-500 font-black block mb-2">الحد الأدنى للاستبدال (نقطة)</label>
                                            <input type="number" value={loyaltyConfig.minToRedeem} className="w-full premium-input rounded-xl p-3 font-black" />
                                        </div>
                                        <button className="w-full py-4 bg-green-500 text-black rounded-2xl font-black text-lg hover:brightness-110 transition-all">تثبيت نظام الولاء 💾</button>
                                    </div>
                                    
                                    <div className="lg:col-span-2 glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">أفضل 5 شركاء في تجميع النقاط</h3>
                                        <div className="space-y-4">
                                            {[
                                                { name: 'القائد ياسين', points: 45000, level: 'ماسي' },
                                                { name: 'المستثمرة سارة', points: 32000, level: 'ذهبي' },
                                                { name: 'القائد كريم', points: 28000, level: 'فضي' }
                                            ].map((u, i) => (
                                                <div key={i} className="flex justify-between items-center p-4 bg-white/5 rounded-2xl border border-white/5">
                                                    <div className="flex items-center gap-4">
                                                        <div className="w-10 h-10 rounded-full bg-yellow-500/20 text-yellow-500 flex items-center justify-center font-black">{i+1}</div>
                                                        <span className="font-bold">{u.name}</span>
                                                    </div>
                                                    <span className="text-[#00FF88] font-black">{u.points.toLocaleString()} نقطة</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Overview (Radar) */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-4xl font-black text-center mb-12 mt-10">الرادار الاستراتيجي اللحظي 🛰️</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="glass-panel p-10 rounded-[3rem] border-t-8 border-red-500">
                                        <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="AlertTriangle" className="text-red-500"/> تنبيهات العجز والندرة</h3>
                                        <div className="space-y-4">
                                            {notifications.map(n => (
                                                <div key={n.id} className="p-4 bg-red-500/10 rounded-2xl border border-red-500/20 flex items-center gap-4">
                                                    <div className="w-2 h-2 rounded-full bg-red-500"></div>
                                                    <span className="text-sm font-bold">{n.text}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="glass-panel p-10 rounded-[3rem] border-t-8 border-green-500">
                                        <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="Zap" className="text-green-500"/> نبضات السوق</h3>
                                        <p className="text-gray-400 leading-relaxed font-bold">
                                            "إقليم مصر يظهر زيادة في طلب 'برج السيادة' بنسبة 15%. نظام الذكاء الاصطناعي يقترح رفع نقاط الولاء لهذا الأصل بنسبة 5% لتحفيز الضخ السريع."
                                        </p>
                                        <button className="mt-8 bg-green-500 text-black px-8 py-3 rounded-xl font-black hover:scale-105 transition-all">تنفيذ التوصية ✅</button>
                                    </div>
                                </div>
                            </div>
                        )}

                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل آمن ---
final_html = react_html.replace("CURRENT_THEME_PLACEHOLDER", current_theme)
final_html = final_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=1050, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
