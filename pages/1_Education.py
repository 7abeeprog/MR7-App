import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Education Academy", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة وتأمين المتغيرات ---
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
current_theme = st.session_state.get('app_theme', "غامق إمبراطوري 🖤")

# --- 3. واجهة React المتقدمة (Micro-Frontend Architecture) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <!-- استخدام CDNs فائقة الاستقرار ومضادة للحظر (jsDelivr & Cloudflare) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lucide@0.292.0/dist/umd/lucide.min.js"></script>
    
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getFirestore, collection, onSnapshot, query, where } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        window.firebaseModules = { initializeApp, getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, getFirestore, collection, onSnapshot, query, where };
    </script>

    <style>
        body { font-family: 'Tajawal', sans-serif; margin: 0; overflow-x: hidden; scroll-behavior: smooth; background-color: #050505; color: white; }
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
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        #loading-screen { position: fixed; inset: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999; transition: opacity 0.5s ease; }
    </style>

    <!-- نظام الطوارئ الفائق: إخفاء الشاشة السوداء إجبارياً بعد 3 ثوانٍ -->
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
        <div style="border: 4px solid rgba(255,255,255,0.1); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FFD700; font-weight: 900; letter-spacing: 2px;">MR7 ACADEMY</h2>
    </div>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

        // --- مكون الأيقونات الآمن ---
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

        // =====================================================================
        // Micro-Frontend 1: Course Player (مشغل الكورس التفاعلي للمناهج المفتوحة)
        // =====================================================================
        const CoursePlayerView = ({ course, onBack, theme, showToast }) => {
            const firstLessonId = (course.curriculum && course.curriculum[0] && course.curriculum[0].lessons && course.curriculum[0].lessons[0]) ? course.curriculum[0].lessons[0].id : null;
            const [activeLessonId, setActiveLessonId] = useState(firstLessonId);
            const [completedLessons, setCompletedLessons] = useState([]);
            const [quizAnswers, setQuizAnswers] = useState({});

            let currentLesson = null;
            if (course.curriculum) {
                course.curriculum.forEach(mod => {
                    if (mod.lessons) {
                        const lesson = mod.lessons.find(l => l.id === activeLessonId);
                        if(lesson) currentLesson = lesson;
                    }
                });
            }

            const handleComplete = (lessonId, isQuiz = false, isCorrect = false) => {
                if (isQuiz && !isCorrect) {
                    showToast('إجابة خاطئة! القائد يتعلم من المحاولة.', 'error');
                    return;
                }
                if (!completedLessons.includes(lessonId)) {
                    setCompletedLessons([...completedLessons, lessonId]);
                    showToast(isQuiz ? 'إجابة صحيحة! +50 XP' : 'تم إنجاز الدرس! +20 XP', 'success');
                }
            };

            const totalLessons = course.curriculum ? course.curriculum.reduce((acc, mod) => acc + (mod.lessons ? mod.lessons.length : 0), 0) : 0;
            const progress = totalLessons === 0 ? 0 : (completedLessons.length / totalLessons) * 100;

            return (
                <div className="min-h-screen flex flex-col animate-fade-in bg-[#050505]" dir="rtl">
                    <nav className="glass-panel border-b border-white/10 px-8 py-5 flex items-center justify-between z-50">
                        <div className="flex items-center gap-6">
                            <button onClick={onBack} className="flex items-center gap-2 bg-white/5 hover:bg-white/10 px-5 py-2.5 rounded-xl font-bold transition-all border border-white/10"><Icon name="ArrowRight" size={18} /> العودة</button>
                            <div>
                                <span className="text-[10px] text-yellow-500 font-black uppercase tracking-widest">{course.phase}</span>
                                <h2 className="text-xl font-black text-white">{course.title}</h2>
                            </div>
                        </div>
                        <div className="w-48">
                            <div className="flex justify-between text-[10px] font-bold mb-1 text-gray-400"><span>التقدم</span><span>{progress.toFixed(0)}%</span></div>
                            <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden"><div className="h-full bg-yellow-500" style={{width: `${progress}%`}}></div></div>
                        </div>
                    </nav>

                    <div className="flex flex-1 overflow-hidden">
                        <div className="flex-1 overflow-y-auto no-scrollbar bg-black relative">
                            {currentLesson ? (
                                <div>
                                    {currentLesson.type === 'video' && (
                                        <div className="w-full aspect-video bg-[#111] relative flex items-center justify-center border-b border-white/10">
                                            <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-20" />
                                            <div className="z-10 bg-yellow-500 w-20 h-20 rounded-full flex items-center justify-center text-black cursor-pointer hover:scale-110 transition-transform shadow-[0_0_30px_rgba(255,215,0,0.4)]"><Icon name="Play" size={30} className="ml-2"/></div>
                                        </div>
                                    )}
                                    <div className="max-w-4xl mx-auto p-10">
                                        <h1 className="text-3xl font-black mb-6">{currentLesson.title}</h1>
                                        {currentLesson.type === 'quiz' ? (
                                            <div className="bg-white/5 border border-white/10 p-8 rounded-2xl">
                                                <p className="text-xl mb-6 font-bold">{currentLesson.question}</p>
                                                <div className="space-y-3">
                                                    {(currentLesson.options || []).map((opt, i) => (
                                                        <button key={i} onClick={() => setQuizAnswers({...quizAnswers, [currentLesson.id]: opt})} className={`w-full text-right p-4 rounded-xl font-bold border transition-all ${quizAnswers[currentLesson.id] === opt ? 'bg-yellow-500/20 border-yellow-500 text-white' : 'bg-black border-white/10 text-gray-400'}`}>{opt}</button>
                                                    ))}
                                                </div>
                                                <button onClick={() => handleComplete(currentLesson.id, true, quizAnswers[currentLesson.id] === currentLesson.correct)} className="mt-8 w-full py-4 bg-yellow-500 text-black font-black rounded-xl">تأكيد الإجابة</button>
                                            </div>
                                        ) : (
                                            <div>
                                                <div className="text-gray-300 leading-relaxed text-lg mb-10" dangerouslySetInnerHTML={{__html: currentLesson.content || 'محتوى الدرس...'}}></div>
                                                <button onClick={() => handleComplete(currentLesson.id)} className="w-full py-4 bg-[#00FF88] text-black font-black rounded-xl shadow-[0_0_20px_rgba(0,255,136,0.2)] flex items-center justify-center gap-2">إتمام الدرس <Icon name="CheckCircle2" size={20}/></button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ) : (
                                <div className="h-full flex items-center justify-center text-gray-500"><p className="font-bold text-xl">اختر درساً من القائمة</p></div>
                            )}
                        </div>

                        <div className="w-80 bg-[#0a0a0a] border-r border-white/10 overflow-y-auto no-scrollbar">
                            <div className="p-6 border-b border-white/5"><h3 className="font-black text-lg">المحتوى الأكاديمي</h3></div>
                            {(course.curriculum || []).map((mod, i) => (
                                <div key={i} className="border-b border-white/5">
                                    <div className="p-4 bg-white/5 font-black text-sm text-yellow-500">القسم {i + 1}: {mod.title}</div>
                                    {(mod.lessons || []).map(lesson => {
                                        const isDone = completedLessons.includes(lesson.id);
                                        const isActive = activeLessonId === lesson.id;
                                        return (
                                            <div key={lesson.id} onClick={() => setActiveLessonId(lesson.id)} className={`p-4 pl-6 cursor-pointer flex items-center gap-3 transition-colors ${isActive ? 'bg-white/10 border-r-4 border-yellow-500' : 'hover:bg-white/5 border-r-4 border-transparent'}`}>
                                                <Icon name={isDone ? 'CheckCircle2' : (lesson.type === 'video' ? 'PlayCircle' : 'HelpCircle')} size={16} className={isDone ? 'text-[#00FF88]' : (isActive ? 'text-yellow-500' : 'text-gray-500')} />
                                                <span className={`text-sm font-bold ${isActive ? 'text-white' : 'text-gray-400'}`}>{lesson.title}</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            );
        };

        // =====================================================================
        // Micro-Frontend 2: Sales Page (صفحة الهبوط للمناهج المشفرة)
        // =====================================================================
        const SalesPageView = ({ course, onBack, onBuy }) => (
            <div className="min-h-screen bg-[#050505] animate-fade-in overflow-y-auto no-scrollbar pb-20" dir="rtl">
                <div className="relative h-[60vh] w-full border-b border-white/10">
                    <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-40" />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#050505] via-[#050505]/80 to-transparent"></div>
                    <button onClick={onBack} className="absolute top-8 right-8 z-20 p-3 bg-white/10 hover:bg-yellow-500 hover:text-black rounded-xl text-white transition-all backdrop-blur-md border border-white/10"><Icon name="ArrowRight" size={24} /></button>
                    
                    <div className="absolute bottom-0 left-0 right-0 p-8 md:p-16 max-w-7xl mx-auto flex flex-col md:flex-row items-end gap-10">
                        <div className="flex-1">
                            <span className="bg-yellow-500 text-black px-4 py-1.5 rounded-lg text-xs font-black uppercase tracking-widest mb-4 inline-block">{course.phase}</span>
                            <h1 className="text-5xl md:text-6xl font-black text-white mb-4 leading-tight">{course.title}</h1>
                            <p className="text-xl text-gray-300 font-medium leading-relaxed max-w-2xl">{course.desc}</p>
                        </div>
                        <div className="bg-black/80 backdrop-blur-xl border border-white/10 p-8 rounded-[2rem] w-full md:w-96 shadow-2xl flex-shrink-0">
                            <div className="flex justify-between items-center mb-6">
                                <span className="text-gray-500 uppercase font-black text-xs">قيمة الاستثمار</span>
                                <span className="text-4xl font-black text-[#00FF88]">${course.price}</span>
                            </div>
                            <ul className="space-y-4 mb-8 text-sm font-bold text-gray-300">
                                <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> وصول مدى الحياة للمحتوى</li>
                                <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> شهادة سيادية معتمدة</li>
                                <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> تفعيل عمولات الإحالة</li>
                            </ul>
                            <button onClick={() => onBuy(course)} className="w-full py-5 rounded-2xl font-black text-lg bg-yellow-500 text-black hover:scale-105 transition-transform flex justify-center items-center gap-3 shadow-[0_10px_30px_rgba(255,215,0,0.3)]"><Icon name="Unlock" size={22} /> فك التشفير</button>
                        </div>
                    </div>
                </div>
                <div className="max-w-7xl mx-auto w-full px-8 py-16">
                    <h3 className="text-2xl font-black mb-8 border-b border-white/10 pb-4">المحتوى الأكاديمي (Curriculum)</h3>
                    <div className="space-y-6">
                        {(!course.curriculum || course.curriculum.length === 0) ? (
                            <div className="text-center py-10 bg-white/5 rounded-xl border border-dashed border-white/10 text-gray-500">يتم تجهيز الفصول الدراسية حالياً.</div>
                        ) : (
                            course.curriculum.map((mod, i) => (
                                <div key={i} className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden">
                                    <div className="bg-white/5 p-5 font-black text-lg flex justify-between items-center">
                                        <span>القسم {i+1}: {mod.title}</span><span className="text-xs text-gray-500">{mod.lessons ? mod.lessons.length : 0} دروس</span>
                                    </div>
                                    <div className="p-2">
                                        {(mod.lessons || []).map((lesson, j) => (
                                            <div key={j} className="flex items-center justify-between p-4 hover:bg-white/5 rounded-xl transition-colors border-b border-white/5 last:border-0">
                                                <div className="flex items-center gap-3"><Icon name={lesson.type === 'video' ? 'PlayCircle' : 'FileText'} size={18} className="text-gray-500" /><span className="font-bold text-sm text-gray-300">{lesson.title}</span></div>
                                                <div>{lesson.isPreview ? <span className="text-[10px] bg-blue-500/20 text-blue-400 px-3 py-1 rounded-md font-black uppercase"><Icon name="Eye" size={12} className="inline mr-1"/> معاينة مجانية</span> : <Icon name="Lock" size={16} className="text-gray-600" />}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        );

        // =====================================================================
        // Micro-Frontend 3: Main Academy App (الواجهة الرئيسية الحاضنة)
        // =====================================================================
        const AppContent = () => {
            const theme = { hex: "#FFD700", btn: "bg-[#FFD700]", btnText: "text-black" }; // Theme fallback
            
            const [selectedCourse, setSelectedCourse] = useState(null);
            const [activeCategory, setActiveCategory] = useState('الكل');
            const [toasts, setToasts] = useState([]);
            
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // قاعدة البيانات المدمجة (Data Store)
            const [coursesDB, setCoursesDB] = useState([
                { 
                    id: 1, phase: 'القيادة', title: 'القيادة التحويلية في العصر الرقمي', hours: 20, price: 299, 
                    img: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800', desc: 'دورة مكثفة لتمكين القادة من قيادة التغيير بفعالية.', locked: false,
                    curriculum: [
                        { id: 101, title: "فهم القيادة التحويلية", lessons: [
                            { id: 1001, title: "مفهوم القيادة وأهميتها", type: "video", isPreview: true },
                            { id: 1002, title: "اختبار الفهم الأول", type: "quiz", question: "ما هي الخاصية الأهم للقائد؟", options: ["الحفاظ على الوضع", "التأثير المثالي"], correct: "التأثير المثالي" }
                        ]}
                    ]
                },
                { 
                    id: 2, phase: 'الاستثمار', title: 'تحليل الأسهم وأسواق المال', hours: 25, price: 499, 
                    img: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800', desc: 'تعلم قراءة وتحليل القوائم المالية للشركات.', locked: true,
                    curriculum: [ { id: 201, title: "مقدمة مالية", lessons: [ { id: 2001, title: "أسواق الأسهم", type: "video", isPreview: true } ] } ]
                },
                { 
                    id: 3, phase: 'تكنولوجيا', title: 'الذكاء الاصطناعي في الأعمال', hours: 15, price: 350, 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', desc: 'استخدام الذكاء الاصطناعي في التسويق.', locked: true, curriculum: []
                },
                { 
                    id: 4, phase: 'ريادة أعمال', title: 'من الفكرة إلى المشروع', hours: 25, price: 399, 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800', desc: 'دراسة الجدوى والتمويل.', locked: true, curriculum: []
                }
            ]);

            // إخفاء الـ Loader بمجرد نجاح رسم المكونات
            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            const handleBuy = (course) => {
                showToast(`تم شراء المنهج '${course.title}' بنجاح!`, 'success');
                setCoursesDB(prev => prev.map(c => c.id === course.id ? {...c, locked: false} : c));
                setSelectedCourse({...course, locked: false}); 
            };

            // Routing Logic
            if (selectedCourse) {
                if (selectedCourse.locked) {
                    return <SalesPageView course={selectedCourse} onBack={() => setSelectedCourse(null)} onBuy={handleBuy} />;
                } else {
                    return <CoursePlayerView course={selectedCourse} onBack={() => setSelectedCourse(null)} theme={theme} showToast={showToast} />;
                }
            }

            // Catalog View (الواجهة الرئيسية)
            return (
                <div className="min-h-screen bg-[#050505] text-white flex flex-col font-['Tajawal'] animate-fade-in" dir="rtl">
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3">
                        {toasts.map(t => (
                            <div key={t.id} className="bg-black/90 border border-[#00FF88]/40 text-[#00FF88] flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl">
                                <Icon name="CheckCircle2" size={20} /> <span className="font-bold text-sm">{t.msg}</span>
                            </div>
                        ))}
                    </div>

                    <div className="max-w-[1600px] mx-auto w-full px-6 md:px-10 py-10">
                        <div className="flex flex-col md:flex-row justify-between items-center mb-10 border-b border-white/10 pb-8">
                            <div className="flex items-center gap-4">
                                <div className="bg-yellow-500 text-black p-3 rounded-2xl"><Icon name="GraduationCap" size={32} /></div>
                                <div><h1 className="text-3xl font-black uppercase tracking-tighter m-0">MR7 <span className="text-yellow-500">ACADEMY</span></h1><p className="text-xs text-gray-500 font-bold uppercase tracking-[0.2em] m-0">100 Days of Sovereignty</p></div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                            {coursesDB.map(course => (
                                <div key={course.id} onClick={() => setSelectedCourse(course)} className="course-card bg-[#0a0a0a] rounded-[2rem] border border-white/10 overflow-hidden cursor-pointer group flex flex-col h-full relative">
                                    <div className="relative h-56 w-full overflow-hidden">
                                        <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                                        <img src={course.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                                        <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity">
                                            {course.locked ? 
                                                <div className="bg-black/80 px-6 py-3 rounded-full border border-white/20 text-white flex items-center gap-2 font-black"><Icon name="Lock" size={20} /> عرض المنهج</div> : 
                                                <div className="bg-[#00FF88] px-6 py-3 rounded-full text-black flex items-center gap-2 font-black"><Icon name="PlayCircle" size={20} /> دخول القاعة</div>
                                            }
                                        </div>
                                    </div>
                                    <div className="p-6 flex flex-col flex-1">
                                        <span className="text-[10px] font-black uppercase tracking-widest mb-3 text-yellow-500">{course.phase}</span>
                                        <h3 className="text-xl font-black mb-3 line-clamp-2 leading-tight">{course.title}</h3>
                                        <p className="text-xs text-gray-500 mb-6 line-clamp-2">{course.desc}</p>
                                        <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
                                            {course.locked ? (
                                                <><span className="text-[10px] text-gray-500 font-bold uppercase">قيمة الاستثمار</span><span className="text-2xl font-black text-[#00FF88]">${course.price}</span></>
                                            ) : (
                                                <div className="w-full"><div className="flex justify-between text-[10px] font-bold mb-1 text-gray-400"><span>التقدم</span><span>0%</span></div><div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden"><div className="h-full bg-yellow-500 w-[0%]"></div></div></div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<AppContent />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات للواجهة ---
components.html(react_html, height=1000, scrolling=True)

# --- 5. أزرار التنقل السريع الخاصة بـ Streamlit ---
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
