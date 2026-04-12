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

# --- 3. واجهة React المتقدمة (الإصدار 15.0 - الهوية الكاملة والعقل الاقتصادي) ---
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
            color: inherit;
            transition: all 0.3s ease;
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        .chat-bubble-client { background: rgba(255,255,255,0.05); border-radius: 15px 15px 0 15px; margin: 10px 0; padding: 12px; }
        .chat-bubble-merchant { background: rgba(255,215,0,0.1); border-radius: 15px 15px 15px 0; margin: 10px 0; padding: 12px; border-right: 3px solid #FFD700; }

        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

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
        <h2 style="margin-top:20px;">جاري تشغيل مركز القيادة الموحد...</h2>
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

        const App = () => {
            // --- 1. الأنماط السبعة (7 Themes) ---
            const themes = {
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", borderLight: "border-[#B8860B]/20", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#FFFFFF" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
                "أحمر القوة 🔴": { bg: "bg-[#140000]", text: "text-white", card: "bg-[#2B0000]/80", border: "border-[#FF4136]", borderLight: "border-[#FF4136]/20", accent: "text-[#FF4136]", btn: "bg-[#FF4136]", btnText: "text-white", hex: "#FF4136" },
                "أصفر الريادة 🟡": { bg: "bg-[#141400]", text: "text-white", card: "bg-[#2B2B00]/80", border: "border-[#FFDC00]", borderLight: "border-[#FFDC00]/20", accent: "text-[#FFDC00]", btn: "bg-[#FFDC00]", btnText: "text-black", hex: "#FFDC00" },
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };

            const [activeThemeName, setActiveThemeName] = useState("أسود قيادي 🖤");
            const theme = themes[activeThemeName] || themes["أسود قيادي 🖤"];

            // --- 2. اللغات السبعة (7 Languages) ---
            const translations = {
                ar: { title: "مركز القيادة", overview: "الرادار", inventory: "الأصول", ops: "العمليات", comms: "التواصل", finance: "المالية", search: "البحث الشامل...", add: "نشر أصل جديد", levels: "تخصيص عمولات الأجيال", buyer: "المشتري", amount: "القيمة", status: "الحالة", send: "إرسال" },
                en: { title: "Command Hub", overview: "Radar", inventory: "Assets", ops: "Ops", comms: "Comms", finance: "Finance", search: "Global Search...", add: "Publish Asset", levels: "Multi-level Commissions", buyer: "Buyer", amount: "Amount", status: "Status", send: "Send" },
                fr: { title: "Centre de Commande", overview: "Radar", inventory: "Actifs", ops: "Ops", comms: "Comms", finance: "Finances", search: "Recherche...", add: "Publier l'actif", levels: "Commissions multiniveaux", buyer: "Acheteur", amount: "Montant", status: "Statut", send: "Envoyer" },
                es: { title: "Centro de Mando", overview: "Radar", inventory: "Activos", ops: "Ops", comms: "Comms", finance: "Finanzas", search: "Buscar...", add: "Publicar activo", levels: "Comisiones multinivel", buyer: "Comprador", amount: "Monto", status: "Estado", send: "Enviar" },
                zh: { title: "指挥中心", overview: "雷达", inventory: "资产", ops: "操作", comms: "通信", finance: "金融", search: "搜索...", add: "发布资产", levels: "多级佣金", buyer: "买方", amount: "金额", status: "状态", send: "发送" },
                fa: { title: "مرکز فرماندهی", overview: "رادار", inventory: "دارایی‌ها", ops: "عملیات", comms: "ارتباطات", finance: "مالی", search: "جستجو...", add: "انتشار دارایی", levels: "کمیسیون‌های چند سطحی", buyer: "خریدار", amount: "ارزش", status: "وضعیت", send: "ارسال" },
                sw: { title: "Kituo cha Amri", overview: "Rada", inventory: "Mali", ops: "Operesheni", comms: "Mawasiliano", finance: "Fedha", search: "Tafuta...", add: "Chapisha Mali", levels: "Tume za ngazi nyingi", buyer: "Mnunuzi", amount: "Thamani", status: "Hali", send: "Tuma" }
            };

            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // --- Global State ---
            const [activeTab, setActiveTab] = useState('overview');
            const [toasts, setToasts] = useState([]);
            const [balance, setBalance] = useState(Number(LEADER_BALANCE_PLACEHOLDER));
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);

            // Logic State
            const [assets, setAssets] = useState([
                { id: 1, name: 'برج السيادة الإداري', price: 1500000, commRates: [10,5,2,1,1,1,1,1,1,1], stock: 5, type: 'عقاري', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400', desc: 'مقر قيادي عالمي.' },
                { id: 2, name: 'دبلوم هندسة الأرباح', price: 499, commRates: [15,7,3,1,1,1,1,1,1,1], stock: Infinity, type: 'رقمي', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400', desc: 'صناعة عقلية المليار.' }
            ]);

            const [orders, setOrders] = useState([
                { id: 'ORD-202', buyer: 'أحمد القائد', item: 'برج السيادة', amount: 1500000, status: 'قيد المراجعة', date: 'اليوم' }
            ]);
            
            const [chats, setChats] = useState([
                { id: 1, sender: 'أحمد القائد', type: 'Client', lastMsg: 'هل هناك تسهيلات دفع؟', time: '10:30 AM', unread: true }
            ]);
            const [activeChat, setActiveChat] = useState(null);
            const [messageText, setMessageText] = useState('');

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            const handleAddAsset = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                const n = {
                    id: Date.now(),
                    name: f.get('name'), price: parseFloat(f.get('price')),
                    commRates: Array.from({length:10}).map((_,i)=>parseFloat(f.get(`c${i+1}`)||1)),
                    stock: f.get('type') === 'رقمي' ? Infinity : parseInt(f.get('stock')),
                    type: f.get('type'), img: f.get('img'), desc: f.get('desc'), status: 'نشط'
                };
                setAssets([n, ...assets]);
                showToast(lang === 'ar' ? 'تم التوثيق بنجاح' : 'Success');
                e.target.reset();
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
                document.documentElement.dir = (lang === 'ar' || lang === 'fa') ? 'rtl' : 'ltr';
            }, [lang]);

            const isRTL = lang === 'ar' || lang === 'fa';

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col md:flex-row overflow-hidden transition-all duration-500`}>
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${theme.card} border-b md:border-b-0 md:border-l ${theme.borderLight} flex flex-col z-10 shadow-2xl`}>
                        
                        <div className="p-6 pb-2 flex justify-between items-center">
                            {/* Theme Picker Container */}
                            <div className="relative">
                                <button onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)} className="w-8 h-8 rounded-full border-2 border-white/20 shadow-lg" style={{backgroundColor: theme.hex}}></button>
                                {isThemeMenuOpen && (
                                    <div className={`absolute top-10 ${isRTL ? 'right-0' : 'left-0'} glass-panel p-2 rounded-xl flex flex-col gap-2 z-[100] animate-view`}>
                                        {Object.entries(themes).map(([name, t]) => (
                                            <button key={name} onClick={() => {setActiveThemeName(name); setIsThemeMenuOpen(false);}} className="w-6 h-6 rounded-full border border-white/10" style={{backgroundColor: t.hex}} title={name}></button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Lang Picker Container */}
                            <div className="relative">
                                <button onClick={() => setIsLangMenuOpen(!isLangMenuOpen)} className="flex items-center gap-2 px-3 py-1 bg-white/5 rounded-lg border border-white/10 text-[10px] font-bold">
                                    <Icon name="Globe" size={14} /> {lang.toUpperCase()}
                                </button>
                                {isLangMenuOpen && (
                                    <div className={`absolute top-10 ${isRTL ? 'left-0' : 'right-0'} glass-panel p-2 rounded-xl flex flex-col gap-1 z-[100] animate-view min-w-[80px]`}>
                                        {Object.keys(translations).map(l => (
                                            <button key={l} onClick={() => {setLang(l); setIsLangMenuOpen(false);}} className="text-[10px] font-bold py-1 hover:bg-white/10 rounded uppercase">{l}</button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="p-8 pt-4">
                            <div className={`${theme.btn} ${theme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-xl`}><Icon name="Terminal" size={30} /></div>
                            <h1 className={`text-xl font-black uppercase tracking-tighter ${theme.accent}`}>{t.title}</h1>
                            <p className="text-[10px] opacity-50 font-bold uppercase">MR7 Logic v15.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: t.overview},
                                {id: 'inventory', icon: 'Box', label: t.inventory},
                                {id: 'operations', icon: 'Zap', label: t.ops},
                                {id: 'communications', icon: 'MessageSquare', label: t.comms},
                                {id: 'finance', icon: 'CreditCard', label: t.finance}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 ${isRTL ? 'border-r-4' : 'border-l-4'} ${theme.border} ${theme.accent}` : 'opacity-50 hover:opacity-100 hover:bg-white/5'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir relative">
                        
                        <div className="flex flex-col md:flex-row gap-6 mb-10 items-center justify-between">
                            <div className="flex-1 max-w-xl w-full relative">
                                <Icon name="Search" size={18} className={`absolute ${isRTL ? 'right-4' : 'left-4'} top-1/2 -translate-y-1/2 opacity-30`} />
                                <input placeholder={t.search} className="w-full premium-input py-4 rounded-2xl pr-12 pl-4 text-sm font-bold shadow-xl outline-none border-transparent focus:border-yellow-500/30" />
                            </div>
                            <div className={`${theme.card} px-6 py-3 rounded-2xl border ${theme.borderLight} flex items-center gap-4`}>
                                <div className="text-left">
                                    <span className="text-[10px] opacity-40 font-black uppercase">Liquidity Vault</span>
                                    <h4 className="text-xl font-black text-[#00FF88]">${balance.toLocaleString()}</h4>
                                </div>
                                <Icon name="Wallet" size={24} className={theme.accent} />
                            </div>
                        </div>

                        {/* Views Logic */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className={`${theme.card} p-6 rounded-[2rem] border-t-4 border-green-500 shadow-xl`}>
                                        <small className="opacity-50 font-bold uppercase">Total ROI</small>
                                        <h4 className="text-2xl font-black text-green-500">$3.1M</h4>
                                    </div>
                                    <div className={`${theme.card} p-6 rounded-[2rem] border-t-4 border-yellow-500`}>
                                        <small className="opacity-50 font-bold uppercase">Pending Orders</small>
                                        <h4 className="text-2xl font-black">{orders.length}</h4>
                                    </div>
                                    <div className={`${theme.card} p-6 rounded-[2rem] border-t-4 border-blue-500`}>
                                        <small className="opacity-50 font-bold uppercase">Loyalty Points</small>
                                        <h4 className="text-2xl font-black text-blue-500">124K</h4>
                                    </div>
                                    <div className={`${theme.card} p-6 rounded-[2rem] border-t-4 border-purple-500`}>
                                        <small className="opacity-50 font-bold uppercase">Active Assets</small>
                                        <h4 className="text-2xl font-black">{assets.length}</h4>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col xl:flex-row gap-8">
                                    <div className={`${theme.card} xl:w-2/5 p-8 rounded-[2.5rem] h-fit border ${theme.borderLight}`}>
                                        <h3 className="text-lg font-black mb-6 flex items-center gap-3"><Icon name="PlusCircle" className={theme.accent}/> {t.add}</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="Name..." required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="price" type="number" placeholder="Price ($)" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black/50 text-sm">
                                                    <option>عقاري</option><option>منتج</option><option>رقمي</option>
                                                </select>
                                            </div>
                                            <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                                                <label className="text-[10px] opacity-50 font-black uppercase block mb-3">{t.levels} (10 Levels %)</label>
                                                <div className="grid grid-cols-5 gap-2">
                                                    {Array.from({length: 10}).map((_, i) => (
                                                        <input key={i} name={`c${i+1}`} placeholder={`L${i+1}`} className="premium-input p-2 rounded-lg text-center text-xs font-bold" />
                                                    ))}
                                                </div>
                                            </div>
                                            <input name="img" placeholder="Image URL..." className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            <textarea name="desc" placeholder="Description..." className="w-full premium-input p-4 rounded-xl font-bold h-20 text-sm"></textarea>
                                            <button type="submit" className={`w-full py-4 ${theme.btn} ${theme.btnText} rounded-xl font-black text-lg transition-all shadow-xl`}>PROCEED 🚀</button>
                                        </form>
                                    </div>

                                    <div className={`${theme.card} xl:w-3/5 p-8 rounded-[2.5rem] overflow-x-auto border ${theme.borderLight}`}>
                                        <h3 className="text-lg font-black mb-6">Inventory Ledger</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="opacity-40 text-[10px] border-b border-white/5 uppercase">
                                                    <th className="pb-4 text-right">Asset</th>
                                                    <th className="pb-4 text-center">Stock</th>
                                                    <th className="pb-4 text-center">Price</th>
                                                    <th className="pb-4 text-center">Action</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all group">
                                                        <td className="py-4 flex items-center gap-4">
                                                            <img src={a.img} className="w-12 h-12 rounded-xl object-cover" />
                                                            <div><div className="font-bold text-sm">{a.name}</div><small className="opacity-40">{a.type}</small></div>
                                                        </td>
                                                        <td className="py-4 text-center font-black">{a.stock === Infinity ? '∞' : a.stock}</td>
                                                        <td className="py-4 text-center text-[#00FF88] font-black">${a.price.toLocaleString()}</td>
                                                        <td className="py-4 text-center"><button onClick={()=>setAssets(assets.filter(as=>as.id!==a.id))} className="text-red-500/50 hover:text-red-500"><Icon name="Trash2" size={16}/></button></td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'communications' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto h-[70vh]">
                                <div className="flex h-full gap-6">
                                    <div className={`${theme.card} w-1/3 rounded-[2.5rem] flex flex-col overflow-hidden border ${theme.borderLight}`}>
                                        <div className="p-6 border-b border-white/5 flex justify-between items-center"><h3 className="font-black uppercase">{t.comms}</h3><Icon name="Filter" size={18} className="opacity-20" /></div>
                                        <div className="flex-1 overflow-y-auto no-scrollbar p-2">
                                            {chats.map(chat => (
                                                <div key={chat.id} onClick={() => setActiveChat(chat)} className={`p-4 rounded-2xl cursor-pointer transition-all mb-2 ${activeChat?.id === chat.id ? 'bg-white/10' : 'hover:bg-white/5'}`}>
                                                    <div className="flex justify-between items-start mb-1"><span className="font-black text-sm">{chat.sender}</span><small className="opacity-30">{chat.time}</small></div>
                                                    <p className="text-[11px] opacity-50 truncate">{chat.lastMsg}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className={`${theme.card} w-2/3 rounded-[2.5rem] flex flex-col overflow-hidden relative border ${theme.borderLight}`}>
                                        {activeChat ? (
                                            <>
                                                <div className="p-6 border-b border-white/5 bg-white/5 flex items-center justify-between">
                                                    <div className="flex items-center gap-4"><div className={`${theme.btn} ${theme.btnText} w-10 h-10 rounded-full flex items-center justify-center font-black`}>👤</div><h4 className="font-black">{activeChat.sender}</h4></div>
                                                </div>
                                                <div className="flex-1 p-6 overflow-y-auto no-scrollbar space-y-4">
                                                    <div className="chat-bubble-client"><p className="text-sm">أهلاً يا قائد، مهتم بشراء برج السيادة.</p></div>
                                                    <div className="chat-bubble-merchant"><p className="text-sm">أهلاً بك. متاح لدينا أنظمة تقسيط استراتيجية.</p></div>
                                                </div>
                                                <div className="p-6 border-t border-white/5 bg-black/20 flex gap-4">
                                                    <input value={messageText} onChange={(e)=>setMessageText(e.target.value)} placeholder={t.send + "..."} className="flex-1 premium-input p-4 rounded-xl font-bold text-sm" />
                                                    <button onClick={()=>{showToast('SENT'); setMessageText('')}} className={`${theme.btn} ${theme.btnText} px-8 rounded-xl font-black`}><Icon name="Send" size={20}/></button>
                                                </div>
                                            </>
                                        ) : (
                                            <div className="h-full flex flex-col items-center justify-center opacity-20"><Icon name="MessageSquare" size={60} className="mb-4" /><p className="text-xl font-black">SELECT COMMANDER</p></div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-2xl font-black flex items-center gap-4"><Icon name="RefreshCcw" size={28} /> {t.ops}</h2>
                                {orders.map(o => (
                                    <div key={o.id} className={`${theme.card} p-6 rounded-[2rem] border ${theme.borderLight} flex justify-between items-center`}>
                                        <div><h4 className="font-black text-xl">{o.buyer}</h4><p className="text-xs opacity-50">{o.item} • {o.date}</p></div>
                                        <div className="flex items-center gap-6">
                                            <span className="text-2xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                            <button className={`${theme.btn} ${theme.btnText} px-6 py-2 rounded-xl font-black text-xs`}>APPROVE</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                    </div>

                    {/* Toasts */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : 'bg-black/90 border-red-500/40 text-red-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                                <span className="font-bold text-sm text-white">{t.msg}</span>
                            </div>
                        ))}
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
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=1150, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
