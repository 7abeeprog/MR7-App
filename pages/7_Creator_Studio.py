import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Creator Studio", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة ---
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
user_id = st.session_state.get('user_id', "COMMANDER-001")

# --- 3. واجهة React المتقدمة (استوديو المبدعين السيادي v7.0 - المناهج والعمولات) ---
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
            box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
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

        /* الجيمفيكيشن: أنيميشن العملات الذهبية */
        .coin-bounce { animation: coinBounceAnim 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: inline-block; }
        @keyframes coinBounceAnim {
            0% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-15px) scale(1.3); color: #FFD700; text-shadow: 0 0 30px #FFD700; }
            100% { transform: translateY(0) scale(1); }
        }

        /* شريط رحلة الـ 100 يوم */
        .journey-bar-bg { width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 10px; overflow: hidden; margin-top: 10px; }
        .journey-bar-fill { height: 100%; background: linear-gradient(90deg, #FFD700, #00FF88); transition: width 1s ease-in-out; }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }

        #loading-screen {
            position: fixed; inset: 0; background: #000; color: #FFD700; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999;
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; font-weight: 900; letter-spacing: 2px;">MR7 CREATOR STUDIO</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Knowledge Engine & Affiliate Systems...</p>
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

        // --- نظام التنبيه الصوتي والاهتزاز (Audio & Haptics) ---
        const triggerSensoryFeedback = (type) => {
            if (typeof navigator !== 'undefined' && navigator.vibrate) {
                if (type === 'coin') navigator.vibrate([50, 50, 50]); 
                else if (type === 'success') navigator.vibrate([100, 50, 100]); 
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

                if (type === 'coin') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(987.77, ctx.currentTime); 
                    osc.frequency.setValueAtTime(1318.51, ctx.currentTime + 0.08); 
                    gain.gain.setValueAtTime(0.15, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.3);
                } else if (type === 'success') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); 
                    osc.frequency.exponentialRampToValueAtTime(1046.50, ctx.currentTime + 0.1); 
                    gain.gain.setValueAtTime(0.1, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.15);
                }
            } catch(e) { console.log("Audio blocked.", e); }
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
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text:-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };

            const [activeThemeName, setActiveThemeName] = useState("أسود قيادي 🖤");
            const theme = themes[activeThemeName] || themes["أسود قيادي 🖤"];

            // --- 2. اللغات السبعة (7 Languages) ---
            const translations = {
                ar: { title: "استوديو المبدعين", builder: "بناء المنهج", quizzes: "بنك الاختبارات", badges: "الأوسمة", earnings: "الأرباح", publish: "نشر الدورة", add_course: "هندسة دورة جديدة", course_name: "اسم المنهج", price: "القيمة الاستثمارية ($)", desc: "الوصف الاستراتيجي", img_url: "رابط صورة الغلاف (URL)" },
                en: { title: "Creator Studio", builder: "Course Builder", quizzes: "Quiz Bank", badges: "Badges", earnings: "Earnings", publish: "Publish Course", add_course: "Engineer New Course", course_name: "Course Title", price: "Investment Value ($)", desc: "Strategic Description", img_url: "Cover Image URL" },
                // ... (باقي اللغات تتبع نفس النمط)
            };

            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // --- States ---
            const [activeTab, setActiveTab] = useState('builder');
            const [toasts, setToasts] = useState([]);
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            
            // --- نظام الجيمفيكيشن والعملات (Coins & XP) ---
            const [coins, setCoins] = useState(2450);
            const [coinAnim, setCoinAnim] = useState(false);

            // --- Data States (المناهج والأقسام والدروس) ---
            const [courses, setCourses] = useState([
                { 
                    id: 1, 
                    name: 'أسرار المليار دولار', 
                    price: 499, 
                    desc: 'دورة هندسة الأرباح وبناء الجيوش التسويقية.', 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800',
                    commRates: [10, 5, 2, 1, 1, 1, 1, 1, 1, 1], // نظام الإحالة
                    modules: [
                        { id: 101, title: 'الأساسيات القيادية', lessons: [{id: 1001, title: 'مقدمة في السيادة', type: 'video'}] }
                    ]
                }
            ]);
            const [quizzes, setQuizzes] = useState([
                { id: 1, question: 'ما هو قانون الـ 10؟', course: 'أسرار المليار دولار' }
            ]);

            // --- Curriculum Manager State ---
            const [managingCourseId, setManagingCourseId] = useState(null);

            // --- Helper Functions ---
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                triggerSensoryFeedback(type);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            const addCoins = (amount) => {
                setCoins(prev => prev + amount);
                setCoinAnim(true);
                setTimeout(() => setCoinAnim(false), 800); 
            };

            // --- Handlers ---
            const handleAddCourse = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                
                // استخراج نظام العمولة (الإحالة)
                const affiliateRates = Array.from({length: 10}).map((_, i) => parseFloat(f.get(`c${i+1}`) || 0));

                setCourses([{
                    id: Date.now(), 
                    name: f.get('name'), 
                    price: parseFloat(f.get('price')), 
                    desc: f.get('desc'),
                    img: f.get('img') || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800',
                    commRates: affiliateRates,
                    modules: []
                }, ...courses]);
                
                const earnedCoins = 100;
                addCoins(earnedCoins);
                showToast(lang === 'ar' ? `تم طرح المنهج مع نظام الإحالة! +${earnedCoins} 🪙` : `Course Published! +${earnedCoins} 🪙`, 'coin');
                e.target.reset();
            };

            // --- Curriculum Handlers ---
            const handleAddModule = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                const title = f.get('title');
                
                setCourses(courses.map(c => c.id === managingCourseId ? {
                    ...c, modules: [...(c.modules || []), { id: Date.now(), title, lessons: [] }]
                } : c));
                
                addCoins(20);
                showToast(lang === 'ar' ? 'تم بناء قسم جديد! +20🪙' : 'Module Added! +20🪙', 'coin');
                e.target.reset();
            };

            const handleAddLesson = (e, moduleId) => {
                e.preventDefault();
                const f = new FormData(e.target);
                const title = f.get('title');
                const type = f.get('type'); // video or text
                
                setCourses(courses.map(c => {
                    if (c.id === managingCourseId) {
                        return {
                            ...c,
                            modules: c.modules.map(m => m.id === moduleId ? {
                                ...m, lessons: [...(m.lessons || []), { id: Date.now(), title, type }]
                            } : m)
                        };
                    }
                    return c;
                }));
                
                addCoins(10);
                showToast(lang === 'ar' ? 'تم إضافة درس! +10🪙' : 'Lesson Added! +10🪙', 'coin');
                e.target.reset();
            };

            const handleAddQuiz = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                setQuizzes([{
                    id: Date.now(), question: f.get('question'), course: f.get('course')
                }, ...quizzes]);
                
                const earnedCoins = 25;
                addCoins(earnedCoins);
                showToast(lang === 'ar' ? `تم إضافة اختبار ذكي! +${earnedCoins} 🪙` : `Quiz Added! +${earnedCoins} 🪙`, 'coin');
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

                        <div className="p-8 pb-4">
                            <div className={`${theme.btn} ${theme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-xl`}><Icon name="PenTool" size={30} /></div>
                            <h1 className={`text-xl font-black uppercase tracking-tighter ${theme.accent}`}>{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Creator Engine</p>
                            
                            {/* رحلة الـ 100 يوم */}
                            <div className="mt-8 mb-2">
                                <div className="flex justify-between items-end mb-1">
                                    <span className="text-[10px] text-gray-400 font-bold uppercase">رحلة الـ 100 يوم للسيادة</span>
                                    <span className="text-xs font-black text-[#00FF88]">اليوم 40</span>
                                </div>
                                <div className="journey-bar-bg">
                                    <div className="journey-bar-fill" style={{width: '40%'}}></div>
                                </div>
                            </div>

                            {/* عداد العملات السيادية (Coins) */}
                            <div className="mt-6 bg-black/40 border border-white/10 rounded-xl p-4 flex justify-between items-center shadow-inner">
                                <div className="flex items-center gap-2">
                                    <span className="text-xl">🪙</span>
                                    <span className="text-[10px] text-gray-400 font-black uppercase tracking-widest">عملات المبدع</span>
                                </div>
                                <span className={`text-[#FFD700] font-black text-xl flex items-center gap-1 ${coinAnim ? 'coin-bounce' : ''}`}>
                                    {coins.toLocaleString()}
                                </span>
                            </div>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'builder', icon: 'LayoutTemplate', label: t.builder},
                                {id: 'quizzes', icon: 'HelpCircle', label: t.quizzes},
                                {id: 'badges', icon: 'Award', label: t.badges},
                                {id: 'earnings', icon: 'TrendingUp', label: t.earnings}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => {setActiveTab(btn.id); setManagingCourseId(null);}} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 ${isRTL ? 'border-r-4' : 'border-l-4'} ${theme.border} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab 1: Course Builder & Curriculum Manager */}
                        {activeTab === 'builder' && (
                            <div className="animate-view space-y-8 max-w-[1600px] mx-auto pt-5">
                                
                                {/* إذا كنا في وضع "إدارة المنهج" لدورة معينة */}
                                {managingCourseId ? (() => {
                                    const mCourse = courses.find(c => c.id === managingCourseId);
                                    return (
                                        <div className="animate-view">
                                            <div className="flex items-center gap-4 mb-8">
                                                <button onClick={() => setManagingCourseId(null)} className="p-3 bg-white/5 hover:bg-white/10 rounded-xl transition-colors">
                                                    <Icon name={isRTL ? "ArrowRight" : "ArrowLeft"} size={24}/>
                                                </button>
                                                <div>
                                                    <h2 className="text-3xl font-black">{mCourse.name}</h2>
                                                    <p className="text-sm text-gray-500">إدارة الأقسام والدروس</p>
                                                </div>
                                            </div>

                                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                                {/* الأقسام (Modules) */}
                                                <div className="lg:col-span-2 space-y-6">
                                                    {(mCourse.modules || []).map((mod, idx) => (
                                                        <div key={mod.id} className={`glass-panel p-6 rounded-[2rem] border ${theme.borderLight}`}>
                                                            <div className="flex justify-between items-center mb-4 pb-4 border-b border-white/5">
                                                                <h3 className="text-xl font-black flex items-center gap-3"><span className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm">{idx+1}</span> {mod.title}</h3>
                                                            </div>
                                                            <div className="space-y-3 mb-6">
                                                                {(mod.lessons || []).length === 0 ? <p className="text-xs text-gray-500 italic">لا توجد دروس في هذا القسم.</p> : 
                                                                    mod.lessons.map((lesson, lIdx) => (
                                                                        <div key={lesson.id} className="flex items-center gap-3 bg-black/40 p-4 rounded-xl border border-white/5 hover:border-yellow-500/30 transition-colors">
                                                                            <Icon name={lesson.type === 'video' ? 'PlayCircle' : 'FileText'} size={18} className={lesson.type === 'video' ? 'text-blue-400' : 'text-green-400'} />
                                                                            <span className="font-bold text-sm flex-1">{lesson.title}</span>
                                                                        </div>
                                                                    ))
                                                                }
                                                            </div>
                                                            {/* نموذج إضافة درس للقسم */}
                                                            <form onSubmit={(e) => handleAddLesson(e, mod.id)} className="flex gap-2">
                                                                <input name="title" required placeholder="عنوان الدرس الجديد..." className="flex-1 premium-input p-3 rounded-xl text-xs font-bold" />
                                                                <select name="type" className="premium-input p-3 rounded-xl text-xs font-bold bg-black"><option value="video">🎥 فيديو</option><option value="text">📄 نص/مقال</option></select>
                                                                <button type="submit" className={`${theme.btn} ${theme.btnText} px-4 rounded-xl text-xs font-black`}><Icon name="Plus" size={16}/></button>
                                                            </form>
                                                        </div>
                                                    ))}
                                                    
                                                    {/* نموذج إضافة قسم جديد */}
                                                    <div className={`glass-panel p-6 rounded-[2rem] border border-dashed ${theme.borderLight} bg-transparent`}>
                                                        <form onSubmit={handleAddModule} className="flex flex-col gap-4">
                                                            <label className="text-xs font-black text-gray-400 uppercase">إضافة قسم جديد (Module)</label>
                                                            <div className="flex gap-4">
                                                                <input name="title" required placeholder="مثال: الفصل الأول - العقلية" className="flex-1 premium-input p-4 rounded-xl font-bold text-sm" />
                                                                <button type="submit" className={`${theme.btn} ${theme.btnText} px-8 rounded-xl font-black shadow-lg`}>إضافة</button>
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>

                                                {/* معلومات الدورة والأفيليت */}
                                                <div className="space-y-6">
                                                    <div className={`glass-panel p-6 rounded-[2rem] border ${theme.borderLight}`}>
                                                        <img src={mCourse.img} className="w-full h-40 object-cover rounded-xl mb-4" />
                                                        <h4 className="font-black text-lg mb-2">{mCourse.name}</h4>
                                                        <p className="text-xs text-gray-400 mb-4">{mCourse.desc}</p>
                                                        <div className="bg-yellow-500/10 p-4 rounded-xl border border-yellow-500/20 text-center mb-4">
                                                            <span className="block text-[10px] uppercase text-yellow-500 font-black mb-1">القيمة</span>
                                                            <span className="text-2xl font-black text-yellow-500">${mCourse.price}</span>
                                                        </div>
                                                        <div className="border-t border-white/5 pt-4">
                                                            <span className="block text-[10px] uppercase text-gray-400 font-black mb-2">خارطة نظام الإحالة (10 مستويات)</span>
                                                            <div className="flex flex-wrap gap-1">
                                                                {(mCourse.commRates || []).map((rate, i) => (
                                                                    <div key={i} className="bg-white/5 px-2 py-1 rounded text-[10px] font-bold"><span className="opacity-50">ج{i+1}:</span> <span className="text-[#00FF88]">{rate}%</span></div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })() : (
                                    /* الوضع العادي: إضافة المناهج وعرضها */
                                    <>
                                        <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="LayoutTemplate" className={theme.accent} size={32}/> {t.builder}</h2>
                                        <div className="flex flex-col lg:flex-row gap-8">
                                            {/* Form */}
                                            <div className={`glass-panel p-8 rounded-[2.5rem] flex-1 border ${theme.borderLight} h-fit`}>
                                                <h3 className="text-xl font-black mb-6">{t.add_course}</h3>
                                                <form onSubmit={handleAddCourse} className="space-y-5">
                                                    <div>
                                                        <label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.course_name}</label>
                                                        <input name="name" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" placeholder="..."/>
                                                    </div>
                                                    <div className="grid grid-cols-2 gap-3">
                                                        <div>
                                                            <label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.price}</label>
                                                            <input name="price" type="number" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" placeholder="..."/>
                                                        </div>
                                                        <div>
                                                            <label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.img_url}</label>
                                                            <input name="img" className="w-full premium-input p-4 rounded-xl font-bold text-sm" placeholder="https://..."/>
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.desc}</label>
                                                        <textarea name="desc" required className="w-full premium-input p-4 rounded-xl font-bold text-sm min-h-[80px]" placeholder="..."></textarea>
                                                    </div>
                                                    
                                                    {/* نظام الإحالة (Affiliate System) */}
                                                    <div className="p-5 bg-white/5 rounded-2xl border border-white/10 mt-4">
                                                        <div className="flex items-center gap-2 mb-4">
                                                            <Icon name="Network" className="text-[#00FF88]" size={20} />
                                                            <label className="text-xs uppercase font-black tracking-widest text-[#00FF88] block">نظام الإحالة والعمولات الممتد (Affiliate)</label>
                                                        </div>
                                                        <p className="text-[10px] text-gray-400 mb-4 font-bold">حدد نسبة العمولة لكل مستوى من المستويات العشرة لمسوقي هذا المنهج.</p>
                                                        <div className="grid grid-cols-5 gap-3">
                                                            {Array.from({length: 10}).map((_, i) => (
                                                                <div key={i} className="flex flex-col">
                                                                    <span className="text-[9px] text-center text-gray-500 font-black mb-1">جيل {i+1}</span>
                                                                    <input name={`c${i+1}`} type="number" defaultValue={i===0?10:i===1?5:1} className="premium-input p-2 rounded-lg text-center text-xs font-bold" />
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>

                                                    <button type="submit" className={`w-full mt-4 ${theme.btn} ${theme.btnText} py-4 rounded-xl font-black text-lg hover:scale-105 transition-transform shadow-xl`}>{t.publish} 🚀</button>
                                                </form>
                                            </div>

                                            {/* Course List */}
                                            <div className="flex-1 space-y-5">
                                                <h3 className="text-xl font-black mb-6">المناهج المعتمدة في السحابة</h3>
                                                {courses.map(course => (
                                                    <div key={course.id} className={`glass-panel p-6 rounded-[2rem] border-r-4 ${theme.borderLight} hover:border-yellow-500 transition-colors flex gap-5`}>
                                                        <img src={course.img} className="w-28 h-28 rounded-xl object-cover border border-white/10 shadow-lg" />
                                                        <div className="flex-1 flex flex-col justify-center">
                                                            <div className="flex justify-between items-start mb-1">
                                                                <h4 className="font-black text-xl">{course.name}</h4>
                                                                <span className="text-[#00FF88] font-black text-lg">${course.price}</span>
                                                            </div>
                                                            <p className="text-xs text-gray-400 mb-3 line-clamp-1">{course.desc}</p>
                                                            <div className="flex gap-3 mt-auto">
                                                                <button onClick={() => setManagingCourseId(course.id)} className="bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500 hover:text-black px-5 py-2.5 rounded-xl text-xs font-black transition-all flex items-center gap-2"><Icon name="LayoutGrid" size={14}/> بناء المحتوى {(course.modules || []).length} قسم</button>
                                                                <button onClick={()=>{setCourses(courses.filter(c=>c.id!==course.id)); showToast('تم الأرشفة');}} className="bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white px-4 py-2.5 rounded-xl text-xs font-bold transition-all"><Icon name="Trash2" size={14}/></button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </>
                                )}
                            </div>
                        )}

                        {/* Tab 2: Quizzes */}
                        {activeTab === 'quizzes' && (
                            <div className="animate-view space-y-8 max-w-5xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="HelpCircle" className="text-blue-500" size={32}/> {t.quizzes}</h2>
                                <div className={`glass-panel p-10 rounded-[3rem] border ${theme.borderLight}`}>
                                    <h3 className="text-xl font-black mb-6">تصميم مقاييس الجدارة</h3>
                                    <form onSubmit={handleAddQuiz} className="space-y-4 mb-10">
                                        <input name="question" required placeholder="نص السؤال الاستراتيجي..." className="w-full premium-input p-4 rounded-xl font-bold text-sm"/>
                                        <select name="course" className="w-full premium-input p-4 rounded-xl font-bold text-sm bg-black">
                                            {courses.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
                                        </select>
                                        <div className="grid grid-cols-2 gap-4">
                                            <input placeholder="الخيار الصحيح..." className="w-full premium-input p-4 rounded-xl font-bold text-sm border-green-500/50"/>
                                            <input placeholder="الخيار الخاطئ..." className="w-full premium-input p-4 rounded-xl font-bold text-sm border-red-500/50"/>
                                        </div>
                                        <button type="submit" className="bg-blue-600 text-white w-full py-4 rounded-xl font-black hover:bg-blue-500 transition-all">إضافة للسجل المعرفي 📥</button>
                                    </form>

                                    <h3 className="text-lg font-black mb-4 border-t border-white/10 pt-6">بنك الأسئلة المعتمد</h3>
                                    {quizzes.map(q => (
                                        <div key={q.id} className="bg-black/40 p-4 rounded-2xl mb-2 border border-white/5">
                                            <span className="text-[10px] text-yellow-500 font-black uppercase">{q.course}</span>
                                            <h4 className="font-bold text-sm mt-1">{q.question}</h4>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab 3: Badges */}
                        {activeTab === 'badges' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Award" className="text-purple-500" size={32}/> {t.badges}</h2>
                                <p className="text-gray-400">حدد الأوسمة التي تمنح لطلابك لتعزيز التحفيز (Gamification).</p>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    {[
                                        {icon: '🏅', name: 'المنطلق السريع', desc: 'يمنح عند إتمام أول وحدة في 24 ساعة'},
                                        {icon: '🧠', name: 'العقل الذهبي', desc: 'يمنح عند تخطي الاختبار بنسبة 100%'},
                                        {icon: '🏆', name: 'القائد المطبق', desc: 'يمنح عند رفع المشروع النهائي'}
                                    ].map((badge, i) => (
                                        <div key={i} className={`glass-panel p-8 rounded-[2.5rem] text-center border hover:border-purple-500 transition-all`}>
                                            <div className="text-6xl mb-4">{badge.icon}</div>
                                            <h4 className="text-xl font-black mb-2 text-white">{badge.name}</h4>
                                            <p className="text-sm text-gray-400 mb-6">{badge.desc}</p>
                                            <button onClick={()=>{showToast('تم تفعيل الوسام في المنهج', 'info'); addCoins(5);}} className="w-full py-2.5 bg-white/5 hover:bg-purple-500 hover:text-white rounded-xl font-black text-xs transition-colors">تفعيل الوسام ✅</button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab 4: Earnings */}
                        {activeTab === 'earnings' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="TrendingUp" className="text-[#00FF88]" size={32}/> {t.earnings}</h2>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500">
                                        <small className="text-gray-500 font-bold uppercase">إجمالي العوائد الصافية</small>
                                        <h4 className="text-3xl font-black text-green-500">$45,200</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">الطلاب المسجلين</small>
                                        <h4 className="text-3xl font-black text-blue-500">1,248</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">التقييم العالمي</small>
                                        <h4 className="text-3xl font-black text-yellow-500 flex items-center gap-2">4.9 <Icon name="Star" fill="currentColor" size={24}/></h4>
                                    </div>
                                </div>
                                <div className={`glass-panel p-8 rounded-[3rem] border ${theme.borderLight}`}>
                                    <h3 className="text-xl font-black mb-6">الانتشار الجغرافي للمحتوى</h3>
                                    <div className="space-y-4">
                                        <div>
                                            <div className="flex justify-between text-sm font-bold mb-1"><span>مصر</span><span>55%</span></div>
                                            <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden"><div className="h-full bg-yellow-500 w-[55%]"></div></div>
                                        </div>
                                        <div>
                                            <div className="flex justify-between text-sm font-bold mb-1"><span>السعودية</span><span>25%</span></div>
                                            <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden"><div className="h-full bg-green-500 w-[25%]"></div></div>
                                        </div>
                                        <div>
                                            <div className="flex justify-between text-sm font-bold mb-1"><span>ليبيا</span><span>15%</span></div>
                                            <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden"><div className="h-full bg-blue-500 w-[15%]"></div></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                    </div>

                    {/* Toasts Container */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'coin' ? 'bg-black/90 border-yellow-500/50 text-yellow-500' : t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'info' ? 'bg-black/90 border-blue-500/40 text-blue-500' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'coin' ? 'Star' : t.type === 'success' ? 'CheckCircle2' : t.type === 'info' ? 'Info' : 'AlertCircle'} size={20} />
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

# --- 6. أزرار العودة والتنقل الاستراتيجي لرحلة العميل ---
st.markdown("---")
st.markdown("### 🗺️ خريطة السيادة السريعة (رحلة الـ 100 يوم)")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🛒 المتجر العالمي (نشر وتسويق)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("👥 إدارة الفرق (تدريب الأجيال)"):
        st.switch_page("pages/6_Teams.py")
with c3:
    if st.button("🏠 العودة لمركز القيادة الرئيسي"):
        st.switch_page("app.py")
