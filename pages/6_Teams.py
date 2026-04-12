import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Elite Teams Command", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة ---
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
user_id = st.session_state.get('user_id', "COMMANDER-001")

# --- 3. واجهة React المتقدمة (مقر القيادة الميدانية السحري v4.0 - الصوت والاهتزاز) ---
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

        /* الجيمفيكيشن: أنيميشن نقاط الخبرة */
        .pulse-xp { animation: pulseXP 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        @keyframes pulseXP {
            0% { transform: scale(1); color: #00FF88; }
            50% { transform: scale(1.3); color: #FFD700; text-shadow: 0 0 20px rgba(255,215,0,0.8); }
            100% { transform: scale(1); color: #00FF88; }
        }

        /* Kanban Magic Styles */
        .kanban-col {
            background: rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 20px;
            min-height: 65vh;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .task-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        .task-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }

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
        <h2 style="margin-top:20px; font-weight: 900; letter-spacing: 2px;">MR7 TACTICAL COMMAND</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Audio & Haptic Feedback...</p>
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

        // --- نظام التنبيه الصوتي والاهتزاز (Audio & Haptics Engine) ---
        const triggerSensoryFeedback = (type) => {
            // 1. الاهتزاز (Haptic Feedback) إذا كان مدعوماً في المتصفح/الجهاز
            if (typeof navigator !== 'undefined' && navigator.vibrate) {
                if (type === 'success') {
                    navigator.vibrate([100, 50, 100]); // نبضتان للنجاح
                } else if (type === 'info') {
                    navigator.vibrate(50); // نبضة خفيفة للمعلومات
                } else {
                    navigator.vibrate([200]); // نبضة طويلة للتنبيهات الأخرى
                }
            }

            // 2. التنبيه الصوتي (Web Audio API)
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                const ctx = new AudioContext();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();

                osc.connect(gain);
                gain.connect(ctx.destination);

                if (type === 'success') {
                    // نغمة نجاح (تصاعدية)
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
                    osc.frequency.exponentialRampToValueAtTime(1046.50, ctx.currentTime + 0.1); // C6
                    gain.gain.setValueAtTime(0.1, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.15);
                } else {
                    // نغمة معلومات عادية (نبضة بسيطة)
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(440, ctx.currentTime); // A4
                    gain.gain.setValueAtTime(0.05, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.1);
                }
            } catch(e) {
                console.log("Audio feedback not supported or blocked by browser policy.", e);
            }
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
                ar: { title: "القيادة الميدانية", kanban: "المهام الاستراتيجية", meetings: "غرفة الاجتماعات", performance: "رادار الأداء", task: "المهمة", assignee: "القائد المُكلف", priority: "الأولوية", add_task: "إصدار تكليف", todo: "تكليفات جديدة", progress: "قيد التنفيذ", done: "مكتملة", high: "عاجلة 🔥", medium: "متوسطة", low: "عادية", xp_earned: "تم إضافة نقاط خبرة", notification: "إشعار نظام" },
                en: { title: "Field Command", kanban: "Strategic Tasks", meetings: "Meeting Room", performance: "Performance Radar", task: "Task", assignee: "Assignee", priority: "Priority", add_task: "Issue Command", todo: "New Tasks", progress: "In Progress", done: "Completed", high: "Urgent 🔥", medium: "Medium", low: "Normal", xp_earned: "XP Earned", notification: "System Notification" },
                // اللغات الأخرى يمكن إضافتها لاحقاً لتبسيط الكود هنا
            };

            const [lang, setLang] = useState('ar');
            const t = translations[lang] || translations['ar'];

            // --- States ---
            const [activeTab, setActiveTab] = useState('kanban');
            const [toasts, setToasts] = useState([]);
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            
            // --- نظام الجيمفيكيشن (Gamification State) ---
            const [xp, setXp] = useState(14500);
            const [xpAnim, setXpAnim] = useState(false);

            // --- Data States ---
            const [tasks, setTasks] = useState([
                { id: 1, title: 'إعداد حملة التسويق لمشروع النبت', assignee: 'أحمد المصري', status: 'todo', priority: 'high' },
                { id: 2, title: 'متابعة عملاء الجيل الثاني في الإقليم', assignee: 'صالح فهد', status: 'progress', priority: 'medium' },
                { id: 3, title: 'إغلاق 10 مبيعات لدبلوم الأرباح', assignee: 'سارة خالد', status: 'done', priority: 'high' }
            ]);

            const [meetings, setMeetings] = useState([
                { id: 1, title: 'الاجتماع الاستراتيجي الأسبوعي', date: 'غداً 08:00 PM', type: 'Zoom' },
                { id: 2, title: 'تدريب قادة الصف الأول', date: 'الخميس 05:00 PM', type: 'Google Meet' }
            ]);

            // --- Helper Functions ---
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                
                // تشغيل التأثيرات الحسية (صوت واهتزاز)
                triggerSensoryFeedback(type);

                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            const addXp = (amount) => {
                setXp(prev => prev + amount);
                setXpAnim(true);
                setTimeout(() => setXpAnim(false), 800); // إيقاف الأنيميشن
            };

            const simulateGlobalNotification = (msg) => {
                // يحاكي إرسال إشعار للنظام المركزي
                console.log("Global Notification Emitted: ", msg);
            };

            // --- Handlers ---
            const moveTask = (taskId, newStatus) => {
                setTasks(tasks.map(t => t.id === taskId ? { ...t, status: newStatus } : t));
                
                if (newStatus === 'done') {
                    const earnedXp = 50;
                    addXp(earnedXp);
                    showToast(lang === 'ar' ? `تم إنجاز المهمة بنجاح! مكافأة +${earnedXp} XP 🏆` : `Task Completed! +${earnedXp} XP 🏆`, 'success');
                    simulateGlobalNotification(`القائد أنجز مهمة استراتيجية وحصل على ${earnedXp} نقطة خبرة.`);
                } else {
                    showToast(lang === 'ar' ? 'تم تحريك مسار المهمة' : 'Task track updated', 'info');
                }
            };

            const handleAddTask = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                setTasks([{
                    id: Date.now(), title: f.get('title'), assignee: f.get('assignee'),
                    priority: f.get('priority'), status: 'todo'
                }, ...tasks]);
                
                const earnedXp = 15; // نقاط القيادة لإصدار التكليفات
                addXp(earnedXp);
                showToast(lang === 'ar' ? `تم إصدار التكليف للقيادة الميدانية! +${earnedXp} XP 🎯` : `Command issued! +${earnedXp} XP 🎯`, 'success');
                simulateGlobalNotification(`تم تكليف ${f.get('assignee')} بمهمة جديدة.`);
                
                e.target.reset();
            };

            const handleRewardLeader = (leaderName) => {
                const earnedXp = 100;
                addXp(earnedXp);
                showToast(lang === 'ar' ? `تم منح مكافأة تحفيزية للقائد ${leaderName}! إرث قيادي +${earnedXp} XP 🎁` : `Reward granted to ${leaderName}! +${earnedXp} XP 🎁`, 'success');
                simulateGlobalNotification(`القائد الأعلى أرسل مكافأة تحفيزية للقائد ${leaderName}.`);
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
                            <div className={`${theme.btn} ${theme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-xl`}><Icon name="Crosshair" size={30} /></div>
                            <h1 className={`text-xl font-black uppercase tracking-tighter ${theme.accent}`}>{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">Field Ops v4.0</p>
                            
                            {/* عداد الجيمفيكيشن (XP) */}
                            <div className="mt-6 bg-black/40 border border-white/10 rounded-xl p-4 flex justify-between items-center shadow-inner">
                                <div className="flex items-center gap-2">
                                    <Icon name="Zap" size={16} className="text-yellow-500" />
                                    <span className="text-[10px] text-gray-400 font-black uppercase tracking-widest">نقاط السيادة</span>
                                </div>
                                <span className={`text-[#00FF88] font-black text-xl ${xpAnim ? 'pulse-xp' : ''}`}>
                                    {xp.toLocaleString()} <span className="text-[10px]">XP</span>
                                </span>
                            </div>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'kanban', icon: 'KanbanSquare', label: t.kanban},
                                {id: 'meetings', icon: 'Video', label: t.meetings},
                                {id: 'performance', icon: 'TrendingUp', label: t.performance}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 ${isRTL ? 'border-r-4' : 'border-l-4'} ${theme.border} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab 1: Kanban Board */}
                        {activeTab === 'kanban' && (
                            <div className="animate-view space-y-8 max-w-[1600px] mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="KanbanSquare" className={theme.accent} size={32}/> {t.kanban}</h2>

                                {/* نموذج إضافة مهمة */}
                                <div className={`glass-panel p-8 rounded-[2.5rem] mb-10 border ${theme.borderLight}`}>
                                    <form onSubmit={handleAddTask} className="flex flex-col lg:flex-row gap-5 items-end">
                                        <div className="flex-1 w-full"><label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.task}</label><input name="title" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" placeholder="..."/></div>
                                        <div className="w-full lg:w-1/4"><label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.assignee}</label><input name="assignee" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" placeholder="..."/></div>
                                        <div className="w-full lg:w-1/6"><label className="text-[10px] uppercase font-black tracking-widest text-gray-500 mb-2 block">{t.priority}</label>
                                            <select name="priority" className="w-full premium-input p-4 rounded-xl font-bold text-sm bg-black">
                                                <option value="high">{t.high}</option><option value="medium">{t.medium}</option><option value="low">{t.low}</option>
                                            </select>
                                        </div>
                                        <button type="submit" className={`w-full lg:w-auto ${theme.btn} ${theme.btnText} px-10 py-4 rounded-xl font-black text-sm hover:scale-105 transition-transform shadow-xl`}>{t.add_task}</button>
                                    </form>
                                </div>

                                {/* أعمدة الكانبان */}
                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                    {/* Column: To Do */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-3 mb-6 border-b border-white/5 pb-4"><div className="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]"></div><h3 className="font-black text-xl">{t.todo}</h3><span className="bg-white/10 px-2.5 py-1 rounded-md text-[10px] font-black mr-auto">{tasks.filter(tk=>tk.status==='todo').length}</span></div>
                                        {tasks.filter(tk=>tk.status==='todo').map(task => (
                                            <div key={task.id} className="task-card border-t-2 border-t-red-500 hover:border-red-500">
                                                <div className="flex justify-between items-start mb-4"><span className={`text-[10px] font-black px-2 py-1 rounded-md ${task.priority==='high'?'bg-red-500/20 text-red-500':'bg-blue-500/20 text-blue-500'}`}>{t[task.priority]}</span></div>
                                                <h4 className="font-bold text-sm mb-6 leading-relaxed">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-4">
                                                    <span className="text-xs text-gray-400 font-bold flex items-center gap-1.5"><div className="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[8px]">👤</div> {task.assignee}</span>
                                                    <button onClick={()=>moveTask(task.id, 'progress')} className="text-yellow-500 hover:bg-yellow-500/10 p-2 rounded-lg transition-colors"><Icon name={isRTL ? "ArrowLeft" : "ArrowRight"} size={16}/></button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Column: In Progress */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-3 mb-6 border-b border-white/5 pb-4"><div className="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_10px_rgba(255,215,0,0.8)]"></div><h3 className="font-black text-xl">{t.progress}</h3><span className="bg-white/10 px-2.5 py-1 rounded-md text-[10px] font-black mr-auto">{tasks.filter(tk=>tk.status==='progress').length}</span></div>
                                        {tasks.filter(tk=>tk.status==='progress').map(task => (
                                            <div key={task.id} className="task-card border-t-2 border-t-yellow-500 hover:border-yellow-500">
                                                <div className="flex justify-between items-start mb-4"><span className={`text-[10px] font-black px-2 py-1 rounded-md ${task.priority==='high'?'bg-red-500/20 text-red-500':'bg-blue-500/20 text-blue-500'}`}>{t[task.priority]}</span></div>
                                                <h4 className="font-bold text-sm mb-6 leading-relaxed">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-4">
                                                    <button onClick={()=>moveTask(task.id, 'todo')} className="text-gray-500 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-colors"><Icon name={isRTL ? "ArrowRight" : "ArrowLeft"} size={16}/></button>
                                                    <span className="text-xs text-gray-400 font-bold flex items-center gap-1.5"><div className="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[8px]">👤</div> {task.assignee}</span>
                                                    <button onClick={()=>moveTask(task.id, 'done')} className="text-[#00FF88] hover:bg-[#00FF88]/10 p-2 rounded-lg transition-colors"><Icon name={isRTL ? "ArrowLeft" : "ArrowRight"} size={16}/></button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Column: Done */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-3 mb-6 border-b border-white/5 pb-4"><div className="w-3 h-3 rounded-full bg-[#00FF88] shadow-[0_0_10px_rgba(0,255,136,0.8)]"></div><h3 className="font-black text-xl">{t.done}</h3><span className="bg-white/10 px-2.5 py-1 rounded-md text-[10px] font-black mr-auto">{tasks.filter(tk=>tk.status==='done').length}</span></div>
                                        {tasks.filter(tk=>tk.status==='done').map(task => (
                                            <div key={task.id} className="task-card border-t-2 border-t-[#00FF88] opacity-60 hover:opacity-100 hover:border-[#00FF88] transition-all">
                                                <h4 className="font-bold text-sm mb-6 leading-relaxed line-through text-gray-400">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-4">
                                                    <button onClick={()=>moveTask(task.id, 'progress')} className="text-gray-500 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-colors"><Icon name={isRTL ? "ArrowRight" : "ArrowLeft"} size={16}/></button>
                                                    <span className="text-[10px] bg-[#00FF88]/10 text-[#00FF88] px-2 py-1 rounded-md font-black uppercase flex items-center gap-1"><Icon name="CheckCircle2" size={12}/> أنجزت</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab 2: Meetings */}
                        {activeTab === 'meetings' && (
                            <div className="animate-view space-y-8 max-w-5xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Video" className="text-blue-500" size={32}/> {t.meetings}</h2>
                                <div className={`glass-panel p-10 rounded-[3rem] border ${theme.borderLight}`}>
                                    <div className="flex justify-between items-center mb-10 border-b border-white/10 pb-6">
                                        <h3 className="text-2xl font-black">غرفة التخطيط الاستراتيجي</h3>
                                        <button onClick={()=>{showToast(lang === 'ar' ? 'تم نسخ الرابط وإرسال دعوة للفريق! +10 XP' : 'Link Copied & Invite Sent! +10 XP'); addXp(10);}} className="bg-white/10 px-6 py-3 rounded-xl font-bold text-sm hover:bg-white/20 transition-colors flex items-center gap-2"><Icon name="CalendarPlus" size={18}/> جدولة اجتماع</button>
                                    </div>
                                    <div className="space-y-4">
                                        {meetings.map(m => (
                                            <div key={m.id} className="flex flex-col md:flex-row justify-between items-center bg-black/40 p-6 rounded-2xl border border-white/5 hover:border-blue-500/50 transition-all group shadow-lg">
                                                <div className="flex items-center gap-5 mb-4 md:mb-0">
                                                    <div className="bg-blue-500/10 text-blue-500 p-4 rounded-2xl group-hover:scale-110 transition-transform"><Icon name="MonitorPlay" size={24}/></div>
                                                    <div>
                                                        <h4 className="font-black text-lg">{m.title}</h4>
                                                        <p className="text-sm text-gray-400 flex items-center gap-2 mt-1"><Icon name="Clock" size={14}/> {m.date} <span className="mx-2">•</span> {m.type}</p>
                                                    </div>
                                                </div>
                                                <button onClick={()=>showToast('Connecting to secure room...')} className="w-full md:w-auto bg-blue-600 text-white px-8 py-3.5 rounded-xl font-black hover:bg-blue-500 shadow-xl flex items-center justify-center gap-2 transition-all">
                                                    <Icon name="Video" size={18}/> دخول الغرفة
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab 3: Performance Radar */}
                        {activeTab === 'performance' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="TrendingUp" className="text-[#00FF88]" size={32}/> {t.performance}</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                    {[
                                        {name: 'أحمد المصري', sales: 12500, target: 15000, status: 'ممتاز'},
                                        {name: 'صالح فهد', sales: 8400, target: 10000, status: 'جيد'},
                                        {name: 'سارة خالد', sales: 2100, target: 10000, status: 'يحتاج دعم'}
                                    ].map((leader, i) => {
                                        const prog = (leader.sales / leader.target) * 100;
                                        const color = prog > 80 ? 'bg-[#00FF88]' : prog > 50 ? 'bg-yellow-500' : 'bg-red-500';
                                        return (
                                            <div key={i} className={`glass-panel p-8 rounded-[2.5rem] border-t-4 hover:-translate-y-2 transition-transform shadow-xl`} style={{borderTopColor: prog > 80 ? '#00FF88' : prog > 50 ? '#FFD700' : '#EF4444'}}>
                                                <div className="flex items-center gap-4 mb-6">
                                                    <div className="w-14 h-14 rounded-full bg-white/5 flex items-center justify-center text-2xl border border-white/10 shadow-inner">👤</div>
                                                    <div>
                                                        <h4 className="font-black text-lg">{leader.name}</h4>
                                                        <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{leader.status}</span>
                                                    </div>
                                                </div>
                                                <div className="w-full h-2.5 bg-black rounded-full overflow-hidden mb-4 border border-white/5">
                                                    <div className={`h-full ${color}`} style={{width: `${prog}%`}}></div>
                                                </div>
                                                <div className="flex justify-between text-xs font-bold mb-8">
                                                    <span className="text-gray-400">مبيعات: ${leader.sales.toLocaleString()}</span>
                                                    <span className="text-gray-500">الهدف: ${leader.target.toLocaleString()}</span>
                                                </div>
                                                <div className="flex gap-2">
                                                    <button onClick={()=>showToast('تم إرسال برقية دعم عبر مركز الاتصالات', 'info')} className="flex-1 py-3 bg-white/5 border border-white/10 hover:border-white/30 rounded-xl text-xs font-black transition-all flex justify-center items-center gap-2"><Icon name="MessageSquare" size={14}/> تواصل</button>
                                                    <button onClick={()=>handleRewardLeader(leader.name)} className="flex-1 py-3 bg-yellow-500/10 text-yellow-500 border border-yellow-500/30 hover:bg-yellow-500 hover:text-black rounded-xl text-xs font-black transition-all flex justify-center items-center gap-2"><Icon name="Gift" size={14}/> مكافأة</button>
                                                </div>
                                            </div>
                                        )
                                    })}
                                </div>
                            </div>
                        )}

                    </div>

                    {/* Toasts Container */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'info' ? 'bg-black/90 border-blue-500/40 text-blue-500' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : t.type === 'info' ? 'Info' : 'AlertCircle'} size={20} />
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

# --- 6. أزرار العودة ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
