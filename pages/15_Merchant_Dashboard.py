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

# --- 3. واجهة React للوحة التاجر السيادي (مستقرة 100% وخالية من الانهيارات) ---
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
            transition: background-color 0.5s, color 0.5s;
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
            transition: all 0.5s;
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

        /* تعديلات الاتجاه للغات الأجنبية */
        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef } = React;

        // الحل الجذري لمشكلة الشاشة البيضاء: 
        // فصل الأيقونات عن React Virtual DOM لمنع انهيار التطبيق
        const Icon = ({ name, size = 24, className = "", fill = "none" }) => {
            const iconRef = useRef(null);

            useEffect(() => {
                if (iconRef.current) {
                    // تفريغ العنصر لضمان عدم وجود تكرار
                    iconRef.current.innerHTML = '';
                    
                    // إنشاء الأيقونة يدوياً لحمايتها من تحديثات React
                    const i = document.createElement('i');
                    i.setAttribute('data-lucide', name);
                    i.setAttribute('class', className);
                    i.setAttribute('fill', fill);
                    i.style.width = size + 'px';
                    i.style.height = size + 'px';
                    
                    iconRef.current.appendChild(i);
                    
                    // تطبيق مكتبة lucide على هذا العنصر فقط!
                    lucide.createIcons({ root: iconRef.current });
                }
            }, [name, size, className, fill]);

            return <span ref={iconRef} className="inline-flex justify-center items-center"></span>;
        };

        // --- قاموس الترجمة (Multi-Language Dictionary) ---
        const translations = {
            ar: {
                dashboardTitle: "لوحة التاجر",
                dashboardSub: "Sovereign Merchant Hub",
                searchPlaceholder: "البحث الشامل عن الأصول الإمبراطورية...",
                liquidity: "خزنة السيولة",
                overview: "نظرة عامة",
                assets: "إدارة الأصول والمخزون",
                team: "جيش التاجر المساعد",
                services: "الخدمات الذكية المعاونة",
                certified: "تاجر معتمد",
                gen: "الجيل الثالث",
                kpiTitle: "مؤشرات الأداء الاستراتيجية 📊",
                sales: "المبيعات الإجمالية",
                activeAssets: "الأصول النشطة بالسوق",
                views: "زيارات أصولك",
                teamMembers: "الفريق المعاون",
                newProduct: "طرح أصل جديد للسوق",
                addAsset: "اعتماد وإرسال للمراجعة السيادية",
                aiAgent: "وكيل مبيعات AI",
                regionalCamp: "حملة ضخ إقليمية",
                legalDoc: "التوثيق القانوني السيادي",
                successAdded: "تم رفع الأصل للمراجعة السيادية بنجاح! 🚀"
            },
            en: {
                dashboardTitle: "Merchant Hub",
                dashboardSub: "Sovereign Merchant Hub",
                searchPlaceholder: "Search Imperial Assets...",
                liquidity: "Liquidity Vault",
                overview: "Overview",
                assets: "Asset Management",
                team: "Merchant Army",
                services: "Smart Services",
                certified: "Certified Merchant",
                gen: "3rd Generation",
                kpiTitle: "Strategic KPIs 📊",
                sales: "Total Sales",
                activeAssets: "Active Assets",
                views: "Asset Views",
                teamMembers: "Support Team",
                newProduct: "List New Asset",
                addAsset: "Submit for Sovereign Review",
                aiAgent: "AI Sales Agent",
                regionalCamp: "Regional Campaign",
                legalDoc: "Legal Documentation",
                successAdded: "Asset successfully submitted for review! 🚀"
            },
            fr: {
                dashboardTitle: "Hub Marchand",
                dashboardSub: "Hub Marchand Souverain",
                searchPlaceholder: "Rechercher des Actifs...",
                liquidity: "Coffre de Liquidité",
                overview: "Aperçu",
                assets: "Gestion des Actifs",
                team: "Armée Marchande",
                services: "Services Intelligents",
                certified: "Marchand Certifié",
                gen: "3ème Génération",
                kpiTitle: "KPI Stratégiques 📊",
                sales: "Ventes Totales",
                activeAssets: "Actifs Actifs",
                views: "Vues des Actifs",
                teamMembers: "Équipe de Soutien",
                newProduct: "Lister Nouvel Actif",
                addAsset: "Soumettre pour Examen",
                aiAgent: "Agent de Vente IA",
                regionalCamp: "Campagne Régionale",
                legalDoc: "Documentation Légale",
                successAdded: "Actif soumis avec succès ! 🚀"
            },
            es: {
                dashboardTitle: "Centro Comercial",
                dashboardSub: "Centro Comercial Soberano",
                searchPlaceholder: "Buscar Activos...",
                liquidity: "Bóveda de Liquidez",
                overview: "Visión General",
                assets: "Gestión de Activos",
                team: "Ejército Comercial",
                services: "Servicios Inteligentes",
                certified: "Comerciante Certificado",
                gen: "3ª Generación",
                kpiTitle: "KPI Estratégicos 📊",
                sales: "Ventas Totales",
                activeAssets: "Activos Activos",
                views: "Vistas de Activos",
                teamMembers: "Equipo de Apoyo",
                newProduct: "Listar Nuevo Activo",
                addAsset: "Enviar para Revisión",
                aiAgent: "Agente de Ventas IA",
                regionalCamp: "Campaña Regional",
                legalDoc: "Documentación Legal",
                successAdded: "¡Activo enviado con éxito! 🚀"
            }
        };

        const App = () => {
            // --- 7 الأنماط الديناميكية (7 Dynamic Themes) ---
            const themes = {
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", borderLight: "border-[#B8860B]/20", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#E5B80B" },
                "غامق إمبراطوري 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#FFD700" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
                "أحمر القوة 🔴": { bg: "bg-[#140000]", text: "text-white", card: "bg-[#2B0000]/80", border: "border-[#FF4136]", borderLight: "border-[#FF4136]/20", accent: "text-[#FF4136]", btn: "bg-[#FF4136]", btnText: "text-white", hex: "#FF4136" },
                "أصفر السيادة 🟡": { bg: "bg-[#141400]", text: "text-white", card: "bg-[#2B2B00]/80", border: "border-[#FFDC00]", borderLight: "border-[#FFDC00]/20", accent: "text-[#FFDC00]", btn: "bg-[#FFDC00]", btnText: "text-black", hex: "#FFDC00" },
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };
            
            const [activeThemeName, setActiveThemeName] = useState("CURRENT_THEME_PLACEHOLDER" || "غامق إمبراطوري 🖤");
            const activeTheme = themes[activeThemeName] || themes["غامق إمبراطوري 🖤"];
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);

            // --- Multi-language State ---
            const [lang, setLang] = useState('ar');
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            const t = translations[lang];

            useEffect(() => {
                document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
            }, [lang]);

            // --- State ---
            const [activeTab, setActiveTab] = useState('overview'); 
            const [toasts, setToasts] = useState([]);
            const [products, setProducts] = useState([
                { id: 1, name: 'عقار تجاري في التجمع', price: 250000, category: 'عقارات سيادية', sales: 4, views: 1240, status: 'نشط' }
            ]);
            const [team, setTeam] = useState([
                { id: 1, name: 'أحمد المصري', role: 'مدير مبيعات', sales: '$124,000', status: 'نشط 🟢' }
            ]);

            const [newProd, setNewProd] = useState({ name: '', price: '', category: 'عقارات سيادية', desc: '' });

            const showToast = useCallback((msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            }, []);

            const handleAddProduct = (e) => {
                e.preventDefault();
                if(!newProd.name || !newProd.price) {
                    showToast('يرجى استكمال البيانات الأساسية', 'warning');
                    return;
                }
                setProducts([{...newProd, id: Date.now(), sales: 0, views: 0, status: 'قيد المراجعة'}, ...products]);
                setNewProd({ name: '', price: '', category: 'عقارات سيادية', desc: '' });
                showToast(t.successAdded);
                setActiveTab('overview');
            };

            const ToastContainer = () => (
                <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                    {toasts.map(toast => (
                        <div key={toast.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${toast.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : `bg-black/90 ${activeTheme.borderLight} ${activeTheme.accent}`}`}>
                            <Icon name={toast.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                            <span className="font-bold text-sm text-white text-dir">{toast.msg}</span>
                        </div>
                    ))}
                </div>
            );

            return (
                <div className={`min-h-screen ${activeTheme.bg} ${activeTheme.text} flex flex-col md:flex-row overflow-hidden transition-colors duration-500`}>
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${activeTheme.card} border-b md:border-b-0 md:border-l ${activeTheme.borderLight} flex flex-col transition-colors duration-500`}>
                        
                        {/* Global Controls (Theme & Lang) */}
                        <div className="p-6 pb-2 flex justify-between items-center dir-invert">
                            {/* Theme Picker Floating Button */}
                            <div className="relative z-[200]">
                                <button 
                                    onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)} 
                                    className={`w-10 h-10 rounded-full border-2 border-white/20 shadow-lg flex items-center justify-center hover:scale-110 transition-transform`}
                                    style={{backgroundColor: activeTheme.hex}}
                                    title="تغيير النمط"
                                ></button>
                                
                                {isThemeMenuOpen && (
                                    <div className={`absolute top-12 ${lang === 'ar' ? 'right-0' : 'left-0'} glass-panel p-2 rounded-2xl flex flex-col gap-2 shadow-2xl animate-view`}>
                                        {Object.entries(themes).map(([key, theme]) => (
                                            <button 
                                                key={key}
                                                onClick={() => { setActiveThemeName(key); setIsThemeMenuOpen(false); }}
                                                title={key}
                                                className={`w-8 h-8 rounded-full border-2 transition-all ${activeThemeName === key ? 'border-white scale-110' : 'border-transparent hover:scale-110 opacity-70 hover:opacity-100'}`}
                                                style={{ backgroundColor: theme.hex }}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Language Picker */}
                            <div className="relative z-[200]">
                                <button 
                                    onClick={() => setIsLangMenuOpen(!isLangMenuOpen)} 
                                    className={`flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border ${activeTheme.borderLight} hover:bg-white/10 transition-all font-bold text-sm`}
                                >
                                    <Icon name="Globe" size={16} className={activeTheme.accent} /> {lang.toUpperCase()}
                                </button>
                                
                                {isLangMenuOpen && (
                                    <div className={`absolute top-10 ${lang === 'ar' ? 'left-0' : 'right-0'} glass-panel p-2 rounded-xl flex flex-col gap-1 shadow-2xl animate-view min-w-[100px]`}>
                                        <button onClick={() => {setLang('ar'); setIsLangMenuOpen(false);}} className={`px-4 py-2 rounded-lg text-sm font-bold text-dir hover:bg-white/10 ${lang === 'ar' ? activeTheme.accent : 'text-white'}`}>العربية</button>
                                        <button onClick={() => {setLang('en'); setIsLangMenuOpen(false);}} className={`px-4 py-2 rounded-lg text-sm font-bold text-dir hover:bg-white/10 ${lang === 'en' ? activeTheme.accent : 'text-white'}`}>English</button>
                                        <button onClick={() => {setLang('fr'); setIsLangMenuOpen(false);}} className={`px-4 py-2 rounded-lg text-sm font-bold text-dir hover:bg-white/10 ${lang === 'fr' ? activeTheme.accent : 'text-white'}`}>Français</button>
                                        <button onClick={() => {setLang('es'); setIsLangMenuOpen(false);}} className={`px-4 py-2 rounded-lg text-sm font-bold text-dir hover:bg-white/10 ${lang === 'es' ? activeTheme.accent : 'text-white'}`}>Español</button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="px-8 pb-4 text-dir">
                            <div className={`${activeTheme.btn} ${activeTheme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-lg`}>
                                <Icon name="Briefcase" size={28} />
                            </div>
                            <h1 className={`text-2xl font-black uppercase tracking-widest ${activeTheme.accent} mb-1`}>{t.dashboardTitle}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{t.dashboardSub}</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            <button onClick={() => setActiveTab('overview')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === 'overview' ? `bg-white/10 ${lang==='ar'?'border-r-4':'border-l-4'} ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="LayoutDashboard" size={20} /> {t.overview}
                            </button>
                            <button onClick={() => setActiveTab('products')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === 'products' ? `bg-white/10 ${lang==='ar'?'border-r-4':'border-l-4'} ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Package" size={20} /> {t.assets}
                            </button>
                            <button onClick={() => setActiveTab('team')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === 'team' ? `bg-white/10 ${lang==='ar'?'border-r-4':'border-l-4'} ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Users" size={20} /> {t.team}
                            </button>
                            <button onClick={() => setActiveTab('services')} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === 'services' ? `bg-white/10 ${lang==='ar'?'border-r-4':'border-l-4'} ${activeTheme.border} ${activeTheme.accent}` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}>
                                <Icon name="Zap" size={20} /> {t.services}
                            </button>
                        </div>
                        
                        <div className="hidden md:block p-6 mt-auto">
                            <div className="bg-white/5 p-5 rounded-3xl border border-white/5 text-center">
                                <Icon name="ShieldCheck" size={24} className={`${activeTheme.accent} mx-auto mb-2`} />
                                <span className="block text-xs font-black text-gray-400 uppercase">{t.certified}</span>
                                <span className={`block ${activeTheme.accent} font-bold text-sm mt-1`}>{t.gen}</span>
                            </div>
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Search & Wallet Bar */}
                        <div className="flex flex-col md:flex-row gap-6 mb-10 items-center">
                            <div className="flex-1 relative w-full">
                                <Icon name="Search" size={18} className={`absolute ${lang==='ar'?'right-5':'left-5'} top-1/2 -translate-y-1/2 text-gray-400`} />
                                <input 
                                    type="text" 
                                    placeholder={t.searchPlaceholder}
                                    className={`w-full premium-input rounded-2xl py-4 ${lang==='ar'?'pr-14 pl-6':'pl-14 pr-6'} text-sm font-bold text-dir`}
                                />
                            </div>
                            <div className={`glass-panel px-8 py-3 rounded-2xl border ${activeTheme.borderLight} flex items-center gap-4`}>
                                <div className="flex flex-col">
                                    <span className="text-[10px] text-gray-500 font-black uppercase tracking-widest">{t.liquidity}</span>
                                    <span className="text-[#00FF88] font-black text-xl">${LEADER_BALANCE_PLACEHOLDER.toLocaleString()}</span>
                                </div>
                                <Icon name="Wallet" size={24} className={activeTheme.accent} />
                            </div>
                        </div>

                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="flex items-center justify-between mb-8">
                                    <h2 className="text-3xl font-black">{t.kpiTitle}</h2>
                                </div>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute ${lang==='ar'?'-right-4':'-left-4'} -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="TrendingUp" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">{t.sales}</p>
                                        <h4 className="text-3xl font-black text-[#00FF88]">$1,036,000</h4>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute ${lang==='ar'?'-right-4':'-left-4'} -top-4 opacity-5 text-white group-hover:scale-110 transition-transform`}><Icon name="Package" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">{t.activeAssets}</p>
                                        <h4 className="text-3xl font-black text-white">{products.length}</h4>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute ${lang==='ar'?'-right-4':'-left-4'} -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="Eye" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">{t.views}</p>
                                        <h4 className="text-3xl font-black text-white">6,840</h4>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors`}>
                                        <div className={`absolute ${lang==='ar'?'-right-4':'-left-4'} -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="Users" size={120} /></div>
                                        <p className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-widest">{t.teamMembers}</p>
                                        <h4 className="text-3xl font-black text-white">{team.length}</h4>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'products' && (
                            <div className="animate-view space-y-8 max-w-4xl mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="PlusCircle" className={activeTheme.accent} size={32} /> {t.newProduct}
                                </h2>
                                
                                <form onSubmit={handleAddProduct} className={`${activeTheme.card} p-8 md:p-10 rounded-[3rem] border ${activeTheme.borderLight} shadow-2xl transition-colors`}>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                                        <div className="space-y-3">
                                            <input type="text" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border} text-dir`} value={newProd.name} onChange={e => setNewProd({...newProd, name: e.target.value})} placeholder="اسم الأصل..." />
                                        </div>
                                        <div className="space-y-3">
                                            <input type="number" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border} text-dir`} value={newProd.price} onChange={e => setNewProd({...newProd, price: e.target.value})} placeholder="السعر ($)" />
                                        </div>
                                        <div className="md:col-span-2 space-y-3">
                                            <textarea className={`w-full premium-input rounded-2xl py-4 px-5 font-bold min-h-[120px] focus:${activeTheme.border} text-dir`} value={newProd.desc} onChange={e => setNewProd({...newProd, desc: e.target.value})} placeholder="الوصف..."></textarea>
                                        </div>
                                    </div>
                                    <button type="submit" className={`w-full py-6 rounded-[2rem] font-black text-xl ${activeTheme.btn} ${activeTheme.btnText} btn-hover-dynamic flex items-center justify-center gap-3`}>
                                        <Icon name="UploadCloud" /> {t.addAsset}
                                    </button>
                                </form>
                            </div>
                        )}

                        {activeTab === 'services' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:border-[#00FF88] transition-colors`}>
                                        <div className="bg-[#00FF88]/10 text-[#00FF88] p-5 rounded-3xl mb-6"><Icon name="Bot" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">{t.aiAgent}</h4>
                                        <button className="mt-auto w-full py-4 bg-white/5 hover:bg-[#00FF88] hover:text-black rounded-xl font-black transition-all">تفعيل</button>
                                    </div>
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:${activeTheme.border} transition-colors`}>
                                        <div className={`bg-white/10 ${activeTheme.accent} p-5 rounded-3xl mb-6`}><Icon name="Megaphone" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">{t.regionalCamp}</h4>
                                        <button className={`mt-auto w-full py-4 bg-white/5 hover:${activeTheme.btn} hover:${activeTheme.btnText} rounded-xl font-black transition-all`}>تفعيل</button>
                                    </div>
                                    <div className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} text-center flex flex-col items-center hover:border-[#0074D9] transition-colors`}>
                                        <div className="bg-[#0074D9]/10 text-[#0074D9] p-5 rounded-3xl mb-6"><Icon name="FileSignature" size={40} /></div>
                                        <h4 className="text-xl font-black mb-3">{t.legalDoc}</h4>
                                        <button className="mt-auto w-full py-4 bg-white/5 hover:bg-[#0074D9] hover:text-white rounded-xl font-black transition-all">تفعيل</button>
                                    </div>
                                </div>
                            </div>
                        )}
                        
                        {activeTab === 'team' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="Users" className={activeTheme.accent} size={32} /> {t.teamMembers}
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {team.map(member => (
                                        <div key={member.id} className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} relative overflow-hidden transition-colors`}>
                                            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mb-4 text-2xl">👤</div>
                                            <h4 className="text-xl font-black mb-1">{member.name}</h4>
                                            <p className={`text-sm font-bold mb-6 ${activeTheme.accent}`}>{member.role}</p>
                                        </div>
                                    ))}
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
components.html(final_html, height=950, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
