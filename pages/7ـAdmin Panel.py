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
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
user_id = st.session_state.get('user_id', "MR7-ROOT-001")

# --- 3. واجهة React المتقدمة (لوحة التحكم العليا السيادية v8.0) ---
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
        ::-webkit-scrollbar-thumb:hover { background: #FF4B4B; } /* لون أحمر مميز للأدمن */
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
            box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.3); /* توهج أحمر للأدمن */
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

        /* حركات بطاقات المراجعة */
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
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Global Command & Control...</p>
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
                if (type === 'approve') navigator.vibrate([100, 50, 100]); 
                else if (type === 'reject') navigator.vibrate([200, 100, 200]); 
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

                if (type === 'approve') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); 
                    osc.frequency.exponentialRampToValueAtTime(1046.50, ctx.currentTime + 0.15); 
                    gain.gain.setValueAtTime(0.15, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.2);
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
            // --- 1. الأنماط السبعة (بلكنة الأدمن - أحمر/ذهبي) ---
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
                ar: { title: "غرفة التحكم العليا", radar: "الرادار العالمي", projects: "اعتماد المشاريع", courses: "تدقيق المناهج", users: "هويات القادة", dictionary: "قاموس السيادة", approve: "اعتماد", reject: "رفض" },
                en: { title: "God Mode Control", radar: "Global Radar", projects: "Project Approvals", courses: "Course Audits", users: "Leader Identities", dictionary: "Sovereign Dictionary", approve: "Approve", reject: "Reject" },
                fr: { title: "Contrôle Suprême", radar: "Radar Global", projects: "Projets", courses: "Cours", users: "Identités", dictionary: "Dictionnaire", approve: "Approuver", reject: "Rejeter" },
                es: { title: "Control Supremo", radar: "Radar Global", projects: "Proyectos", courses: "Cursos", users: "Identidades", dictionary: "Diccionario", approve: "Aprobar", reject: "Rechazar" },
                zh: { title: "最高控制室", radar: "全球雷达", projects: "项目审批", courses: "课程审核", users: "领导者身份", dictionary: "主权字典", approve: "批准", reject: "拒绝" },
                fa: { title: "کنترل عالی", radar: "رادار جهانی", projects: "تایید پروژه‌ها", courses: "ممیزی دوره‌ها", users: "هویت رهبران", dictionary: "فرهنگ لغت", approve: "تایید", reject: "رد کردن" },
                sw: { title: "Udhibiti Mkuu", radar: "Rada ya Dunia", projects: "Miradi", courses: "Kozi", users: "Vitambulisho", dictionary: "Kamusi", approve: "Idhinisha", reject: "Kataa" }
            };

            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // --- States ---
            const [activeTab, setActiveTab] = useState('radar');
            const [toasts, setToasts] = useState([]);
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            
            // --- Data States (Mocked for MVP) ---
            const [pendingProjects, setPendingProjects] = useState([
                { id: 'proj1', title: 'مدينة النبت الخضراء', owner: 'القائد ياسين', amount: 5000000, region: 'مصر', status: 'pending' },
                { id: 'proj2', title: 'أسطول النقل الذكي', owner: 'صالح فهد', amount: 1200000, region: 'ليبيا', status: 'pending' }
            ]);

            const [pendingCourses, setPendingCourses] = useState([
                { id: 'c1', title: 'القيادة في الأزمات', author: 'سارة خالد', price: 299, status: 'pending' }
            ]);

            // --- Dictionary State (محرك المسميات الديناميكي) ---
            const [dictionary, setDictionary] = useState({
                empire: 'الإمبراطورية',
                leader: 'قائد استراتيجي',
                army: 'جيش المسوقين',
                asset: 'أصل سيادي'
            });

            // --- Helper Functions ---
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // --- Handlers ---
            const handleProjectDecision = (id, decision) => {
                triggerAdminFeedback(decision === 'approve' ? 'approve' : 'reject');
                setPendingProjects(pendingProjects.filter(p => p.id !== id));
                showToast(lang === 'ar' ? (decision === 'approve' ? 'تم اعتماد المشروع وبثه للعامة' : 'تم رفض المشروع') : `Project ${decision}d`, decision === 'approve' ? 'success' : 'error');
            };

            const handleCourseDecision = (id, decision) => {
                triggerAdminFeedback(decision === 'approve' ? 'approve' : 'reject');
                setPendingCourses(pendingCourses.filter(c => c.id !== id));
                showToast(lang === 'ar' ? (decision === 'approve' ? 'تم اعتماد المنهج وطرحه في المتجر' : 'تم تجميد المنهج') : `Course ${decision}d`, decision === 'approve' ? 'success' : 'error');
            };

            const handleDictionarySave = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                setDictionary({
                    empire: f.get('empire'),
                    leader: f.get('leader'),
                    army: f.get('army'),
                    asset: f.get('asset')
                });
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
                                {id: 'projects', icon: 'FolderKanban', label: t.projects, badge: pendingProjects.length},
                                {id: 'courses', icon: 'GraduationCap', label: t.courses, badge: pendingCourses.length},
                                {id: 'users', icon: 'Users', label: t.users},
                                {id: 'dictionary', icon: 'BookA', label: t.dictionary}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center justify-between px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 ${isRTL ? 'border-r-4' : 'border-l-4'} ${theme.border} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
                                    <div className="flex items-center gap-4">
                                        <Icon name={btn.icon} size={18} /> {btn.label}
                                    </div>
                                    {btn.badge > 0 && <span className={`bg-red-500 text-white text-[10px] px-2 py-0.5 rounded-full font-black animate-pulse`}>{btn.badge}</span>}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab 1: Global Radar */}
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
                                        <small className="text-gray-500 font-bold uppercase">مهام معلقة</small>
                                        <h4 className="text-3xl font-black text-red-500">{pendingProjects.length + pendingCourses.length}</h4>
                                    </div>
                                </div>
                                
                                <div className={`glass-panel p-10 rounded-[3rem] mt-10 border ${theme.borderLight}`}>
                                    <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="BrainCircuit" className={theme.accent} /> رؤية الذكاء الاصطناعي (MR7-AI)</h3>
                                    <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
                                        <p className="text-lg leading-relaxed text-gray-300">
                                            "بناءً على التحديث الأخير لـ <b>{dictionary.empire}</b>، هناك زيادة ملحوظة في تسجيل <b>{dictionary.leader}</b> في إقليم شمال إفريقيا. نقترح تسريع اعتماد <b>{dictionary.asset}</b> الخاص بالبنية التحتية لدعم هذا التوسع."
                                        </p>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab 2: Project Approvals */}
                        {activeTab === 'projects' && (
                            <div className="animate-view space-y-8 max-w-5xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="FolderKanban" className={theme.accent} size={32}/> {t.projects}</h2>
                                {pendingProjects.length === 0 ? (
                                    <div className="text-center py-20 opacity-30"><Icon name="CheckCircle2" size={60} className="mx-auto mb-4"/><h3 className="text-2xl font-black">لا توجد مشاريع معلقة</h3></div>
                                ) : (
                                    <div className="space-y-6">
                                        {pendingProjects.map(proj => (
                                            <div key={proj.id} className={`glass-panel p-8 rounded-[2.5rem] review-card bg-black/40`}>
                                                <div className="flex justify-between items-start mb-6">
                                                    <div>
                                                        <span className="bg-white/10 px-3 py-1 rounded-md text-[10px] font-black tracking-widest uppercase mb-3 inline-block">📍 {proj.region}</span>
                                                        <h3 className="text-2xl font-black mb-1">{proj.title}</h3>
                                                        <p className="text-sm text-gray-500 font-bold">بواسطة: {proj.owner}</p>
                                                    </div>
                                                    <div className="text-left">
                                                        <span className="text-[10px] text-gray-500 uppercase font-black block">الميزانية المطلوبة</span>
                                                        <span className="text-3xl font-black text-[#00FF88]">${proj.amount.toLocaleString()}</span>
                                                    </div>
                                                </div>
                                                <div className="flex gap-4 border-t border-white/5 pt-6">
                                                    <button onClick={() => handleProjectDecision(proj.id, 'approve')} className="flex-1 bg-[#00FF88] text-black py-4 rounded-xl font-black text-sm hover:brightness-110 transition-all flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(0,255,136,0.3)]"><Icon name="Check" size={18}/> اعتماد وطرح للتمويل</button>
                                                    <button onClick={() => handleProjectDecision(proj.id, 'reject')} className="flex-1 bg-white/5 border border-red-500/50 text-red-500 py-4 rounded-xl font-black text-sm hover:bg-red-500 hover:text-white transition-all flex justify-center items-center gap-2"><Icon name="X" size={18}/> رفض وإعادة</button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Tab 3: Course Audits */}
                        {activeTab === 'courses' && (
                            <div className="animate-view space-y-8 max-w-5xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="GraduationCap" className={theme.accent} size={32}/> {t.courses}</h2>
                                {pendingCourses.length === 0 ? (
                                    <div className="text-center py-20 opacity-30"><Icon name="CheckCircle2" size={60} className="mx-auto mb-4"/><h3 className="text-2xl font-black">لا توجد مناهج معلقة</h3></div>
                                ) : (
                                    <div className="space-y-6">
                                        {pendingCourses.map(course => (
                                            <div key={course.id} className={`glass-panel p-8 rounded-[2.5rem] review-card bg-black/40 border-l-4 border-l-[#0074D9]`} style={{borderRight: 'none'}}>
                                                <div className="flex justify-between items-start mb-6">
                                                    <div>
                                                        <h3 className="text-2xl font-black mb-1">{course.title}</h3>
                                                        <p className="text-sm text-gray-500 font-bold">إعداد: {course.author}</p>
                                                    </div>
                                                    <div className="text-left">
                                                        <span className="text-[10px] text-gray-500 uppercase font-black block">السعر</span>
                                                        <span className="text-3xl font-black text-yellow-500">${course.price}</span>
                                                    </div>
                                                </div>
                                                <div className="flex gap-4 border-t border-white/5 pt-6">
                                                    <button onClick={() => handleCourseDecision(course.id, 'approve')} className="flex-1 bg-[#0074D9] text-white py-4 rounded-xl font-black text-sm hover:brightness-110 transition-all flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(0,116,217,0.3)]"><Icon name="Check" size={18}/> اعتماد المنهج</button>
                                                    <button onClick={() => handleCourseDecision(course.id, 'reject')} className="flex-1 bg-white/5 border border-red-500/50 text-red-500 py-4 rounded-xl font-black text-sm hover:bg-red-500 hover:text-white transition-all flex justify-center items-center gap-2"><Icon name="X" size={18}/> تجميد</button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Tab 4: Dynamic Dictionary (Sovereign Terminology) */}
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
                                                <p className="text-[10px] text-gray-600">بدائل مقترحة: المنظمة، المؤسسة، الشبكة</p>
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: قائد</label>
                                                <input name="leader" defaultValue={dictionary.leader} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                                <p className="text-[10px] text-gray-600">بدائل مقترحة: سفير، مندوب تنفيذي، شريك</p>
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: جيش</label>
                                                <input name="army" defaultValue={dictionary.army} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                                <p className="text-[10px] text-gray-600">بدائل مقترحة: فريق تنفيذي، شبكة اتصالات</p>
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-gray-500 uppercase tracking-widest block">المصطلح الأساسي: أصل سيادي</label>
                                                <input name="asset" defaultValue={dictionary.asset} className="w-full premium-input p-4 rounded-xl font-black text-lg" />
                                                <p className="text-[10px] text-gray-600">بدائل مقترحة: برنامج تنفيذي، مشروع تنموي</p>
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

# --- 6. أزرار العودة السريعة ---
st.markdown("---")
st.markdown("### 🗺️ مسارات التحكم السريعة")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🛒 المتجر العالمي (واجهة المستخدم)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("👥 إدارة الفرق"):
        st.switch_page("pages/6_Teams.py")
with c3:
    if st.button("🏠 العودة لمركز القيادة (Root)"):
        st.switch_page("app.py")
