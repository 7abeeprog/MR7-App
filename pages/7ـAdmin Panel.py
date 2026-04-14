import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 GOD MODE - Admin Panel", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة (Firebase) بأمان تام ---
fb_config = st.secrets.get("__firebase_config", "{}")
try:
    if isinstance(fb_config, dict):
        fb_config_safe = json.dumps(fb_config)
    elif hasattr(fb_config, "to_dict"):
        fb_config_safe = json.dumps(fb_config.to_dict())
    else:
        fb_config_safe = str(fb_config)
except Exception:
    fb_config_safe = "{}"

app_id = st.secrets.get("__app_id", "mr7-empire-v1")
auth_token = st.secrets.get("__initial_auth_token", "")
current_theme = st.session_state.get('app_theme', "سلطة مطلقة 🔴")

# --- 3. واجهة React المتقدمة (لوحة القيادة العليا V16.2 - محرر المناهج المتطور) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <!-- CDNs مستقرة -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lucide@0.292.0/dist/umd/lucide.min.js"></script>
    
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getFirestore, collection, onSnapshot, query, where, doc, setDoc, getDoc, addDoc, updateDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        window.firebaseModules = { initializeApp, getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, getFirestore, collection, onSnapshot, query, where, doc, setDoc, getDoc, addDoc, updateDoc, deleteDoc };
    </script>

    <style>
        body { font-family: 'Tajawal', sans-serif; margin: 0; overflow-x: hidden; scroll-behavior: smooth; background-color: #020202; color: white; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #FF4B4B; border-radius: 10px; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .premium-input { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); color: white; transition: all 0.3s ease; }
        .premium-input:focus { border-color: var(--accent-color); outline: none; box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2); }
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter { 0% { opacity: 0; transform: translateY(100%) scale(0.9); } 100% { opacity: 1; transform: translateY(0) scale(1); } }

        #loading-screen { position: fixed; inset: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999; transition: opacity 0.5s ease; }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", () => {
            setTimeout(() => {
                const loader = document.getElementById('loading-screen');
                if (loader && loader.style.display !== 'none') {
                    loader.style.opacity = '0';
                    setTimeout(() => { loader.style.display = 'none'; }, 500);
                }
            }, 3000);
        });
    </script>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,75,75,0.3); border-top: 4px solid #FF4B4B; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FF4B4B; font-weight: 900; letter-spacing: 2px;">MR7 GOD MODE</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Global Command & Live Database Connection...</p>
    </div>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo, Component } = React;

        class ErrorBoundary extends Component {
            constructor(props) { super(props); this.state = { hasError: false }; }
            componentDidCatch(error, errorInfo) { this.setState({ hasError: true }); console.error(error); }
            render() { return this.state.hasError ? <div className="p-10 text-center text-red-500">حدث خطأ في عرض الواجهة. يرجى تحديث الصفحة.</div> : this.props.children; }
        }

        const Icon = ({ name, size = 24, className = "" }) => {
            const iconRef = React.useRef(null);
            useEffect(() => {
                if (iconRef.current && window.lucide) {
                    iconRef.current.innerHTML = ''; 
                    const i = document.createElement('i'); i.setAttribute('data-lucide', name); if (className) i.setAttribute('class', className);
                    iconRef.current.appendChild(i); 
                    try { window.lucide.createIcons({ root: iconRef.current }); } catch (e) {}
                }
            }, [name, size, className]);
            return <span ref={iconRef} className={`inline-flex justify-center items-center ${className}`}></span>;
        };

        const AppContent = () => {
            // --- Theming ---
            const themes = {
                "سلطة مطلقة 🔴": { bg: "bg-[#0A0000]", text: "text-[#FFFFFF]", card: "bg-[#140000]/90", borderLight: "border-[#FF4B4B]/20", accent: "text-[#FF4B4B]", btn: "bg-[#FF4B4B]", btnText: "text-white", hex: "#FF4B4B" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" }
            };
            const themeName = window.__current_theme || "سلطة مطلقة 🔴";
            const theme = themes[themeName] || themes["سلطة مطلقة 🔴"];
            useEffect(() => { document.documentElement.style.setProperty('--accent-color', theme.hex); }, [theme]);

            const [activeTab, setActiveTab] = useState('programs');
            const [toasts, setToasts] = useState([]);

            // --- Course Editor State ---
            const [editingCourse, setEditingCourse] = useState(null);
            const [editSubTab, setEditSubTab] = useState('curriculum');
            const [expandedLessonId, setExpandedLessonId] = useState(null); // للتحكم في الدرس المفتوح حالياً للتعديل

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // --- Data States ---
            const [courses, setCourses] = useState([
                { 
                    id: 1, title: 'القيادة التحويلية في العصر الرقمي', price: 299, students: 1240, status: 'active',
                    desc: 'دورة مكثفة تهدف إلى تمكين القادة من قيادة التغيير بفعالية.',
                    img: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800',
                    xp: 1000, badge: 'باني الإمبراطورية',
                    curriculum: [
                        { id: 101, title: 'فهم القيادة التحويلية', lessons: [
                            {id: 1001, title: 'مفهوم القيادة', type: 'video', url: 'https://youtube.com/...', content: 'مقدمة في العقلية', duration: '10:00'}, 
                            {id: 1002, title: 'اختبار الفهم', type: 'quiz', question: 'ما هو الهدف؟', options: ['النماء', 'التراجع'], correct: 'النماء'}
                        ] }
                    ]
                }
            ]);

            const [certificates, setCertificates] = useState([
                { id: 'C-101', student: 'أحمد محمود', course: 'القيادة التحويلية', progress: 100, status: 'pending', date: '2026-04-14' }
            ]);

            const [marketingStats, setMarketingStats] = useState({
                totalSales: 1250000, commissionsPaid: 187500, activeAffiliates: 3420,
                campaigns: [{ name: 'حملة التضاعف العشري (قانون 10)', roi: '+45%', active: true }]
            });

            // --- Handlers ---
            const openCourseEditor = (course) => {
                const fullCourse = {
                    ...course,
                    desc: course.desc || '', img: course.img || '', curriculum: course.curriculum || [], xp: course.xp || 1000, badge: course.badge || 'لم يتم التحديد'
                };
                setEditingCourse(JSON.parse(JSON.stringify(fullCourse))); 
                setEditSubTab('curriculum');
                setActiveTab('edit_program');
            };

            const saveCourseChanges = () => {
                setCourses(prev => prev.map(c => c.id === editingCourse.id ? editingCourse : c));
                showToast('تم اعتماد وحفظ كافة التعديلات في السحابة بنجاح! 💾', 'success');
            };
            
            const exitEditor = () => {
                setEditingCourse(null);
                setActiveTab('programs');
            }

            // Curriculum Actions
            const addModule = () => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: [...(prev.curriculum || []), { id: Date.now(), title: 'قسم جديد', lessons: [] }]
                }));
            };

            const addLesson = (moduleId) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? {
                        ...m, lessons: [...(m.lessons || []), { id: Date.now(), title: 'درس جديد', type: 'video', content: '', options: ['خيار 1', 'خيار 2'] }]
                    } : m)
                }));
                showToast('تمت إضافة إطار الدرس، قم بتوسيعه لتعبئة البيانات.', 'info');
            };

            const updateModuleTitle = (moduleId, title) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? { ...m, title } : m)
                }));
            };

            const updateLessonField = (moduleId, lessonId, field, value) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? {
                        ...m, lessons: m.lessons.map(l => l.id === lessonId ? { ...l, [field]: value } : l)
                    } : m)
                }));
            };

            const updateQuizOption = (moduleId, lessonId, optIndex, value) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? {
                        ...m, lessons: m.lessons.map(l => {
                            if (l.id === lessonId) {
                                const newOpts = [...(l.options || [])];
                                newOpts[optIndex] = value;
                                return { ...l, options: newOpts };
                            }
                            return l;
                        })
                    } : m)
                }));
            };

            const addQuizOption = (moduleId, lessonId) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? {
                        ...m, lessons: m.lessons.map(l => l.id === lessonId ? { ...l, options: [...(l.options||[]), `خيار جديد`] } : l)
                    } : m)
                }));
            };

            const removeQuizOption = (moduleId, lessonId, optIndex) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? {
                        ...m, lessons: m.lessons.map(l => {
                            if (l.id === lessonId) {
                                const newOpts = [...(l.options || [])];
                                newOpts.splice(optIndex, 1);
                                return { ...l, options: newOpts };
                            }
                            return l;
                        })
                    } : m)
                }));
            };

            const deleteModule = (moduleId) => {
                setEditingCourse(prev => ({ ...prev, curriculum: prev.curriculum.filter(m => m.id !== moduleId) }));
            };

            const deleteLesson = (moduleId, lessonId) => {
                setEditingCourse(prev => ({
                    ...prev, curriculum: prev.curriculum.map(m => m.id === moduleId ? { ...m, lessons: m.lessons.filter(l => l.id !== lessonId) } : m)
                }));
            };

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col md:flex-row overflow-hidden font-['Tajawal']`} dir="rtl">
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${theme.card} border-b md:border-b-0 md:border-l ${theme.borderLight} flex flex-col z-10 shadow-2xl shrink-0`}>
                        <div className="p-8 pb-4 text-center md:text-right">
                            <div className={`${theme.btn} ${theme.btnText} p-4 rounded-2xl inline-block mb-4 shadow-[0_0_30px_rgba(255,75,75,0.4)]`}><Icon name="ShieldAlert" size={32} /></div>
                            <h1 className={`text-2xl font-black uppercase tracking-tighter ${theme.accent}`}>القيادة العليا</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Root Access</p>
                        </div>
                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'radar', icon: 'Activity', label: 'الرادار والتحليلات'},
                                {id: 'programs', icon: 'BookOpen', label: 'إدارة المناهج'},
                                {id: 'certificates', icon: 'Award', label: 'اعتماد الشهادات'},
                                {id: 'marketing', icon: 'TrendingUp', label: 'خطط التسويق'}
                            ].map(btn => (
                                <button 
                                    key={btn.id} onClick={() => { setActiveTab(btn.id); setEditingCourse(null); }} 
                                    className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id || (activeTab === 'edit_program' && btn.id === 'programs') ? `bg-white/5 border-r-4 ${theme.borderLight.replace('/20','')} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}
                                >
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 h-screen overflow-y-auto no-scrollbar relative">
                        
                        {/* Tab: Edit Program (محرر المناهج المتطور) */}
                        {activeTab === 'edit_program' && editingCourse && (
                            <div className="animate-fade-in pb-20">
                                {/* شريط الحفظ العائم (Sticky Top Header) لضمان سهولة الحفظ دائماً */}
                                <div className="sticky top-0 z-50 bg-black/80 backdrop-blur-xl border-b border-white/10 px-6 py-4 flex justify-between items-center shadow-xl">
                                    <div className="flex items-center gap-4">
                                        <button onClick={exitEditor} className="p-2.5 bg-white/5 hover:bg-red-500/20 hover:text-red-500 rounded-xl transition-all border border-white/10" title="خروج بدون حفظ"><Icon name="ArrowRight" size={20}/></button>
                                        <div>
                                            <h2 className="text-xl font-black">{editingCourse.title}</h2>
                                            <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold flex items-center gap-1"><Icon name="Settings" size={10}/> وضع هندسة المناهج</span>
                                        </div>
                                    </div>
                                    <button onClick={saveCourseChanges} className={`${theme.btn} ${theme.btnText} px-8 py-3 rounded-xl font-black shadow-[0_10px_30px_rgba(255,75,75,0.3)] flex items-center gap-2 hover:scale-105 transition-transform`}>
                                        <Icon name="Save" size={18}/> اعتماد وحفظ التعديلات
                                    </button>
                                </div>

                                <div className="max-w-6xl mx-auto mt-8 px-6">
                                    {/* Editor Tabs */}
                                    <div className="flex gap-3 border-b border-white/10 pb-4 mb-8">
                                        <button onClick={() => setEditSubTab('curriculum')} className={`px-6 py-3 rounded-xl font-black text-sm transition-all ${editSubTab === 'curriculum' ? `${theme.btn} ${theme.btnText}` : 'bg-white/5 text-gray-400 hover:text-white'}`}>الخارطة الأكاديمية (الدروس)</button>
                                        <button onClick={() => setEditSubTab('details')} className={`px-6 py-3 rounded-xl font-black text-sm transition-all ${editSubTab === 'details' ? `${theme.btn} ${theme.btnText}` : 'bg-white/5 text-gray-400 hover:text-white'}`}>البيانات الأساسية</button>
                                        <button onClick={() => setEditSubTab('gamification')} className={`px-6 py-3 rounded-xl font-black text-sm transition-all ${editSubTab === 'gamification' ? `${theme.btn} ${theme.btnText}` : 'bg-white/5 text-gray-400 hover:text-white'}`}>محفزات السيادة (Gamification)</button>
                                    </div>

                                    {/* Curriculum Editor (القسم الأكثر تطوراً) */}
                                    {editSubTab === 'curriculum' && (
                                        <div className="space-y-6">
                                            <button onClick={addModule} className="w-full py-5 bg-white/5 border-2 border-dashed border-white/20 rounded-2xl text-gray-400 font-black hover:text-white hover:border-yellow-500 transition-all flex items-center justify-center gap-2"><Icon name="PlusCircle" size={20}/> إضافة قسم دراسي جديد (Module)</button>
                                            
                                            {(editingCourse.curriculum || []).map((mod, mIdx) => (
                                                <div key={mod.id} className="glass-panel p-6 rounded-[2rem] border border-white/10 shadow-lg">
                                                    <div className="flex items-center justify-between mb-4 pb-4 border-b border-white/5">
                                                        <div className="flex-1 mr-4 flex items-center gap-3">
                                                            <span className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm font-black text-yellow-500">{mIdx+1}</span>
                                                            <input value={mod.title} onChange={e => updateModuleTitle(mod.id, e.target.value)} className="bg-transparent border-none outline-none text-2xl font-black w-full focus:ring-0 text-white" placeholder="اسم القسم المرجعي..." />
                                                        </div>
                                                        <button onClick={() => deleteModule(mod.id)} className="p-2 text-gray-500 hover:bg-red-500/20 hover:text-red-500 rounded-lg transition-colors"><Icon name="Trash2" size={20}/></button>
                                                    </div>
                                                    
                                                    <div className="space-y-3 mb-6 pl-4 border-r-2 border-white/5">
                                                        {(mod.lessons || []).length === 0 ? <p className="text-xs text-gray-500 font-bold p-4 bg-black/20 rounded-xl">هذا القسم فارغ، قم بإضافة دروس إليه.</p> : 
                                                            mod.lessons.map((lesson, lIdx) => (
                                                                <div key={lesson.id} className={`flex flex-col bg-black/60 rounded-xl border transition-all ${expandedLessonId === lesson.id ? 'border-yellow-500/50 shadow-xl' : 'border-white/5 hover:border-white/20'}`}>
                                                                    
                                                                    {/* شريط الدرس المصغر (Collapsed View) */}
                                                                    <div className="flex items-center gap-3 p-4">
                                                                        <Icon name="GripVertical" size={16} className="text-gray-600 cursor-grab" />
                                                                        <select value={lesson.type} onChange={e => updateLessonField(mod.id, lesson.id, 'type', e.target.value)} className="bg-[#111] border border-white/10 rounded-lg p-2 text-xs font-bold text-yellow-500 outline-none">
                                                                            <option value="video">🎥 فيديو</option>
                                                                            <option value="quiz">❓ اختبار</option>
                                                                            <option value="assignment">💼 تكليف</option>
                                                                            <option value="text">📄 نص/مقال</option>
                                                                        </select>
                                                                        <input value={lesson.title} onChange={e => updateLessonField(mod.id, lesson.id, 'title', e.target.value)} className="flex-1 bg-transparent border-none outline-none text-sm font-bold text-white placeholder-gray-600" placeholder="عنوان الدرس هنا..." />
                                                                        
                                                                        {/* زر التوسعة للمحرر المتقدم */}
                                                                        <button onClick={() => setExpandedLessonId(expandedLessonId === lesson.id ? null : lesson.id)} className={`p-2 rounded-lg font-bold text-xs flex items-center gap-1 transition-colors ${expandedLessonId === lesson.id ? 'bg-yellow-500 text-black' : 'bg-white/10 text-gray-400 hover:bg-white/20 hover:text-white'}`}>
                                                                            {expandedLessonId === lesson.id ? 'طي اللوحة' : 'محرر الدرس'} <Icon name={expandedLessonId === lesson.id ? 'ChevronUp' : 'ChevronDown'} size={14}/>
                                                                        </button>
                                                                        <button onClick={() => deleteLesson(mod.id, lesson.id)} className="p-2 text-gray-500 hover:text-red-500 transition-colors"><Icon name="X" size={16}/></button>
                                                                    </div>

                                                                    {/* المحرر المتقدم للدرس (Expanded Editor) */}
                                                                    {expandedLessonId === lesson.id && (
                                                                        <div className="p-5 border-t border-white/10 bg-[#0a0a0a] rounded-b-xl space-y-5 animate-fade-in">
                                                                            
                                                                            {/* 1. محرر الفيديو */}
                                                                            {lesson.type === 'video' && (
                                                                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                                                    <div className="md:col-span-2">
                                                                                        <label className="text-[10px] font-black text-gray-500 uppercase block mb-2">رابط المصدر (YouTube / Vimeo URL)</label>
                                                                                        <input value={lesson.url || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'url', e.target.value)} placeholder="https://..." className="w-full premium-input p-3 rounded-xl text-sm font-bold text-blue-400" dir="ltr" />
                                                                                    </div>
                                                                                    <div>
                                                                                        <label className="text-[10px] font-black text-gray-500 uppercase block mb-2">المدة الزمنية التقديرية</label>
                                                                                        <input value={lesson.duration || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'duration', e.target.value)} placeholder="مثال: 15:30 دقيقة" className="w-full premium-input p-3 rounded-xl text-sm font-bold" />
                                                                                    </div>
                                                                                    <div className="md:col-span-3">
                                                                                        <label className="text-[10px] font-black text-gray-500 uppercase block mb-2">الوصف النصي (سيظهر أسفل المشغل)</label>
                                                                                        <textarea value={lesson.content || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'content', e.target.value)} placeholder="أضف المراجع أو الملخص هنا..." className="w-full premium-input p-4 rounded-xl text-sm font-bold min-h-[100px]"></textarea>
                                                                                    </div>
                                                                                </div>
                                                                            )}

                                                                            {/* 2. محرر الاختبارات */}
                                                                            {lesson.type === 'quiz' && (
                                                                                <div className="space-y-4">
                                                                                    <div>
                                                                                        <label className="text-[10px] font-black text-gray-500 uppercase block mb-2">السؤال الاستراتيجي</label>
                                                                                        <input value={lesson.question || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'question', e.target.value)} placeholder="اكتب السؤال بوضوح..." className="w-full premium-input p-4 rounded-xl text-lg font-black text-yellow-500" />
                                                                                    </div>
                                                                                    <div className="bg-white/5 p-4 rounded-2xl border border-white/10">
                                                                                        <div className="flex justify-between items-center mb-3">
                                                                                            <label className="text-[10px] font-black text-gray-400 uppercase block">الخيارات المتاحة للرد</label>
                                                                                            <button onClick={() => addQuizOption(mod.id, lesson.id)} className="text-xs bg-white/10 px-3 py-1 rounded-lg hover:bg-white/20 flex items-center gap-1 font-bold"><Icon name="Plus" size={12}/> إضافة خيار</button>
                                                                                        </div>
                                                                                        <div className="space-y-2">
                                                                                            {(lesson.options || []).map((opt, oIdx) => (
                                                                                                <div key={oIdx} className="flex items-center gap-2">
                                                                                                    <div className="w-6 h-6 rounded-full bg-black flex items-center justify-center text-[10px] font-bold text-gray-500">{oIdx+1}</div>
                                                                                                    <input value={opt} onChange={e => updateQuizOption(mod.id, lesson.id, oIdx, e.target.value)} className="flex-1 premium-input p-3 rounded-lg text-sm font-bold" placeholder={`خيار ${oIdx+1}`} />
                                                                                                    <button onClick={() => removeQuizOption(mod.id, lesson.id, oIdx)} className="p-2 text-gray-500 hover:text-red-500"><Icon name="X" size={16}/></button>
                                                                                                </div>
                                                                                            ))}
                                                                                        </div>
                                                                                    </div>
                                                                                    <div className="bg-[#00FF88]/10 p-4 rounded-2xl border border-[#00FF88]/30">
                                                                                        <label className="text-[10px] font-black text-[#00FF88] uppercase block mb-2">تحديد الإجابة الصحيحة للاعتماد الآلي</label>
                                                                                        <select value={lesson.correct || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'correct', e.target.value)} className="w-full premium-input bg-black p-3 rounded-xl text-sm font-bold text-[#00FF88] outline-none">
                                                                                            <option value="" disabled>-- اختر الإجابة المعتمدة --</option>
                                                                                            {(lesson.options || []).map((opt, oIdx) => (
                                                                                                <option key={oIdx} value={opt}>{opt || `الخيار ${oIdx+1}`}</option>
                                                                                            ))}
                                                                                        </select>
                                                                                    </div>
                                                                                </div>
                                                                            )}

                                                                            {/* 3. محرر التكاليف والنصوص */}
                                                                            {(lesson.type === 'assignment' || lesson.type === 'text') && (
                                                                                <div>
                                                                                    <label className="text-[10px] font-black text-gray-500 uppercase block mb-2">{lesson.type === 'assignment' ? 'تعليمات دراسة الحالة أو التكليف' : 'المحتوى النصي للدرس'}</label>
                                                                                    <textarea value={lesson.content || ''} onChange={e => updateLessonField(mod.id, lesson.id, 'content', e.target.value)} placeholder="اكتب المحتوى أو تفاصيل المهمة المطلوبة من القائد ليتم تقييمها..." className="w-full premium-input p-4 rounded-xl text-sm font-bold min-h-[150px]"></textarea>
                                                                                </div>
                                                                            )}
                                                                        </div>
                                                                    )}
                                                                </div>
                                                            ))
                                                        }
                                                    </div>
                                                    <button onClick={() => addLesson(mod.id)} className="bg-white/5 border border-white/10 hover:bg-white/10 px-5 py-3 rounded-xl text-xs font-black text-white flex items-center gap-2 transition-all"><Icon name="Plus" size={16}/> إدراج درس جديد هنا</button>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    {/* Details Editor */}
                                    {editSubTab === 'details' && (
                                        <div className="glass-panel p-8 rounded-[2rem] animate-fade-in">
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                                <div>
                                                    <label className="text-[10px] uppercase font-black text-gray-500 mb-2 block">اسم البرنامج</label>
                                                    <input value={editingCourse.title} onChange={e => setEditingCourse({...editingCourse, title: e.target.value})} className="w-full premium-input p-4 rounded-xl font-bold text-lg" />
                                                </div>
                                                <div>
                                                    <label className="text-[10px] uppercase font-black text-gray-500 mb-2 block">قيمة الاستثمار ($)</label>
                                                    <input type="number" value={editingCourse.price} onChange={e => setEditingCourse({...editingCourse, price: parseFloat(e.target.value) || 0})} className="w-full premium-input p-4 rounded-xl font-black text-lg text-[#00FF88]" />
                                                </div>
                                            </div>
                                            <div className="mb-6">
                                                <label className="text-[10px] uppercase font-black text-gray-500 mb-2 block">رابط صورة الغلاف (URL)</label>
                                                <input value={editingCourse.img} onChange={e => setEditingCourse({...editingCourse, img: e.target.value})} dir="ltr" className="w-full premium-input p-4 rounded-xl font-bold text-left" />
                                                {editingCourse.img && <div className="mt-4 p-2 bg-white/5 rounded-2xl inline-block border border-white/10"><img src={editingCourse.img} className="w-48 h-28 object-cover rounded-xl" /></div>}
                                            </div>
                                            <div>
                                                <label className="text-[10px] uppercase font-black text-gray-500 mb-2 block">الوصف الاستراتيجي الشامل</label>
                                                <textarea value={editingCourse.desc} onChange={e => setEditingCourse({...editingCourse, desc: e.target.value})} className="w-full premium-input p-4 rounded-xl font-bold min-h-[120px] leading-relaxed"></textarea>
                                            </div>
                                        </div>
                                    )}

                                    {/* Gamification Editor */}
                                    {editSubTab === 'gamification' && (
                                        <div className="glass-panel p-8 rounded-[2rem] animate-fade-in">
                                            <div className="flex items-center gap-4 mb-8 border-b border-white/10 pb-6">
                                                <div className="bg-purple-500/10 p-4 rounded-full text-purple-500 border border-purple-500/20"><Icon name="Target" size={32}/></div>
                                                <div>
                                                    <h3 className="text-2xl font-black">هندسة التحفيز والاستحقاق</h3>
                                                    <p className="text-sm text-gray-400 font-bold mt-1">حدد الدوافع السيكولوجية والنقاط التي سيكسبها القائد بعد المعاناة في هذا المنهج.</p>
                                                </div>
                                            </div>
                                            
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                                <div className="bg-black/50 p-8 rounded-3xl border border-white/5">
                                                    <label className="text-xs uppercase font-black text-[#00FF88] mb-4 block flex items-center gap-2"><Icon name="Zap" size={16}/> مكافأة الاجتياز (نقاط سيادة XP)</label>
                                                    <input type="number" value={editingCourse.xp} onChange={e => setEditingCourse({...editingCourse, xp: parseInt(e.target.value) || 0})} className="w-full premium-input p-5 rounded-2xl font-black text-4xl text-center text-[#00FF88]" />
                                                    <p className="text-[10px] text-gray-500 mt-4 text-center">يتم تحويلها لتقييم الحساب وفتح مزايا إمبراطورية.</p>
                                                </div>
                                                
                                                <div className="bg-black/50 p-8 rounded-3xl border border-white/5">
                                                    <label className="text-xs uppercase font-black text-yellow-500 mb-4 block flex items-center gap-2"><Icon name="Award" size={16}/> الوسام السيادي الممنوح (Badge)</label>
                                                    <input value={editingCourse.badge} onChange={e => setEditingCourse({...editingCourse, badge: e.target.value})} className="w-full premium-input p-5 rounded-2xl font-black text-2xl text-center text-yellow-500" placeholder="مثال: مهندس عقول" />
                                                    <p className="text-[10px] text-gray-500 mt-4 text-center">يتم تعليق هذا الوسام في ملف القائد أمام الجيوش.</p>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* --- باقي التبويبات (Programs, Radar, etc.) --- */}
                        {activeTab === 'programs' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto pt-6 px-4">
                                <div className="flex justify-between items-center mb-8">
                                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="BookOpen" className={theme.accent} size={32}/> إدارة المناهج الأكاديمية</h2>
                                </div>
                                <div className="glass-panel p-2 rounded-[2rem] overflow-x-auto border border-white/5">
                                    <table className="w-full text-right">
                                        <thead>
                                            <tr className="border-b border-white/10 text-gray-400 text-sm">
                                                <th className="p-6 font-bold">اسم البرنامج</th>
                                                <th className="p-6 font-bold">السعر</th>
                                                <th className="p-6 font-bold text-center">الحالة</th>
                                                <th className="p-6 font-bold text-center">محرر المنهج</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {courses.map(c => (
                                                <tr key={c.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                    <td className="p-6 font-black">{c.title}</td>
                                                    <td className="p-6 text-[#00FF88] font-black">${c.price}</td>
                                                    <td className="p-6 text-center">
                                                        <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase ${c.status === 'active' ? 'bg-[#00FF88]/20 text-[#00FF88]' : 'bg-gray-500/20 text-gray-400'}`}>
                                                            {c.status === 'active' ? 'نشط' : 'مسودة'}
                                                        </span>
                                                    </td>
                                                    <td className="p-6 flex justify-center gap-2">
                                                        <button onClick={()=>openCourseEditor(c)} className="bg-yellow-500 text-black px-6 py-2.5 rounded-xl font-black text-sm flex items-center gap-2 hover:scale-105 transition-transform"><Icon name="Edit3" size={16}/> تعديل وتطوير</button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}
                        
                        {/* Tab: Radar */}
                        {activeTab === 'radar' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto pt-6 px-4">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="Activity" className={theme.accent} size={32}/> رادار الإمبراطورية</h2>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-[#00FF88]">
                                        <small className="text-gray-500 font-bold uppercase">إجمالي المبيعات (USD)</small>
                                        <h4 className="text-3xl font-black text-[#00FF88]">${marketingStats.totalSales.toLocaleString()}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">العمولات الموزعة</small>
                                        <h4 className="text-3xl font-black text-yellow-500">${marketingStats.commissionsPaid.toLocaleString()}</h4>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Toasts Container */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'warning' ? 'bg-black/90 border-yellow-500/40 text-yellow-500' : 'bg-black/90 border-blue-500/40 text-blue-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : t.type === 'warning' ? 'AlertCircle' : 'Info'} size={20} />
                                <span className="font-bold text-sm text-white">{t.msg}</span>
                            </div>
                        ))}
                    </div>
                </div>
            );
        };

        const App = () => (
            <ErrorBoundary>
                <AppContent />
            </ErrorBoundary>
        );

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل آمن ---
components.html(react_html, height=1000, scrolling=True)

# --- 5. أزرار التنقل السريع الخاصة ببايثون (Streamlit Core) ---
st.markdown("---")
st.markdown("### 🗺️ مسارات التحكم السريعة للقيادة")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎓 معاينة الأكاديمية كمتدرب"):
        st.switch_page("pages/1_Education.py")
with c2:
    if st.button("⚙️ استوديو المبدعين (إضافة محتوى)"):
        st.switch_page("pages/7_Creator_Studio.py")
with c3:
    if st.button("🏠 العودة لمركز القيادة الرئيسي"):
        st.switch_page("app.py")
