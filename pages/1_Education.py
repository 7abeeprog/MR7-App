import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Education Academy", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة (Firebase) ---
fb_config = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
auth_token = st.secrets.get("__initial_auth_token", "")
current_theme = st.session_state.get('app_theme', "سلطة مطلقة 🔴")

# --- 3. واجهة React المتقدمة (أكاديمية التريليون - V13.0 - قاعة الدراسة المستقلة) ---
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
    
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getFirestore, collection, onSnapshot, query, where } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        window.firebaseModules = { initializeApp, getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, getFirestore, collection, onSnapshot, query, where };
    </script>

    <style>
        body { font-family: 'Tajawal', sans-serif; margin: 0; overflow-x: hidden; scroll-behavior: smooth; transition: background-color 0.5s, color 0.5s; background-color: #020202; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }
        
        .course-card {
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background: linear-gradient(180deg, rgba(20,20,20,0.9) 0%, rgba(5,5,5,1) 100%);
        }
        .course-card:hover { transform: translateY(-10px) scale(1.02); z-index: 10; box-shadow: 0 20px 40px rgba(0,0,0,0.8); border-color: var(--accent-color); }

        .premium-input { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); color: white; transition: all 0.3s ease; }
        .premium-input:focus { outline: none; border-color: var(--accent-color); box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1); }
        
        .animate-fade-in { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .module-item { transition: 0.2s; border-right: 3px solid transparent; }
        .module-item:hover { background: rgba(255,255,255,0.05); border-right-color: var(--accent-color); }
        .module-item.active { background: rgba(255,255,255,0.1); border-right-color: var(--accent-color); }

        #loading-screen { position: fixed; inset: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999; }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,255,255,0.1); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FFD700; font-weight: 900; letter-spacing: 2px;">MR7 ACADEMY</h2>
    </div>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

        const Icon = ({ name, size = 24, className = "" }) => {
            const iconRef = React.useRef(null);
            useEffect(() => {
                if (iconRef.current && window.lucide) {
                    iconRef.current.innerHTML = ''; 
                    const i = document.createElement('i'); i.setAttribute('data-lucide', name); if (className) i.setAttribute('class', className);
                    iconRef.current.appendChild(i); window.lucide.createIcons({ root: iconRef.current });
                }
            }, [name, size, className]);
            return <span ref={iconRef} className={`inline-flex justify-center items-center ${className}`}></span>;
        };

        // --- واجهة قاعة الدراسة المستقلة (Course Viewer) ---
        const CourseViewer = ({ course, onBack, theme }) => {
            const [activeModule, setActiveModule] = useState(1);
            
            // هيكل دراسي افتراضي لمحاكاة المحتوى
            const curriculum = [
                { id: 1, title: "مقدمة في العقلية السيادية", duration: "15:00", type: "video" },
                { id: 2, title: "تحليل الأسواق والاتجاهات", duration: "22:30", type: "video" },
                { id: 3, title: "المهمة الأولى: كتابة الوثيقة", duration: "10:00", type: "document" },
                { id: 4, title: "قانون الـ 10 للتضاعف", duration: "45:00", type: "video", locked: course.locked },
                { id: 5, title: "الاختبار الاستراتيجي الأول", duration: "20:00", type: "quiz", locked: course.locked }
            ];

            return (
                <div className="min-h-screen bg-[#050505] flex flex-col animate-fade-in" dir="rtl">
                    {/* شريط التنقل الخاص بقاعة الدراسة */}
                    <nav className="glass-panel border-b border-white/10 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
                        <div className="flex items-center gap-6">
                            <button 
                                onClick={onBack} 
                                className="flex items-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-2.5 rounded-xl font-bold transition-all text-gray-300 hover:text-white"
                            >
                                <Icon name="ArrowRight" size={18} /> العودة للأكاديمية
                            </button>
                            <div className="h-8 w-px bg-white/10"></div>
                            <div>
                                <span className="text-[10px] uppercase font-black tracking-widest text-gray-500 block mb-0.5">{course.phase}</span>
                                <h2 className="text-lg font-black text-white">{course.title}</h2>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="text-left">
                                <span className="text-[10px] text-gray-500 font-bold uppercase block mb-1">نسبة الإنجاز</span>
                                <div className="w-32 h-1.5 bg-white/10 rounded-full overflow-hidden">
                                    <div className="h-full" style={{width: `${course.progress}%`, backgroundColor: theme.hex}}></div>
                                </div>
                            </div>
                            <button className={`p-2.5 rounded-xl border border-white/10 hover:bg-white/5`}>
                                <Icon name="Share2" size={18} />
                            </button>
                        </div>
                    </nav>

                    <div className="flex flex-1 overflow-hidden h-[calc(100vh-80px)]">
                        {/* مساحة عرض المحتوى (Video/Content Area) */}
                        <div className="flex-1 flex flex-col bg-black relative overflow-y-auto no-scrollbar">
                            {course.locked ? (
                                <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#0a0a0a] z-10 p-8 text-center">
                                    <div className="w-24 h-24 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mb-6 border border-red-500/20">
                                        <Icon name="Lock" size={40} />
                                    </div>
                                    <h2 className="text-3xl font-black mb-4">هذا المحتوى مشفر</h2>
                                    <p className="text-gray-400 max-w-md mb-8 leading-relaxed">أنت بحاجة إلى صلاحيات سيادية لفتح هذا الأصل المعرفي. استثمر في تطوير ذاتك للوصول إلى هذا المستوى.</p>
                                    <button className={`px-10 py-5 rounded-2xl font-black text-lg ${theme.btn} ${theme.btnText} shadow-[0_0_30px_rgba(255,215,0,0.3)] hover:scale-105 transition-transform flex items-center gap-3`}>
                                        <Icon name="CreditCard" size={22} /> دفع ${course.price} لفك التشفير
                                    </button>
                                </div>
                            ) : (
                                <div className="w-full aspect-video bg-[#111] border-b border-white/5 flex items-center justify-center relative">
                                    {/* محاكي مشغل الفيديو */}
                                    <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-30" />
                                    <button className="w-20 h-20 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center border border-white/20 transition-all z-10 hover:scale-110">
                                        <Icon name="Play" size={30} className="text-white ml-2" />
                                    </button>
                                </div>
                            )}
                            
                            <div className="p-8 md:p-12 max-w-4xl mx-auto w-full">
                                <h1 className="text-3xl font-black mb-6">{curriculum.find(c => c.id === activeModule)?.title || course.title}</h1>
                                <p className="text-gray-400 leading-relaxed text-lg mb-8">
                                    {course.desc} هنا سيتم عرض التفاصيل النصية للدرس، المرفقات، وملخص الفيديو. 
                                    الذكاء الاصطناعي سيقوم بتلخيص هذا المحتوى تلقائياً للقائد لتسريع عملية التعلم والمراجعة.
                                </p>
                                
                                <div className="flex gap-4">
                                    <button className="flex-1 bg-white/5 hover:bg-white/10 border border-white/10 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors">
                                        <Icon name="FileText" size={18} /> تحميل المرفقات (PDF)
                                    </button>
                                    <button className="flex-1 bg-white/5 hover:bg-white/10 border border-white/10 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors">
                                        <Icon name="MessageSquare" size={18} /> مناقشة مع القادة
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* القائمة الجانبية للمنهج (Curriculum Sidebar) */}
                        <div className="w-80 bg-[#0a0a0a] border-r border-white/10 flex flex-col hidden lg:flex h-full overflow-y-auto no-scrollbar">
                            <div className="p-6 border-b border-white/5">
                                <h3 className="font-black text-lg mb-1">محتوى المنهج السيادي</h3>
                                <p className="text-xs text-gray-500 font-bold">{curriculum.length} وحدات تدريبية</p>
                            </div>
                            <div className="flex flex-col">
                                {curriculum.map((mod, index) => (
                                    <div 
                                        key={mod.id} 
                                        onClick={() => !mod.locked && setActiveModule(mod.id)}
                                        className={`module-item p-5 cursor-pointer border-b border-white/5 flex items-start gap-4 ${activeModule === mod.id ? 'active' : ''} ${mod.locked ? 'opacity-40 cursor-not-allowed' : ''}`}
                                    >
                                        <div className={`mt-1 ${mod.locked ? 'text-red-500' : (activeModule === mod.id ? 'text-['+theme.hex+']' : 'text-gray-500')}`}>
                                            <Icon name={mod.locked ? 'Lock' : (mod.type === 'video' ? 'PlayCircle' : mod.type === 'quiz' ? 'HelpCircle' : 'FileText')} size={18} />
                                        </div>
                                        <div className="flex-1">
                                            <h4 className={`font-bold text-sm mb-1 ${activeModule === mod.id ? 'text-white' : 'text-gray-300'}`}>{index + 1}. {mod.title}</h4>
                                            <span className="text-[10px] text-gray-500 font-black">{mod.duration}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        const App = () => {
            // --- The 7x7 Engine ---
            const themes = {
                "سلطة مطلقة 🔴": { bg: "bg-[#0A0000]", text: "text-[#FFFFFF]", card: "bg-[#140000]/90", border: "border-[#FF4B4B]", accent: "text-[#FF4B4B]", btn: "bg-[#FF4B4B]", btnText: "text-white", hex: "#FF4B4B" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
            };
            const themeName = window.__current_theme || "أسود قيادي 🖤";
            const theme = themes[themeName] || themes["أسود قيادي 🖤"];
            
            useEffect(() => { document.documentElement.style.setProperty('--accent-color', theme.hex); }, [theme]);

            const [activeTab, setActiveTab] = useState('courses'); 
            const [selectedCourse, setSelectedCourse] = useState(null); // إذا كان له قيمة، يفتح الـ CourseViewer
            const [searchQ, setSearchQ] = useState('');
            const [selectedCategory, setSelectedCategory] = useState('الكل');

            // --- قاعدة بيانات الـ 100 برنامج (عينة للفرونت اند) ---
            const DB_COURSES = [
                { id: 1, phase: 'القيادة الاستراتيجية', title: 'القيادة التحويلية في العصر الرقمي', hours: 20, price: 299, img: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800', desc: 'إدارة التغيير وبناء الرؤية في بيئة عدم اليقين.', locked: false, progress: 45 },
                { id: 2, phase: 'الاستثمار والمالية', title: 'تحليل الأسهم وأسواق المال', hours: 25, price: 499, img: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800', desc: 'التحليل الأساسي والفني، قراءة القوائم المالية.', locked: true, progress: 0 },
                { id: 3, phase: 'التكنولوجيا والتحول', title: 'الذكاء الاصطناعي في الأعمال', hours: 15, price: 350, img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', desc: 'استخدام AI في التسويق والمالية وخدمة العملاء.', locked: true, progress: 0 },
                { id: 4, phase: 'ريادة الأعمال', title: 'من الفكرة إلى المشروع الشامل', hours: 25, price: 399, img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800', desc: 'نموذج العمل، دراسة الجدوى، والتمويل الأولي.', locked: true, progress: 0 },
                { id: 5, phase: 'المهارات الشخصية', title: 'الذكاء العاطفي في بيئة العمل', hours: 14, price: 150, img: 'https://images.unsplash.com/photo-1552581234-26160f608093?w=800', desc: 'الوعي الذاتي، إدارة العلاقات، والتأثير الإيجابي.', locked: true, progress: 0 },
                { id: 6, phase: 'الاقتصاد المستدام', title: 'الاستثمار في الطاقة المتجددة', hours: 16, price: 450, img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=800', desc: 'السندات الخضراء، طاقة الرياح، والتمويل المستدام.', locked: true, progress: 0 },
            ];

            const categories = ["الكل", ...new Set(DB_COURSES.map(c => c.phase))];

            const filteredCourses = useMemo(() => {
                return DB_COURSES.filter(c => {
                    const matchSearch = c.title.includes(searchQ) || c.desc.includes(searchQ);
                    const matchCat = selectedCategory === 'الكل' || c.phase === selectedCategory;
                    return matchSearch && matchCat;
                });
            }, [searchQ, selectedCategory]);

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            // إذا تم اختيار كورس، نعرض واجهة الـ CourseViewer بالكامل وراء الشاشة الرئيسية
            if (selectedCourse) {
                return <CourseViewer course={selectedCourse} onBack={() => setSelectedCourse(null)} theme={theme} />;
            }

            // الواجهة الرئيسية للأكاديمية (Academy Main View)
            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col font-['Tajawal']`} dir="rtl">
                    {/* Header */}
                    <nav className="glass-panel sticky top-0 z-40 border-b border-white/10">
                        <div className="max-w-[1600px] mx-auto px-6 md:px-10 py-5 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-4 w-full md:w-auto justify-between md:justify-start">
                                <div className="flex items-center gap-3">
                                    <div className={`p-3 rounded-2xl ${theme.btn} ${theme.btnText}`}><Icon name="GraduationCap" size={28} /></div>
                                    <div>
                                        <h1 className="text-2xl font-black tracking-tighter uppercase m-0">MR7 <span style={{color: theme.hex}}>ACADEMY</span></h1>
                                        <p className="text-[10px] text-gray-500 font-bold uppercase tracking-[0.2em] m-0">100 Days of Sovereignty</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div className="flex w-full md:w-auto bg-black/50 border border-white/10 rounded-2xl p-1 overflow-x-auto no-scrollbar">
                                {[
                                    {id: 'courses', label: 'المناهج السيادية', icon: 'BookOpen'},
                                    {id: 'articles', label: 'المدونة الاستراتيجية', icon: 'FileText'},
                                    {id: 'my_learning', label: 'قاعتي الدراسية', icon: 'MonitorPlay'}
                                ].map(tab => (
                                    <button 
                                        key={tab.id} onClick={() => setActiveTab(tab.id)}
                                        className={`flex items-center justify-center gap-2 flex-1 md:flex-none px-6 py-3 rounded-xl font-bold text-sm transition-all whitespace-nowrap ${activeTab === tab.id ? `${theme.btn} ${theme.btnText} shadow-lg` : 'text-gray-400 hover:text-white'}`}
                                    >
                                        <Icon name={tab.icon} size={16} /> {tab.label}
                                    </button>
                                ))}
                            </div>

                            <div className="flex items-center gap-3 relative w-full md:w-auto">
                                <Icon name="Search" size={18} className="absolute right-4 text-gray-500" />
                                <input 
                                    type="text" placeholder="ابحث في عقول القادة..." 
                                    value={searchQ} onChange={e=>setSearchQ(e.target.value)}
                                    className="premium-input bg-[#111] py-3 pr-12 pl-4 rounded-xl text-sm font-bold w-full md:w-64 focus:md:w-80 transition-all"
                                />
                            </div>
                        </div>
                    </nav>

                    <main className="flex-1 max-w-[1600px] mx-auto w-full px-6 md:px-10 py-10">
                        {activeTab === 'courses' && (
                            <div className="animate-fade-in">
                                {/* Categories */}
                                <div className="flex gap-3 overflow-x-auto no-scrollbar mb-10 pb-2">
                                    {categories.map(cat => (
                                        <button 
                                            key={cat} onClick={() => setSelectedCategory(cat)}
                                            className={`px-6 py-2.5 rounded-xl text-sm font-black whitespace-nowrap transition-all border ${selectedCategory === cat ? `${theme.btn} ${theme.btnText} border-transparent` : 'bg-transparent text-gray-400 border-white/10 hover:border-white/30'}`}
                                        >
                                            {cat}
                                        </button>
                                    ))}
                                </div>

                                {/* Grid */}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                                    {filteredCourses.map(course => (
                                        <div key={course.id} onClick={() => setSelectedCourse(course)} className="course-card rounded-[2rem] border border-white/10 overflow-hidden cursor-pointer group flex flex-col h-full relative bg-[#0a0a0a]">
                                            {/* صورة الكورس */}
                                            <div className="relative h-56 w-full overflow-hidden">
                                                <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                                                <img src={course.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                                                {course.locked && (
                                                    <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity">
                                                        <div className="bg-black/80 p-4 rounded-full border border-white/20 text-white"><Icon name="Lock" size={28} /></div>
                                                    </div>
                                                )}
                                            </div>
                                            
                                            {/* بيانات الكورس */}
                                            <div className="p-6 flex flex-col flex-1">
                                                <span className="text-[10px] font-black uppercase tracking-widest mb-3" style={{color: theme.hex}}>{course.phase}</span>
                                                <h3 className="text-xl font-black mb-3 line-clamp-2 text-white leading-tight">{course.title}</h3>
                                                <div className="flex items-center gap-4 text-xs font-bold text-gray-500 mb-6">
                                                    <span className="flex items-center gap-1"><Icon name="Clock" size={14}/> {course.hours} ساعة</span>
                                                </div>
                                                
                                                <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
                                                    {course.locked ? (
                                                        <div className="flex justify-between items-center w-full">
                                                          <span className="text-xs text-gray-500 font-bold uppercase">مغلق</span>
                                                          <span className="text-2xl font-black text-[#00FF88]">${course.price}</span>
                                                        </div>
                                                    ) : (
                                                        <div className="w-full">
                                                            <div className="flex justify-between text-[10px] font-bold mb-1 text-gray-400"><span>التقدم</span><span>{course.progress}%</span></div>
                                                            <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden"><div className="h-full" style={{width: `${course.progress}%`, backgroundColor: theme.hex}}></div></div>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {activeTab === 'articles' && (
                            <div className="animate-fade-in text-center py-24 bg-white/5 border border-dashed border-white/10 rounded-[3rem]">
                                <Icon name="BookOpen" size={80} className="mx-auto mb-6 text-gray-600" />
                                <h2 className="text-3xl font-black mb-4">المدونة السيادية والمقالات</h2>
                                <p className="text-gray-400 font-bold max-w-lg mx-auto">هنا سيكون محرك المحتوى والمقالات (CMS) جاهزاً لرفع مستوى الـ SEO للمنظومة عالمياً.</p>
                            </div>
                        )}
                        
                        {activeTab === 'my_learning' && (
                            <div className="animate-fade-in">
                                <h2 className="text-2xl font-black mb-8 border-b border-white/10 pb-4">مناهجي الدراسية (المفتوحة)</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                   {DB_COURSES.filter(c => !c.locked).map(course => (
                                        <div key={course.id} onClick={() => setSelectedCourse(course)} className="course-card rounded-[2rem] border border-white/10 overflow-hidden cursor-pointer group flex flex-col h-full relative bg-[#0a0a0a]">
                                            <div className="relative h-40 w-full overflow-hidden">
                                                <img src={course.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                                                <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                                    <Icon name="PlayCircle" size={40} className="text-white" />
                                                </div>
                                            </div>
                                            <div className="p-5 flex flex-col flex-1">
                                                <h3 className="text-lg font-black mb-4 line-clamp-1">{course.title}</h3>
                                                <div className="w-full mt-auto">
                                                    <div className="flex justify-between text-[10px] font-bold mb-1 text-gray-400"><span>استكمال</span><span>{course.progress}%</span></div>
                                                    <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden"><div className="h-full" style={{width: `${course.progress}%`, backgroundColor: theme.hex}}></div></div>
                                                </div>
                                            </div>
                                        </div>
                                   ))}
                                </div>
                            </div>
                        )}

                    </main>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات للواجهة ---
fb_config_safe = json.dumps(fb_config) if isinstance(fb_config, dict) else fb_config

components.html(f"""
    <script>
        window.__firebase_config = `{fb_config_safe}`;
        window.__app_id = "{app_id}";
        window.__initial_auth_token = "{auth_token}";
        window.__current_theme = "{current_theme}";
    </script>
    {react_html}
""", height=950, scrolling=True)

# --- 5. أزرار التنقل السريع ---
st.markdown("---")
st.markdown("### 🗺️ مسارات التحكم السريعة")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🛒 المتجر العالمي (نشر وتسويق)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("⚙️ استوديو المبدعين (إنشاء كورس)"):
        st.switch_page("pages/7_Creator_Studio.py")
with c3:
    if st.button("🏠 العودة لمركز القيادة"):
        st.switch_page("app.py")
