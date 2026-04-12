import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Merchant Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة والنمط ---
fb_config_str = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
current_theme = st.session_state.get('app_theme', "غامق إمبراطوري 🖤")
current_balance = st.session_state.get('cash_balance', 1250000)

# --- 3. واجهة React للوحة التاجر السيادي (مع محول الأنماط الديناميكي 7 ألوان) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        body { 
            font-family: 'Tajawal', sans-serif; 
            margin: 0; 
            overflow-x: hidden; 
            scroll-behavior: smooth;
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #888; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
            outline: none;
            background: rgba(255, 255, 255, 0.05);
        }

        .product-card { 
            background: linear-gradient(145deg, rgba(20,20,20,0.9) 0%, rgba(10,10,10,0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        }
        .product-card:hover { 
            transform: translateY(-10px); 
            box-shadow: 0 20px 40px rgba(255, 255, 255, 0.05);
        }
        
        .btn-hover-dynamic { transition: all 0.3s ease; }
        .btn-hover-dynamic:hover {
            transform: scale(1.03);
            filter: brightness(1.1);
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback } = React;

        const Icon = ({ name, size = 24, className = "" }) => {
            const LucideIcon = lucide[name];
            return LucideIcon ? <i data-lucide={name} className={className} style={{ width: size, height: size }}></i> : null;
        };

        const App = () => {
            // --- 7 الأنماط الديناميكية (7 Dynamic Themes) ---
            const themes = {
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", borderLight: "border-[#B8860B]/20", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#FFFFFF" },
                "غامق إمبراطوري 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#111111" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
                "أحمر القوة 🔴": { bg: "bg-[#140000]", text: "text-white", card: "bg-[#2B0000]/80", border: "border-[#FF4136]", borderLight: "border-[#FF4136]/20", accent: "text-[#FF4136]", btn: "bg-[#FF4136]", btnText: "text-white", hex: "#FF4136" },
                "أصفر السيادة 🟡": { bg: "bg-[#141400]", text: "text-white", card: "bg-[#2B2B00]/80", border: "border-[#FFDC00]", borderLight: "border-[#FFDC00]/20", accent: "text-[#FFDC00]", btn: "bg-[#FFDC00]", btnText: "text-black", hex: "#FFDC00" },
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };
            
            const [activeThemeName, setActiveThemeName] = useState("CURRENT_THEME_PLACEHOLDER" || "غامق إمبراطوري 🖤");
            const activeTheme = themes[activeThemeName] || themes["غامق إمبراطوري 🖤"];

            // --- State ---
            const [activeTab, setActiveTab] = useState('overview'); // overview, products, team, services
            const [toasts, setToasts] = useState([]);
            const [products, setProducts] = useState([
                { id: 1, name: 'عقار تجاري في التجمع', price: 250000, category: 'عقارات سيادية', sales: 4, views: 1240, status: 'نشط' },
                { id: 2, name: 'استشارة مالية للشركات', price: 1500, category: 'استشارات', sales: 24, views: 5600, status: 'نشط' }
            ]);
            const [team, setTeam] = useState([
                { id: 1, name: 'أحمد المصري', role: 'مدير مبيعات إقليمي', sales: '$124,000', status: 'نشط 🟢' },
                { id: 2, name: 'سارة خالد', role: 'دعم فني كبار العملاء', sales: '-', status: 'نشط 🟢' },
                { id: 3, name: 'إدريس عثمان', role: 'مسوق سيادي', sales: '$45,200', status: 'خامل 🟡' }
            ]);

            const [newProd, setNewProd] = useState({ name: '', price: '', category: 'عقارات سيادية', desc: '' });

            useEffect(() => { lucide.createIcons(); }, [activeTab, toasts, products, team, activeThemeName]);

            const showToast = useCallback((msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            }, []);

            const handleAddProduct = (e) => {
                e.preventDefault();
                if(!newProd.name || !newProd.price) {
                    showToast('يرجى استكمال البيانات الأساسية للأصل', 'warning');
                    return;
                }
                setProducts([{...newProd, id: Date.now(), sales: 0, views: 0, status: 'قيد المراجعة'}, ...products]);
                setNewProd({ name: '', price: '', category: 'عقارات سيادية', desc: '' });
                showToast('تم رفع الأصل للمراجعة السيادية بنجاح! 🚀');
                setActiveTab('overview');
            };

            const ToastContainer = () => (
                <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                    {toasts.map(t => (
                        <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : `bg-black/90 ${activeTheme.borderLight} ${activeTheme.accent}`}`}>
                            <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                            <span className="font-bold text-sm text-white">{t.msg}</span>
                        </div>
                    ))}
                </div>
            );

            return (
                <div className={`min-h-screen ${activeTheme.bg} ${activeTheme.text} flex flex-col md:flex-row overflow-hidden transition-colors duration-500`}>
                    {/* Sidebar */}
                    <div className={`w-full md:w-72 md:min-h-screen ${activeTheme.card} border-b md:border-b-0 md:border-l ${activeTheme.borderLight} flex flex-col transition-colors duration-500`}>
                        <div className="p-8 pb-4">
                            <div className={`${activeTheme.btn} ${activeTheme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-lg`}>
                                <Icon name="Briefcase" size={28} />
                            </div>
                            <h1 className={`text-2xl font-black uppercase tracking-widest ${activeTheme.accent} mb-1`}>لوحة التاجر</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Sovereign Merchant Hub</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            <button onClick={() => setActiveTab('overview')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-right whitespace-nowrap ${activeTab === 'overview' ? `bg-white/10 border-r-4 ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="LayoutDashboard" size={20} /> نظرة عامة
                            </button>
                            <button onClick={() => setActiveTab('products')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-right whitespace-nowrap ${activeTab === 'products' ? `bg-white/10 border-r-4 ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Package" size={20} /> إدارة الأصول والمخزون
                            </button>
                            <button onClick={() => setActiveTab('team')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-right whitespace-nowrap ${activeTab === 'team' ? `bg-white/10 border-r-4 ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Users" size={20} /> جيش التاجر المساعد
                            </button>
                            <button onClick={() => setActiveTab('services')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-right whitespace-nowrap ${activeTab === 'services' ? `bg-white/10 border-r-4 ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Zap" size={20} /> الخدمات الذكية المعاونة
                            </button>
                        </div>
                        
                        <div className="hidden md:block p-6 mt-auto">
                            {/* --- أزرار تبديل الأنماط (Theme Switcher) --- */}
                            <div className="bg-white/5 p-4 rounded-3xl border border-white/5 text-center mb-4">
                                <span className="block text-xs font-black text-gray-400 uppercase mb-3">تخصيص النمط</span>
                                <div className="flex flex-wrap justify-center gap-2">
                                    {Object.entries(themes).map(([key, theme]) => (
                                        <button 
                                            key={key}
                                            onClick={() => setActiveThemeName(key)}
                                            title={key}
                                            className={`w-6 h-6 rounded-full border-2 transition-all ${activeThemeName === key ? 'border-white scale-125' : 'border-transparent hover:scale-110 opacity-60 hover:opacity-100'}`}
                                            style={{ backgroundColor: theme.hex }}
                                        />
                                    ))}
                                </div>
                            </div>
                            
                            <div className="bg-white/5 p-5 rounded-3xl border border-white/5 text-center">
                                <Icon name="ShieldCheck" size={24} className={`${activeTheme.accent} mx-auto mb-2`} />
                                <span className="block text-xs font-black text-gray-400 uppercase">تاجر معتمد</span>
                                <span className={`block ${activeTheme.accent} font-bold text-sm mt-1`}>الجيل الثالث</span>
                            </div>
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar">
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="flex items-center justify-between mb-8">
                                    <h2 className="text-3xl font-black">مؤشرات الأداء الاستراتيجية 📊</h2>
                                    <button className="bg-white/10 px-6 py-3 rounded-xl font-bold text-sm hover:bg-white/20 transition-colors flex items-center gap-2">
                                        <Icon name="Download" size={16} /> استخراج تقرير
                                    </button>
                                </div>
                                
                                {/* KPI Cards */}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute -right-4 -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="TrendingUp" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">المبيعات الإجمالية</p>
                                        <h4 className="text-3xl font-black text-[#00FF88]">$1,036,000</h4>
                                        <span className={`text-xs ${activeTheme.accent} font-black mt-3 flex items-center gap-1`}><Icon name="ArrowUpRight" size={14}/> +15.4% هذا الربع</span>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className="absolute -right-4 -top-4 opacity-5 text-white group-hover:scale-110 transition-transform"><Icon name="Package" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">الأصول النشطة بالسوق</p>
                                        <h4 className="text-3xl font-black text-white">{products.length}</h4>
                                        <span className="text-xs text-gray-500 font-black mt-3 block">جميعها مفعلة</span>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute -right-4 -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="Eye" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">زيارات أصولك</p>
                                        <h4 className="text-3xl font-black text-white">6,840</h4>
                                        <span className="text-xs text-[#00FF88] font-black mt-3 flex items-center gap-1"><Icon name="ArrowUpRight" size={14}/> +2.1% الأسبوع الماضي</span>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute -right-4 -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="Users" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">الفريق المعاون</p>
                                        <h4 className="text-3xl font-black text-white">{team.length}</h4>
                                        <span className="text-xs text-gray-500 font-black mt-3 block">1 بانتظار الاعتماد</span>
                                    </div>
                                </div>

                                {/* Recent Orders/Products */}
                                <div className={`${activeTheme.card} p-8 rounded-[2rem] border ${activeTheme.borderLight} transition-colors`}>
                                    <h3 className="text-xl font-black mb-6 border-b border-white/5 pb-4">حالة الأصول الاستراتيجية</h3>
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-right border-collapse">
                                            <thead>
                                                <tr className="text-gray-400 text-sm uppercase tracking-widest border-b border-white/10">
                                                    <th className="pb-4 font-black">اسم الأصل</th>
                                                    <th className="pb-4 font-black">القسم</th>
                                                    <th className="pb-4 font-black">القيمة</th>
                                                    <th className="pb-4 font-black">المبيعات</th>
                                                    <th className="pb-4 font-black">الحالة</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {products.map(p => (
                                                    <tr key={p.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                        <td className="py-4 font-bold">{p.name}</td>
                                                        <td className="py-4 text-gray-400 text-sm">{p.category}</td>
                                                        <td className="py-4 font-black text-[#00FF88]">${Number(p.price).toLocaleString()}</td>
                                                        <td className="py-4 font-bold">{p.sales}</td>
                                                        <td className="py-4">
                                                            <span className={`px-3 py-1 rounded-lg text-xs font-black ${p.status === 'نشط' ? 'bg-[#00FF88]/20 text-[#00FF88]' : `${activeTheme.bg} ${activeTheme.accent} opacity-80`}`}>{p.status}</span>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'products' && (
                            <div className="animate-view space-y-8 max-w-4xl mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="PlusCircle" className={activeTheme.accent} size={32} /> طرح أصل جديد للسوق
                                </h2>
                                
                                <form onSubmit={handleAddProduct} className={`${activeTheme.card} p-8 md:p-10 rounded-[3rem] border ${activeTheme.borderLight} shadow-2xl transition-colors`}>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                                        <div className="space-y-3">
                                            <label className="text-xs font-black text-gray-400 uppercase tracking-widest">اسم الأصل / المنتج</label>
                                            <input type="text" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border}`} value={newProd.name} onChange={e => setNewProd({...newProd, name: e.target.value})} placeholder="مثال: يخت قيادي فاخر..." />
                                        </div>
                                        <div className="space-y-3">
                                            <label className="text-xs font-black text-gray-400 uppercase tracking-widest">القيمة التسويقية ($)</label>
                                            <input type="number" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border}`} value={newProd.price} onChange={e => setNewProd({...newProd, price: e.target.value})} placeholder="0.00" />
                                        </div>
                                        <div className="space-y-3">
                                            <label className="text-xs font-black text-gray-400 uppercase tracking-widest">القسم الاستراتيجي</label>
                                            <select className={`w-full premium-input rounded-2xl py-4 px-5 font-bold text-white bg-black appearance-none focus:${activeTheme.border}`} value={newProd.category} onChange={e => setNewProd({...newProd, category: e.target.value})}>
                                                <option>عقارات سيادية</option>
                                                <option>أكاديمية القيادة</option>
                                                <option>تقنيات المستقبل</option>
                                                <option>أصول فاخرة</option>
                                            </select>
                                        </div>
                                        <div className="space-y-3">
                                            <label className="text-xs font-black text-gray-400 uppercase tracking-widest">النطاق الجغرافي للتوفر</label>
                                            <select className={`w-full premium-input rounded-2xl py-4 px-5 font-bold text-white bg-black appearance-none focus:${activeTheme.border}`}>
                                                <option>مصر</option>
                                                <option>ليبيا</option>
                                                <option>السودان</option>
                                                <option>عالمي</option>
                                            </select>
                                        </div>
                                        <div className="md:col-span-2 space-y-3">
                                            <label className="text-xs font-black text-gray-400 uppercase tracking-widest">الوصف الذكي (سيتم تحسينه عبر الذكاء الاصطناعي تلقائياً)</label>
                                            <textarea className={`w-full premium-input rounded-2xl py-4 px-5 font-bold min-h-[120px] focus:${activeTheme.border}`} value={newProd.desc} onChange={e => setNewProd({...newProd, desc: e.target.value})} placeholder="اشرح القيمة المضافة لهذا الأصل ليجذب القادة للاستحواذ عليه..."></textarea>
                                        </div>
                                    </div>
                                    <button type="submit" className={`w-full py-6 rounded-[2rem] font-black text-xl ${activeTheme.btn} ${activeTheme.btnText} btn-hover-dynamic flex items-center justify-center gap-3`}>
                                        <Icon name="UploadCloud" /> اعتماد وإرسال للمراجعة السيادية
                                    </button>
                                </form>
                            </div>
                        )}

                        {activeTab === 'team' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="flex justify-between items-center mb-8 border-b border-white/10 pb-6">
                                    <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Users" className={activeTheme.accent} size={32} /> جيش التاجر المعاون</h2>
                                    <button onClick={() => showToast('تم إرسال دعوة انضمام!', 'success')} className={`bg-white/10 hover:${activeTheme.btn} hover:${activeTheme.btnText} px-6 py-3 rounded-xl font-bold transition-colors flex items-center gap-2`}>
                                        <Icon name="UserPlus" size={18} /> دعوة عضو جديد
                                    </button>
                                </div>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {team.map(member => (
                                        <div key={member.id} className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} relative overflow-hidden transition-colors`}>
                                            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mb-4 text-2xl">👤</div>
                                            <h4 className="text-xl font-black mb-1">{member.name}</h4>
                                            <p className={`text-sm font-bold mb-6 ${activeTheme.accent}`}>{member.role}</p>
                                            <div className="flex justify-between items-center border-t border-white/10 pt-4">
                                                <span className="text-xs text-gray-500 uppercase font-black">المبيعات: <span className="text-white text-sm">{member.sales}</span></span>
                                                <span className="text-xs font-black">{member.status}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {activeTab === 'services' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="Zap" className={activeTheme.accent} size={32} /> الخدمات الذكية المعاونة
                                </h2>
                                <p className="text-gray-400 text-lg mb-10">ارتقِ بمتجرك السيادي عبر تفعيل خدمات الإمبراطورية المعاونة التي تعمل بالنيابة عنك.</p>
                                
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:border-[#00FF88] transition-colors`}>
                                        <div className="bg-[#00FF88]/10 text-[#00FF88] p-5 rounded-3xl mb-6"><Icon name="Bot" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">وكيل مبيعات AI</h4>
                                        <p className="text-gray-400 text-sm mb-8 leading-relaxed">روبوت ذكاء اصطناعي يقوم بالرد على استفسارات المشترين وإقناعهم بإتمام الاستحواذ 24/7.</p>
                                        <button onClick={() => showToast('تم تفعيل وكيل الذكاء الاصطناعي لمتجرك')} className="mt-auto w-full py-4 bg-white/5 hover:bg-[#00FF88] hover:text-black rounded-xl font-black transition-all">تفعيل الخدمة ($50/شهر)</button>
                                    </div>
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:${activeTheme.border} transition-colors`}>
                                        <div className={`bg-white/10 ${activeTheme.accent} p-5 rounded-3xl mb-6`}><Icon name="Megaphone" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">حملة ضخ إقليمية</h4>
                                        <p className="text-gray-400 text-sm mb-8 leading-relaxed">ترويج أصولك بقوة داخل شبكة القادة في إقليم معين لضمان مبيعات فورية.</p>
                                        <button onClick={() => showToast('سيتم توجيهك لمدير الحملات الإقليمية')} className={`mt-auto w-full py-4 bg-white/5 hover:${activeTheme.btn} hover:${activeTheme.btnText} rounded-xl font-black transition-all`}>طلب حملة (مخصص)</button>
                                    </div>
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:border-[#0074D9] transition-colors`}>
                                        <div className="bg-[#0074D9]/10 text-[#0074D9] p-5 rounded-3xl mb-6"><Icon name="FileSignature" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">التوثيق القانوني السيادي</h4>
                                        <p className="text-gray-400 text-sm mb-8 leading-relaxed">إسناد عملية صياغة عقود الملكية للمشترين للإدارة القانونية بالإمبراطورية.</p>
                                        <button onClick={() => showToast('تم ربط متجرك بالخدمة القانونية')} className="mt-auto w-full py-4 bg-white/5 hover:bg-[#0074D9] hover:text-white rounded-xl font-black transition-all">تفعيل التوثيق التلقائي</button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                    
                    <ToastContainer />
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
components.html(final_html, height=900, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
