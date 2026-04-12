import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 GOD MODE - Admin Panel", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة ---
current_theme = st.session_state.get('app_theme', "سلطة مطلقة 🔴")
user_id = st.session_state.get('user_id', "MR7-ROOT-001")

# --- 3. واجهة React المتقدمة (لوحة التحكم العليا السيادية v9.0 - محرك الحقن السحابي) ---
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
        ::-webkit-scrollbar-thumb:hover { background: #FF4B4B; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: inherit;
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.3);
            outline: none;
            border-color: #FF4B4B;
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

        .review-card {
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border-right: 4px solid #FF4B4B;
        }
        .review-card:hover { transform: translateX(-5px); box-shadow: 0 10px 30px rgba(255, 75, 75, 0.1); }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }
        html[dir="ltr"] .review-card { border-right: none; border-left: 4px solid #FF4B4B; }
        html[dir="ltr"] .review-card:hover { transform: translateX(5px); }

        /* Scanning Animation */
        .scan-line {
            position: absolute;
            width: 100%;
            height: 4px;
            background: #00FF88;
            box-shadow: 0 0 20px #00FF88;
            animation: scan 2s linear infinite;
            z-index: 10;
        }
        @keyframes scan {
            0% { top: 0; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }

        #loading-screen {
            position: fixed; inset: 0; background: #000; color: #FF4B4B; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999;
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,75,75,0.3); border-top: 4px solid #FF4B4B; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; font-weight: 900; letter-spacing: 2px;">MR7 GOD MODE</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Global Command & Data Injector...</p>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        const Icon = ({ name, size = 24, className = "" }) => {
            const iconRef = useRef(null);
            useEffect(() => {
                if (iconRef.current && window.lucide) {
                    iconRef.current.innerHTML = ''; 
                    const i = document.createElement('i');
                    i.setAttribute('data-lucide', name);
                    if (className) i.setAttribute('class', className);
                    iconRef.current.appendChild(i);
                    window.lucide.createIcons({ root: iconRef.current });
                }
            }, [name, size, className]);
            return <span ref={iconRef} className={`inline-flex justify-center items-center ${className}`}></span>;
        };

        // --- نظام التنبيه الصوتي والاهتزاز السيادي (Admin Haptics) ---
        const triggerAdminFeedback = (type) => {
            if (typeof navigator !== 'undefined' && navigator.vibrate) {
                if (type === 'approve' || type === 'success') navigator.vibrate([100, 50, 100]); 
                else if (type === 'reject') navigator.vibrate([200, 100, 200]); 
                else if (type === 'scan') navigator.vibrate([30, 30, 30, 30, 30]); 
                else navigator.vibrate(50); 
            }

            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                const ctx = new AudioContext();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();

                osc.connect(gain);
                gain.connect(ctx.destination);

                if (type === 'approve' || type === 'success') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); 
                    osc.frequency.exponentialRampToValueAtTime(1046.50, ctx.currentTime + 0.15); 
                    gain.gain.setValueAtTime(0.15, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.2);
                } else if (type === 'scan') {
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(800, ctx.currentTime); 
                    gain.gain.setValueAtTime(0.05, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.1);
                } else if (type === 'reject') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, ctx.currentTime); 
                    osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.3); 
                    gain.gain.setValueAtTime(0.15, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.3);
                }
            } catch(e) { console.log("Audio blocked.", e); }
        };

        const App = () => {
            // --- 1. الأنماط السبعة ---
            const themes = {
                "سلطة مطلقة 🔴": { bg: "bg-[#0A0000]", text: "text-[#FFFFFF]", card: "bg-[#140000]/90", border: "border-[#FF4B4B]", borderLight: "border-[#FF4B4B]/20", accent: "text-[#FF4B4B]", btn: "bg-[#FF4B4B]", btnText: "text-white", hex: "#FF4B4B" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", borderLight: "border-[#B8860B]/20", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#FFFFFF" },
                "أصفر الريادة 🟡": { bg: "bg-[#141400]", text: "text-white", card: "bg-[#2B2B00]/80", border: "border-[#FFDC00]", borderLight: "border-[#FFDC00]/20", accent: "text-[#FFDC00]", btn: "bg-[#FFDC00]", btnText: "text-black", hex: "#FFDC00" },
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text:-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };

            const [activeThemeName, setActiveThemeName] = useState("سلطة مطلقة 🔴");
            const theme = themes[activeThemeName] || themes["سلطة مطلقة 🔴"];

            // --- 2. اللغات السبعة ---
            const translations = {
                ar: { title: "غرفة التحكم العليا", radar: "الرادار العالمي", projects: "اعتماد المشاريع", courses: "تدقيق المناهج", injector: "محرك الحقن السحابي", dictionary: "قاموس السيادة", approve: "اعتماد", reject: "رفض" },
                en: { title: "God Mode Control", radar: "Global Radar", projects: "Project Approvals", courses: "Course Audits", injector: "Cloud Data Injector", dictionary: "Sovereign Dictionary", approve: "Approve", reject: "Reject" },
                fr: { title: "Contrôle Suprême", radar: "Radar Global", projects: "Projets", courses: "Cours", injector: "Injecteur Cloud", dictionary: "Dictionnaire", approve: "Approuver", reject: "Rejeter" },
                es: { title: "Control Supremo", radar: "Radar Global", projects: "Proyectos", courses: "Cursos", injector: "Inyector Cloud", dictionary: "Diccionario", approve: "Aprobar", reject: "Rechazar" },
                zh: { title: "最高控制室", radar: "全球雷达", projects: "项目审批", courses: "课程审核", injector: "云数据注入器", dictionary: "主权字典", approve: "批准", reject: "拒绝" },
                fa: { title: "کنترل عالی", radar: "رادار جهانی", projects: "تایید پروژه‌ها", courses: "ممیزی دوره‌ها", injector: "تزریق داده‌های ابری", dictionary: "فرهنگ لغت", approve: "تایید", reject: "رد کردن" },
                sw: { title: "Udhibiti Mkuu", radar: "Rada ya Dunia", projects: "Miradi", courses: "Kozi", injector: "Kichomezi cha Wingu", dictionary: "Kamusi", approve: "Idhinisha", reject: "Kataa" }
            };

            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // --- States ---
            const [activeTab, setActiveTab] = useState('injector'); // جعل الحقن هو الافتراضي للتجربة
            const [toasts, setToasts] = useState([]);
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            
            // --- Data States ---
            const [pendingProjects, setPendingProjects] = useState([
                { id: 'proj1', title: 'مدينة النبت الخضراء', owner: 'القائد ياسين', amount: 5000000, region: 'مصر', status: 'pending' }
            ]);

            // --- Data Injector States ---
            const [injectStatus, setInjectStatus] = useState('idle'); // idle, scanning, extracted, injected
            const [extractedPhases, setExtractedPhases] = useState([]);

            // مصفوفة تعكس محتوى الـ PDF للـ 100 برنامج مقسمة لرحلة الـ 100 يوم
            const pdfDataMap = [
                { phase: 1, days: "1-10", title: "القيادة والإدارة الاستراتيجية", count: 10, icon: "Crown", color: "#FFD700", sample: "القيادة التحويلية، التفكير الاستراتيجي، إدارة الأزمات" },
                { phase: 2, days: "11-20", title: "الاستثمار والمالية", count: 10, icon: "TrendingUp", color: "#00FF88", sample: "أساسيات الاستثمار، تحليل الأسهم، التمويل الجماعي" },
                { phase: 3, days: "21-30", title: "ريادة الأعمال وتطوير الأعمال", count: 10, icon: "Rocket", color: "#FF4B4B", sample: "نموذج العمل، التسويق الرقمي، العلامة التجارية" },
                { phase: 4, days: "31-40", title: "التكنولوجيا والتحول الرقمي", count: 10, icon: "Cpu", color: "#0074D9", sample: "الذكاء الاصطناعي، الأمن السيبراني، الحوسبة السحابية" },
                { phase: 5, days: "41-50", title: "المهارات الشخصية والمهنية", count: 10, icon: "Users", color: "#B10DC9", sample: "التواصل الفعال، الذكاء العاطفي، حل المشكلات" },
                { phase: 6, days: "51-60", title: "التخطيط المالي الشخصي", count: 10, icon: "Wallet", color: "#2ECC40", sample: "بناء مستقبل مالي، إدارة الثروات، الاستقلال المالي" },
                { phase: 7, days: "61-70", title: "المهارات القانونية والتنظيمية", count: 10, icon: "Scale", color: "#FF851B", sample: "القانون التجاري، حوكمة الشركات، الملكية الفكرية" },
                { phase: 8, days: "71-80", title: "التنمية المستدامة (CSR)", count: 10, icon: "Leaf", color: "#3D9970", sample: "التنمية المستدامة، الاقتصاد الدائري، الطاقة المتجددة" },
                { phase: 9, days: "81-90", title: "المهارات المتقدمة والمتخصصة", count: 10, icon: "BrainCircuit", color: "#F012BE", sample: "تحليل البيانات، التعلم العميق، تطوير التطبيقات" },
                { phase: 10, days: "91-100", title: "قطاعات MR7 المتخصصة", count: 10, icon: "Globe", color: "#7FDBFF", sample: "الزراعة الذكية، النقل الذكي، النقل اللوجستي، المجتمعات" }
            ];

            const handleScanPDF = () => {
                setInjectStatus('scanning');
                triggerAdminFeedback('scan');
                
                // محاكاة عملية قراءة وتحليل الـ PDF
                setTimeout(() => {
                    setExtractedPhases(pdfDataMap);
                    setInjectStatus('extracted');
                    triggerAdminFeedback('success');
                    showToast('تم استخراج 100 برنامج تدريبي وتصنيفها في 10 مراحل بنجاح.', 'success');
                }, 2500);
            };

            const handleInjectToCloud = () => {
                setInjectStatus('injecting');
                
                // محاكاة الرفع لقواعد البيانات
                setTimeout(() => {
                    setInjectStatus('injected');
                    triggerAdminFeedback('approve');
                    showToast('تم بث الـ 100 برنامج بنجاح! رحلة الـ 100 يوم جاهزة للمستخدمين.', 'success');
                }, 3000);
            };

            // --- Dictionary State ---
            const [dictionary, setDictionary] = useState({
                empire: 'الإمبراطورية',
                leader: 'قائد استراتيجي',
                army: 'جيش المسوقين',
                asset: 'أصل سيادي'
            });

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            const handleDictionarySave = (e) => {
                e.preventDefault();
                triggerAdminFeedback('approve');
                showToast(lang === 'ar' ? 'تم تحديث مصطلحات المنظومة عالمياً 🌍' : 'Global terminology updated 🌍', 'success');
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
                        
                        {/* Theme & Lang Controls */}
                        <div className="p-6 pb-2 flex justify-between items-center">
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

                        <div className="p-8 pb-4 text-center md:text-start">
                            <div className={`${theme.btn} ${theme.btnText} p-4 rounded-2xl inline-block mb-4 shadow-[0_0_30px_rgba(255,75,75,0.4)]`}><Icon name="ShieldAlert" size={32} /></div>
                            <h1 className={`text-2xl font-black uppercase tracking-tighter ${theme.accent}`}>{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Root Access Granted</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'radar', icon: 'Activity', label: t.radar},
                                {id: 'injector', icon: 'DatabaseZap', label: t.injector, badge: 'جديد'}, // Tab الحقن الجديد
                                {id: 'projects', icon: 'FolderKanban', label: t.projects, badge: pendingProjects.length},
                                {id: 'dictionary', icon: 'BookA', label: t.dictionary}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center justify-between px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 ${isRTL ? 'border-r-4' : 'border-l-4'} ${theme.border} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
                                    <div className="flex items-center gap-4">
                                        <Icon name={btn.icon} size={18} /> {btn.label}
                                    </div>
                                    {btn.badge && <span className={`bg-red-500 text-white text-[10px] px-2 py-0.5 rounded-full font-black ${btn.badge === 'جديد' ? 'animate-bounce' : ''}`}>{btn.badge}</span>}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* --- Tab: Data Injector (محرك الحقن السحابي) --- */}
                        {activeTab === 'injector' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-5">
                                <div className="flex justify-between items-center mb-8">
                                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="DatabaseZap" className={theme.accent} size={32}/> هندسة وحقن المناهج (رحلة 100 يوم)</h2>
                                    {injectStatus === 'injected' && <span className="bg-[#00FF88]/20 text-[#00FF88] px-4 py-2 rounded-xl text-sm font-black flex items-center gap-2"><Icon name="CheckCircle2" size={18}/> السحابة متزامنة 100%</span>}
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                    {/* لوحة تحكم الـ PDF */}
                                    <div className={`glass-panel p-8 rounded-[2.5rem] border ${theme.borderLight} flex flex-col items-center justify-center text-center h-fit sticky top-5`}>
                                        <div className="w-24 h-24 bg-white/5 rounded-3xl flex items-center justify-center mb-6 relative overflow-hidden border border-white/10">
                                            {injectStatus === 'scanning' && <div className="scan-line"></div>}
                                            <Icon name="FileText" size={40} className={injectStatus === 'extracted' || injectStatus === 'injected' ? 'text-[#00FF88]' : 'text-gray-400'} />
                                        </div>
                                        <h3 className="text-xl font-black mb-2">Comprehensive_Training_Package.pdf</h3>
                                        <p className="text-sm text-gray-500 mb-8 font-bold">يحتوي الملف على 10 فئات و 100 برنامج تدريبي مفصل لإعداد القادة والمستثمرين.</p>

                                        {injectStatus === 'idle' && (
                                            <button onClick={handleScanPDF} className={`w-full py-4 ${theme.btn} ${theme.btnText} rounded-xl font-black text-lg shadow-[0_10px_30px_rgba(255,75,75,0.3)] flex justify-center items-center gap-2 hover:scale-105 transition-transform`}>
                                                <Icon name="ScanLine" size={20}/> بدء تحليل المستند الذكي
                                            </button>
                                        )}

                                        {injectStatus === 'scanning' && (
                                            <div className="w-full text-center">
                                                <p className="text-yellow-500 font-black mb-3 animate-pulse">جاري استخراج البيانات والمحاور...</p>
                                                <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden"><div className="h-full bg-yellow-500 w-1/2 animate-pulse"></div></div>
                                            </div>
                                        )}

                                        {injectStatus === 'extracted' && (
                                            <button onClick={handleInjectToCloud} className="w-full py-4 bg-[#00FF88] text-black rounded-xl font-black text-lg shadow-[0_10px_30px_rgba(0,255,136,0.3)] flex justify-center items-center gap-2 hover:scale-105 transition-transform">
                                                <Icon name="CloudUpload" size={20}/> بث البرامج للسحابة (Firebase)
                                            </button>
                                        )}

                                        {injectStatus === 'injected' && (
                                            <div className="w-full p-4 bg-[#00FF88]/10 border border-[#00FF88]/30 rounded-xl text-[#00FF88]">
                                                <Icon name="CheckCircle2" size={30} className="mx-auto mb-2" />
                                                <p className="font-black text-sm">تم حقن 100 برنامج بنجاح!</p>
                                                <p className="text-[10px] text-white mt-2">المناهج متاحة الآن في الأكاديمية.</p>
                                            </div>
                                        )}
                                    </div>

                                    {/* عرض نتائج التحليل (الـ 10 مراحل) */}
                                    <div className="lg:col-span-2 space-y-6">
                                        <div className="flex justify-between items-center mb-2">
                                            <h3 className="text-2xl font-black">خارطة حقن رحلة الـ 100 يوم</h3>
                                            <span className="text-gray-500 text-sm font-bold">{extractedPhases.length} مراحل / 100 برنامج</span>
                                        </div>

                                        {extractedPhases.length === 0 ? (
                                            <div className="glass-panel p-10 rounded-[2.5rem] border border-dashed border-gray-700 text-center opacity-40">
                                                <Icon name="Database" size={50} className="mx-auto mb-4" />
                                                <p className="text-xl font-black">في انتظار التحليل لفك تشفير البرامج وبناء الخارطة...</p>
                                            </div>
                                        ) : (
                                            extractedPhases.map((phase, i) => (
                                                <div key={i} className="glass-panel p-6 rounded-[2rem] flex items-center gap-6 animate-view border border-white/5" style={{animationDelay: `${i * 0.1}s`, borderRight: `4px solid ${phase.color}`}}>
                                                    <div className="w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg" style={{backgroundColor: `${phase.color}20`, color: phase.color}}>
                                                        <Icon name={phase.icon} size={28} />
                                                    </div>
                                                    <div className="flex-1">
                                                        <div className="flex justify-between items-start mb-1">
                                                            <h4 className="text-xl font-black">{phase.title}</h4>
                                                            <span className="text-xs font-black uppercase tracking-widest bg-white/10 px-3 py-1 rounded-lg" style={{color: phase.color}}>أيام {phase.days}</span>
                                                        </div>
                                                        <p className="text-sm text-gray-400 font-bold mb-2">تتضمن {phase.count} برامج تدريبية مفصلة (بواقع برنامج لكل يوم).</p>
                                                        <div className="flex items-center gap-2 text-[10px] text-gray-500 bg-black/40 p-2 rounded-lg border border-white/5">
                                                            <Icon name="BookOpen" size={12} />
                                                            <span>مثال من المحتوى: {phase.sample}...</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Global Radar */}
                        {activeTab === 'radar' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="Activity" className={theme.accent} size={32}/> {t.radar}</h2>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className={`glass-panel p-6 rounded-[2rem] border-t-4 border-[#00FF88] shadow-xl`}>
                                        <small className="text-gray-500 font-bold uppercase">السيولة الإجمالية</small>
                                        <h4 className="text-3xl font-black text-[#00FF88]">$6.4B</h4>
                                    </div>
                                    <div className={`glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500`}>
                                        <small className="text-gray-500 font-bold uppercase">إجمالي المسجلين</small>
                                        <h4 className="text-3xl font-black text-blue-500">1.2M</h4>
                                    </div>
                                    <div className={`glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500`}>
                                        <small className="text-gray-500 font-bold uppercase">معدل التضاعف</small>
                                        <h4 className="text-3xl font-black text-yellow-500">14% 📈</h4>
                                    </div>
                                    <div className={`glass-panel p-6 rounded-[2rem] border-t-4 border-red-500`}>
                                        <small className="text-gray-500 font-bold uppercase">مشاريع معلقة</small>
                                        <h4 className="text-3xl font-black text-red-500">{pendingProjects.length}</h4>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Dynamic Dictionary (Sovereign Terminology) */}
                        {activeTab === 'dictionary' && (
                            <div className="animate-view space-y-8 max-w-4xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-4"><Icon name="BookA" className={theme.accent} size={32}/> {t.dictionary}</h2>
                                <p className="text-gray-400 mb-8 leading-relaxed">قم بتكييف مصطلحات المنظومة لتناسب الفئة المستهدفة (مثال: الهيئات الدبلوماسية، الأمم المتحدة، أو الشركات الكبرى). التغيير هنا ينعكس على واجهات المستخدمين فوراً.</p>
                                
                                <div className={`glass-panel p-10 rounded-[3rem] border ${theme.borderLight}`}>
                                    <form onSubmit={handleDictionarySave} className="space-y-6">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: الإمبراطورية</label>
                                                <input name="empire" defaultValue={dictionary.empire} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: قائد</label>
                                                <input name="leader" defaultValue={dictionary.leader} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: جيش</label>
                                                <input name="army" defaultValue={dictionary.army} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: أصل سيادي</label>
                                                <input name="asset" defaultValue={dictionary.asset} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                            </div>
                                        </div>
                                        
                                        <div className="pt-8 mt-4 border-t border-white/10">
                                            <button type="submit" className={`w-full ${theme.btn} ${theme.btnText} py-5 rounded-2xl font-black text-xl hover:scale-[1.02] transition-transform shadow-[0_10px_30px_rgba(255,75,75,0.3)] flex justify-center items-center gap-3`}>
                                                <Icon name="GlobeLock" size={24}/> توثيق المسميات الدبلوماسية
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        )}

                    </div>

                    {/* Toasts Container */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'error' ? 'bg-black/90 border-red-500/40 text-red-500' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : t.type === 'error' ? 'XCircle' : 'AlertCircle'} size={20} />
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

# --- 4. حقن المتغيرات السحابية ---
final_html = react_html.replace("CURRENT_THEME_PLACEHOLDER", current_theme)

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=950, scrolling=True)

# --- 6. أزرار العودة والتنقل الاستراتيجي ---
st.markdown("---")
st.markdown("### 🗺️ مسارات التحكم السريعة لرحلة الـ 100 يوم")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎓 الأكاديمية (رؤية المناهج بعد الحقن)"):
        st.switch_page("pages/1_Education.py")
with c2:
    if st.button("🛒 المتجر العالمي (واجهة المستخدم)"):
        st.switch_page("pages/4_Marketplace.py")
with c3:
    if st.button("🏠 العودة لمركز القيادة (Root)"):
        st.switch_page("app.py")
