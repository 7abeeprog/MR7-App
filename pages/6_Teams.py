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

# --- 3. واجهة React المتقدمة (مقر القيادة الميدانية - Kanban & Meetings) ---
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
            background-color: #030303;
            color: #ffffff;
            overflow-x: hidden;
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
            background: rgba(15, 15, 15, 0.8);
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: white;
            transition: all 0.3s ease;
        }
        .premium-input:focus { border-color: #FFD700; outline: none; }

        /* Kanban Specific Styles */
        .kanban-col {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 20px;
            min-height: 60vh;
        }
        
        .task-card {
            background: #111;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 15px;
            transition: 0.3s;
            cursor: grab;
        }
        .task-card:hover { border-color: #FFD700; transform: translateY(-3px); }

        .animate-view { animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

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
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px;">جاري نشر مقر القيادة الميدانية...</h2>
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

        const App = () => {
            const [activeTab, setActiveTab] = useState('kanban');
            const [toasts, setToasts] = useState([]);

            // --- Theme Setup ---
            const themes = {
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#FFFFFF" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" }
            };
            const [activeThemeName, setActiveThemeName] = useState("CURRENT_THEME_PLACEHOLDER" || "أسود قيادي 🖤");
            const theme = themes[activeThemeName] || themes["أسود قيادي 🖤"];

            // --- Data States ---
            const [tasks, setTasks] = useState([
                { id: 1, title: 'إعداد حملة التسويق لمشروع النبت', assignee: 'أحمد المصري', status: 'todo', priority: 'high' },
                { id: 2, title: 'متابعة عملاء الجيل الثاني في ليبيا', assignee: 'صالح فهد', status: 'progress', priority: 'medium' },
                { id: 3, title: 'إغلاق 10 مبيعات لدبلوم الأرباح', assignee: 'سارة خالد', status: 'done', priority: 'high' }
            ]);

            const [meetings, setMeetings] = useState([
                { id: 1, title: 'الاجتماع الاستراتيجي الأسبوعي', date: 'غداً 08:00 PM', type: 'Zoom', link: '#' },
                { id: 2, title: 'تدريب قادة الصف الأول', date: 'الخميس 05:00 PM', type: 'Google Meet', link: '#' }
            ]);

            const showToast = (msg) => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- Handlers ---
            const moveTask = (taskId, newStatus) => {
                setTasks(tasks.map(t => t.id === taskId ? { ...t, status: newStatus } : t));
                showToast('تم تحديث مسار المهمة بنجاح');
            };

            const handleAddTask = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                setTasks([...tasks, {
                    id: Date.now(), title: f.get('title'), assignee: f.get('assignee'),
                    priority: f.get('priority'), status: 'todo'
                }]);
                showToast('تم إصدار التكليف الجديد للقائد');
                e.target.reset();
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col md:flex-row overflow-hidden`}>
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${theme.card} border-b md:border-b-0 md:border-l ${theme.border} border-opacity-20 flex flex-col z-10`}>
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-[0_0_20px_rgba(255,215,0,0.3)]"><Icon name="Crosshair" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">مقر القيادة الميدانية</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">Field Ops v1.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'kanban', icon: 'KanbanSquare', label: 'المهام الاستراتيجية'},
                                {id: 'meetings', icon: 'Video', label: 'غرفة الاجتماعات'},
                                {id: 'performance', icon: 'TrendingUp', label: 'رادار أداء القادة'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar">
                        
                        {/* Tab 1: Kanban Board */}
                        {activeTab === 'kanban' && (
                            <div className="animate-view space-y-8">
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="KanbanSquare" className="text-yellow-500" size={32}/> لوحة التكليفات (Kanban)</h2>
                                </div>

                                {/* نموذج إضافة مهمة */}
                                <div className="glass-panel p-6 rounded-[2rem] mb-8">
                                    <form onSubmit={handleAddTask} className="flex flex-col md:flex-row gap-4 items-end">
                                        <div className="flex-1 w-full"><label className="text-xs text-gray-500 font-bold mb-2 block">المهمة</label><input name="title" required className="w-full premium-input p-3 rounded-xl" placeholder="ما هي المهمة؟"/></div>
                                        <div className="w-full md:w-1/4"><label className="text-xs text-gray-500 font-bold mb-2 block">القائد المُكلف</label><input name="assignee" required className="w-full premium-input p-3 rounded-xl" placeholder="اسم القائد..."/></div>
                                        <div className="w-full md:w-1/6"><label className="text-xs text-gray-500 font-bold mb-2 block">الأولوية</label><select name="priority" className="w-full premium-input p-3 rounded-xl bg-black"><option value="high">عاجلة 🔥</option><option value="medium">متوسطة</option><option value="low">عادية</option></select></div>
                                        <button type="submit" className="w-full md:w-auto bg-yellow-500 text-black px-8 py-3.5 rounded-xl font-black hover:scale-105 transition-transform">إصدار التكليف</button>
                                    </form>
                                </div>

                                {/* أعمدة الكانبان */}
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    {/* Column: To Do */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4"><div className="w-3 h-3 rounded-full bg-red-500"></div><h3 className="font-black text-lg">تكليفات جديدة</h3><span className="bg-white/10 px-2 py-0.5 rounded-md text-xs mr-auto">{tasks.filter(t=>t.status==='todo').length}</span></div>
                                        {tasks.filter(t=>t.status==='todo').map(task => (
                                            <div key={task.id} className="task-card border-l-4 border-l-red-500">
                                                <div className="flex justify-between items-start mb-3"><span className={`text-[10px] font-black px-2 py-1 rounded-md ${task.priority==='high'?'bg-red-500/20 text-red-500':'bg-blue-500/20 text-blue-500'}`}>{task.priority}</span></div>
                                                <h4 className="font-bold mb-4">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-3">
                                                    <span className="text-xs text-gray-400 font-bold"><Icon name="User" size={12}/> {task.assignee}</span>
                                                    <button onClick={()=>moveTask(task.id, 'progress')} className="text-yellow-500 hover:bg-yellow-500/10 p-1.5 rounded-lg transition-colors"><Icon name="ArrowLeft" size={16}/></button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Column: In Progress */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4"><div className="w-3 h-3 rounded-full bg-yellow-500"></div><h3 className="font-black text-lg">قيد التنفيذ</h3><span className="bg-white/10 px-2 py-0.5 rounded-md text-xs mr-auto">{tasks.filter(t=>t.status==='progress').length}</span></div>
                                        {tasks.filter(t=>t.status==='progress').map(task => (
                                            <div key={task.id} className="task-card border-l-4 border-l-yellow-500">
                                                <div className="flex justify-between items-start mb-3"><span className={`text-[10px] font-black px-2 py-1 rounded-md ${task.priority==='high'?'bg-red-500/20 text-red-500':'bg-blue-500/20 text-blue-500'}`}>{task.priority}</span></div>
                                                <h4 className="font-bold mb-4">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-3">
                                                    <button onClick={()=>moveTask(task.id, 'todo')} className="text-gray-500 hover:text-white p-1.5"><Icon name="ArrowRight" size={16}/></button>
                                                    <span className="text-xs text-gray-400 font-bold"><Icon name="User" size={12}/> {task.assignee}</span>
                                                    <button onClick={()=>moveTask(task.id, 'done')} className="text-[#00FF88] hover:bg-[#00FF88]/10 p-1.5 rounded-lg transition-colors"><Icon name="ArrowLeft" size={16}/></button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Column: Done */}
                                    <div className="kanban-col">
                                        <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4"><div className="w-3 h-3 rounded-full bg-[#00FF88]"></div><h3 className="font-black text-lg">مكتملة</h3><span className="bg-white/10 px-2 py-0.5 rounded-md text-xs mr-auto">{tasks.filter(t=>t.status==='done').length}</span></div>
                                        {tasks.filter(t=>t.status==='done').map(task => (
                                            <div key={task.id} className="task-card border-l-4 border-l-[#00FF88] opacity-70">
                                                <h4 className="font-bold mb-4 line-through text-gray-400">{task.title}</h4>
                                                <div className="flex justify-between items-center border-t border-white/5 pt-3">
                                                    <button onClick={()=>moveTask(task.id, 'progress')} className="text-gray-500 hover:text-white p-1.5"><Icon name="ArrowRight" size={16}/></button>
                                                    <span className="text-xs text-[#00FF88] font-bold"><Icon name="CheckCircle2" size={14}/> أنجزت</span>
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
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Video" className="text-blue-500" size={32}/> مركز التخطيط والاجتماعات</h2>
                                <div className="glass-panel p-8 rounded-[2.5rem]">
                                    <div className="flex justify-between items-center mb-8">
                                        <h3 className="text-xl font-black">الاجتماعات القادمة</h3>
                                        <button onClick={()=>showToast('سيتم ربط تقويم جوجل قريباً')} className="bg-white/10 px-6 py-2 rounded-xl font-bold text-sm hover:bg-white/20">+ جدولة اجتماع</button>
                                    </div>
                                    <div className="space-y-4">
                                        {meetings.map(m => (
                                            <div key={m.id} className="flex flex-col md:flex-row justify-between items-center bg-black/40 p-6 rounded-2xl border border-white/5 hover:border-blue-500/30 transition-colors">
                                                <div className="flex items-center gap-5 mb-4 md:mb-0">
                                                    <div className="bg-blue-500/10 text-blue-500 p-4 rounded-2xl"><Icon name="Calendar" size={24}/></div>
                                                    <div>
                                                        <h4 className="font-black text-lg">{m.title}</h4>
                                                        <p className="text-sm text-gray-400 flex items-center gap-2"><Icon name="Clock" size={14}/> {m.date} | المنصة: {m.type}</p>
                                                    </div>
                                                </div>
                                                <button className="w-full md:w-auto bg-blue-600 text-white px-8 py-3 rounded-xl font-black hover:bg-blue-500 shadow-lg flex items-center justify-center gap-2">
                                                    <Icon name="Video" size={18}/> الانضمام للغرفة
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab 3: Performance Radar */}
                        {activeTab === 'performance' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="TrendingUp" className="text-green-500" size={32}/> رادار أداء القادة (الجيل الأول)</h2>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    {[
                                        {name: 'أحمد المصري', sales: 12500, target: 15000, status: 'ممتاز'},
                                        {name: 'صالح فهد', sales: 8400, target: 10000, status: 'جيد'},
                                        {name: 'سارة خالد', sales: 2100, target: 10000, status: 'يحتاج دعم'}
                                    ].map((leader, i) => {
                                        const prog = (leader.sales / leader.target) * 100;
                                        const color = prog > 80 ? 'bg-green-500' : prog > 50 ? 'bg-yellow-500' : 'bg-red-500';
                                        return (
                                            <div key={i} className="glass-panel p-8 rounded-[2rem]">
                                                <div className="flex items-center gap-4 mb-6">
                                                    <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-xl border border-white/10">👤</div>
                                                    <div>
                                                        <h4 className="font-black text-lg">{leader.name}</h4>
                                                        <span className="text-[10px] text-gray-500 font-bold uppercase">{leader.status}</span>
                                                    </div>
                                                </div>
                                                <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden mb-3">
                                                    <div className={`h-full ${color}`} style={{width: `${prog}%`}}></div>
                                                </div>
                                                <div className="flex justify-between text-xs font-bold">
                                                    <span className="text-gray-400">مبيعات: ${leader.sales}</span>
                                                    <span className="text-gray-500">الهدف: ${leader.target}</span>
                                                </div>
                                                <button onClick={()=>showToast('تم إرسال برقية دعم للقائد')} className="mt-6 w-full py-2 border border-white/10 rounded-lg text-xs font-black hover:bg-white/10">إرسال تحفيز 💬</button>
                                            </div>
                                        )
                                    })}
                                </div>
                            </div>
                        )}

                    </div>

                    {/* Toasts */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-2 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className="bg-black/90 border border-yellow-500/30 text-yellow-500 px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-view">
                                <Icon name="CheckCircle2" size={18} />
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
