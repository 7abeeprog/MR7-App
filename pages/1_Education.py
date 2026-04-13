import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Education Academy", 
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

# --- 3. واجهة React المتقدمة (أكاديمية التريليون - V14.4 - التحديث المستقر) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <!-- استخدام cdnjs بدلاً من unpkg لضمان استقرار التحميل وتجنب حظر المتصفحات -->
    <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
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
        
        .certificate-bg {
            background: linear-gradient(135deg, #111, #000);
            border: 10px solid var(--accent-color);
            padding: 40px;
            position: relative;
            box-shadow: 0 0 50px rgba(255,215,0,0.2) inset;
        }
        .certificate-bg::before {
            content: ''; position: absolute; inset: 5px; border: 2px dashed rgba(255,215,0,0.3); pointer-events: none;
        }

        #loading-screen { position: fixed; inset: 0; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999; }
        
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    </style>

    <!-- درع الأخطاء الصارم (لن تختفي الشاشة إذا وجد خطأ) -->
    <script>
        window.hasGlobalError = false;
        
        function showErrorScreen(title, message, details) {
            window.hasGlobalError = true;
            const loader = document.getElementById('loading-screen');
            if (loader) {
                loader.innerHTML = `
                    <div style="background:rgba(50,0,0,0.9); padding:40px; border:2px solid #FF4B4B; border-radius:20px; z-index:999999; position:relative; max-width:80%; text-align:center; box-shadow:0 0 50px rgba(255,0,0,0.5);">
                        <h2 style="color:#FF4B4B; margin-top:0; font-size:28px;">🚨 ${title}</h2>
                        <p style="color:white; font-size:18px; direction:ltr;">${message}</p>
                        <p style="color:gray; font-size:12px; direction:ltr; margin-top:10px;">${details}</p>
                        <p style="color:#FFD700; margin-top:30px; font-weight:bold;">قم بتصوير هذه الشاشة وإرسالها للمهندس فوراً.</p>
                    </div>`;
                loader.style.opacity = '1';
                loader.style.display = 'flex';
            }
        }

        window.addEventListener('error', function(e) {
            showErrorScreen("انهيار في النظام (System Crash)", e.message, `${e.filename}:${e.lineno}`);
        });

        window.addEventListener('unhandledrejection', function(e) {
            showErrorScreen("فشل في الاتصال (Promise Rejection)", e.reason, "Network or Async Error");
        });

        // إخفاء شاشة التحميل فقط إذا لم يكن هناك أي أخطاء
        setTimeout(() => {
            if (!window.hasGlobalError) {
                const loader = document.getElementById('loading-screen');
                if (loader && loader.style.display !== 'none') {
                    loader.style.opacity = '0';
                    setTimeout(() => loader.style.display = 'none', 500);
                }
            }
        }, 2000);
    </script>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,255,255,0.1); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FFD700; font-weight: 900; letter-spacing: 2px;">MR7 ACADEMY</h2>
    </div>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo, Component } = React;

        // --- درع أخطاء ريأكت الداخلي ---
        class ErrorBoundary extends Component {
            constructor(props) {
                super(props);
                this.state = { hasError: false, error: null, errorInfo: null };
            }
            componentDidCatch(error, errorInfo) {
                this.setState({ hasError: true, error: error, errorInfo: errorInfo });
                window.hasGlobalError = true; // منع اختفاء شاشة التحميل
                const loader = document.getElementById('loading-screen');
                if (loader) {
                    loader.innerHTML = `
                        <div style="background:rgba(50,0,0,0.9); padding:40px; border:2px solid #FF4B4B; border-radius:20px; z-index:999999; position:relative; max-width:80%; text-align:center;">
                            <h2 style="color:#FF4B4B; margin-top:0;">🚨 خطأ داخلي في الواجهة (React Crash)</h2>
                            <p style="color:white; direction:ltr; font-family:monospace;">${error.toString()}</p>
                            <p style="color:gray; font-size:10px; direction:ltr; text-align:left; overflow:auto; max-height:200px;">${errorInfo.componentStack}</p>
                        </div>`;
                    loader.style.opacity = '1';
                    loader.style.display = 'flex';
                }
            }
            render() {
                if (this.state.hasError) return null; 
                return this.props.children;
            }
        }

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

        // --- المكون 1: مشغل الكورس التفاعلي ---
        const CoursePlayer = ({ course, onBack, theme, showToast }) => {
            const firstLessonId = (course.curriculum && course.curriculum[0] && course.curriculum[0].lessons && course.curriculum[0].lessons[0]) ? course.curriculum[0].lessons[0].id : null;
            const [activeLessonId, setActiveLessonId] = useState(firstLessonId);
            const [completedLessons, setCompletedLessons] = useState([]);
            const [quizAnswers, setQuizAnswers] = useState({});
            const [showCertificate, setShowCertificate] = useState(false);

            let currentLesson = null;
            let currentModule = null;
            if (course.curriculum) {
                course.curriculum.forEach(mod => {
                    if (mod.lessons) {
                        const lesson = mod.lessons.find(l => l.id === activeLessonId);
                        if(lesson) { currentLesson = lesson; currentModule = mod; }
                    }
                });
            }

            const handleComplete = (lessonId, isQuiz = false, isCorrect = false) => {
                if (isQuiz && !isCorrect) {
                    showToast('إجابة خاطئة، القائد الحقيقي يتعلم من أخطائه. أعد المحاولة!', 'error');
                    return;
                }
                
                if (!completedLessons.includes(lessonId)) {
                    setCompletedLessons([...completedLessons, lessonId]);
                    if(isQuiz) showToast('إجابة صحيحة! +50 XP 🪙', 'success');
                    else showToast('تم إنجاز الدرس! +20 XP 🪙', 'success');
                }

                let foundCurrent = false;
                let nextLessonId = null;
                if (course.curriculum) {
                    for (const mod of course.curriculum) {
                        if (!mod.lessons) continue;
                        for (const l of mod.lessons) {
                            if (foundCurrent) { nextLessonId = l.id; break; }
                            if (l.id === lessonId) foundCurrent = true;
                        }
                        if (nextLessonId) break;
                    }
                }

                if (nextLessonId) {
                    setActiveLessonId(nextLessonId);
                } else {
                    showToast('أكملت المنهج بنجاح! +1000 XP 🏆', 'success');
                    setShowCertificate(true);
                }
            };

            const totalLessonsCount = course.curriculum ? course.curriculum.reduce((acc, mod) => acc + (mod.lessons ? mod.lessons.length : 0), 0) : 0;
            const progressPercent = totalLessonsCount === 0 ? 0 : (completedLessons.length / totalLessonsCount) * 100;

            if (showCertificate) {
                return (
                    <div className="min-h-screen bg-[#050505] flex flex-col items-center justify-center p-8 animate-fade-in" dir="rtl">
                        <div className="certificate-bg w-full max-w-4xl text-center rounded-xl bg-black">
                            <Icon name="Award" size={80} className="mx-auto mb-6 text-yellow-500" />
                            <h1 className="text-5xl font-black text-white mb-2 tracking-widest">شهادة إتمام سيادية</h1>
                            <p className="text-xl text-yellow-500 font-bold mb-8">إمبراطورية MR7 تشهد بأن</p>
                            <h2 className="text-4xl font-black text-white mb-8 border-b-2 border-white/20 pb-4 inline-block px-10">القائد الاستراتيجي</h2>
                            <p className="text-2xl text-gray-300 mb-4">قد أتم بنجاح متطلبات المنهج المكثف:</p>
                            <h3 className="text-3xl font-black text-[#00FF88] mb-10">{course.title}</h3>
                            <div className="flex justify-between items-center px-10 text-gray-500 font-bold text-sm">
                                <div>تاريخ الإصدار: {new Date().toLocaleDateString()}</div>
                                <div>رقم التوثيق: MR7-{Math.floor(Math.random()*1000000)}</div>
                                <div>الاعتماد: الإدارة العليا</div>
                            </div>
                        </div>
                        <button onClick={onBack} className="mt-10 px-8 py-4 bg-white/10 hover:bg-white/20 text-white rounded-xl font-black transition-colors flex items-center gap-2 border border-white/20">
                            <Icon name="ArrowRight" size={20} /> العودة للأكاديمية
                        </button>
                    </div>
                );
            }

            return (
                <div className="min-h-screen bg-[#050505] flex flex-col animate-fade-in" dir="rtl">
                    <nav className="glass-panel border-b border-white/10 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
                        <div className="flex items-center gap-6">
                            <button onClick={onBack} className="flex items-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-2.5 rounded-xl font-bold text-gray-300 hover:text-white transition-all">
                                <Icon name="ArrowRight" size={18} /> العودة للأكاديمية
                            </button>
                            <div className="h-8 w-px bg-white/10"></div>
                            <div>
                                <span className="text-[10px] uppercase font-black tracking-widest text-gray-500 block mb-0.5">{course.phase}</span>
                                <h2 className="text-lg font-black text-white">{course.title}</h2>
                            </div>
                        </div>
                        <div className="text-left">
                            <span className="text-[10px] text-gray-500 font-bold uppercase block mb-1">التقدم الكلي</span>
                            <div className="w-32 h-1.5 bg-white/10 rounded-full overflow-hidden">
                                <div className="h-full" style={{width: `${progressPercent}%`, backgroundColor: theme.hex}}></div>
                            </div>
                        </div>
                    </nav>

                    <div className="flex flex-1 overflow-hidden h-[calc(100vh-80px)]">
                        <div className="flex-1 flex flex-col bg-black overflow-y-auto no-scrollbar relative">
                            {!currentLesson ? (
                                <div className="p-12 text-center text-gray-500 flex flex-col items-center justify-center h-full">
                                    <Icon name="BookOpen" size={60} className="mb-4 opacity-50"/>
                                    <h2 className="text-2xl font-black">المحتوى قيد التجهيز</h2>
                                    <p>سيتم توفير دروس هذا المنهج قريباً.</p>
                                </div>
                            ) : (
                                <>
                                    {currentLesson.type === 'video' && (
                                        <div className="w-full aspect-video bg-[#111] border-b border-white/5 flex items-center justify-center relative">
                                            <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-20" />
                                            <div className="z-10 text-center">
                                                <button className="w-20 h-20 bg-yellow-500 hover:bg-yellow-400 text-black rounded-full flex items-center justify-center transition-all hover:scale-110 shadow-[0_0_30px_rgba(255,215,0,0.4)] mb-4 mx-auto">
                                                    <Icon name="Play" size={30} className="ml-2" />
                                                </button>
                                                <p className="font-bold text-gray-400">فيديو: {currentLesson.title}</p>
                                            </div>
                                        </div>
                                    )}

                                    <div className="p-8 md:p-12 max-w-4xl mx-auto w-full">
                                        <h1 className="text-3xl font-black mb-4">{currentLesson.title}</h1>
                                        
                                        {currentLesson.type === 'quiz' ? (
                                            <div className="bg-white/5 border border-white/10 p-8 rounded-2xl">
                                                <h3 className="text-xl font-bold mb-6 text-yellow-500"><Icon name="HelpCircle" className="inline mr-2"/> سؤال تقييمي:</h3>
                                                <p className="text-lg mb-6">{currentLesson.question}</p>
                                                <div className="space-y-3">
                                                    {currentLesson.options && currentLesson.options.map((opt, i) => (
                                                        <button 
                                                            key={i}
                                                            onClick={() => setQuizAnswers({...quizAnswers, [currentLesson.id]: opt})}
                                                            className={`w-full text-right p-4 rounded-xl font-bold border transition-all ${quizAnswers[currentLesson.id] === opt ? 'bg-yellow-500/20 border-yellow-500 text-white' : 'bg-black border-white/10 text-gray-400 hover:border-white/30'}`}
                                                        >
                                                            {opt}
                                                        </button>
                                                    ))}
                                                </div>
                                                <button 
                                                    onClick={() => handleComplete(currentLesson.id, true, quizAnswers[currentLesson.id] === currentLesson.correct)}
                                                    disabled={!quizAnswers[currentLesson.id]}
                                                    className="mt-8 w-full py-4 bg-yellow-500 text-black font-black rounded-xl disabled:opacity-50"
                                                >
                                                    تأكيد الإجابة
                                                </button>
                                            </div>
                                        ) : (
                                            <div>
                                                <div className="text-gray-300 leading-relaxed text-lg mb-8" dangerouslySetInnerHTML={{__html: currentLesson.content || ''}}></div>
                                                <button 
                                                    onClick={() => handleComplete(currentLesson.id)}
                                                    className="w-full py-4 bg-[#00FF88] hover:bg-[#00cc66] text-black font-black rounded-xl transition-colors shadow-[0_0_20px_rgba(0,255,136,0.2)]"
                                                >
                                                    إتمام الدرس والانتقال للتالي <Icon name="CheckCircle2" className="inline ml-2" size={20}/>
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </>
                            )}
                        </div>

                        {/* Sidebar Curriculum */}
                        <div className="w-80 bg-[#0a0a0a] border-r border-white/10 flex flex-col hidden lg:flex h-full overflow-y-auto no-scrollbar">
                            <div className="p-6 border-b border-white/5">
                                <h3 className="font-black text-lg mb-1">محتوى المنهج</h3>
                            </div>
                            <div className="flex flex-col">
                                {course.curriculum && course.curriculum.map((mod, mIdx) => (
                                    <div key={mod.id || mIdx} className="border-b border-white/5">
                                        <div className="p-4 bg-white/5 font-black text-sm text-yellow-500">
                                            القسم {mIdx + 1}: {mod.title}
                                        </div>
                                        {mod.lessons && mod.lessons.map(lesson => {
                                            const iconName = completedLessons.includes(lesson.id) ? 'CheckCircle2' : (lesson.type === 'video' ? 'PlayCircle' : lesson.type === 'quiz' ? 'HelpCircle' : 'FileText');
                                            const iconColor = completedLessons.includes(lesson.id) ? 'text-[#00FF88]' : (activeLessonId === lesson.id ? 'text-yellow-500' : 'text-gray-500');
                                            
                                            return (
                                                <div 
                                                    key={lesson.id} 
                                                    onClick={() => setActiveLessonId(lesson.id)}
                                                    className={`p-4 pl-6 cursor-pointer flex items-center gap-3 transition-colors ${activeLessonId === lesson.id ? 'bg-white/10 border-r-4 border-yellow-500' : 'hover:bg-white/5 border-r-4 border-transparent'}`}
                                                >
                                                    <Icon name={iconName} size={16} className={iconColor} />
                                                    <span className={`text-sm font-bold ${activeLessonId === lesson.id ? 'text-white' : 'text-gray-400'}`}>{lesson.title}</span>
                                                </div>
                                            )
                                        })}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        // --- المكون 2: صفحة الهبوط (Sales Page) ---
        const CourseSalesPage = ({ course, onBack, theme, onBuy, showToast }) => {
            return (
                <div className="min-h-screen bg-[#050505] animate-fade-in overflow-y-auto no-scrollbar pb-20" dir="rtl">
                    <div className="relative h-[60vh] w-full border-b border-white/10">
                        <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-40" />
                        <div className="absolute inset-0 bg-gradient-to-t from-[#050505] via-[#050505]/60 to-transparent"></div>
                        
                        <div className="absolute top-6 left-6 right-6 flex justify-between items-center z-10 max-w-[1400px] mx-auto w-full">
                            <button onClick={onBack} className="p-3 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-xl text-white transition-colors border border-white/10">
                                <Icon name="ArrowRight" size={24} />
                            </button>
                        </div>

                        <div className="absolute bottom-0 left-0 right-0 p-8 md:p-16 max-w-[1400px] mx-auto w-full flex flex-col md:flex-row gap-10 items-end">
                            <div className="flex-1">
                                <span className="bg-yellow-500/20 text-yellow-500 border border-yellow-500/30 px-4 py-1.5 rounded-lg text-xs font-black uppercase tracking-widest mb-4 inline-block">{course.phase}</span>
                                <h1 className="text-4xl md:text-6xl font-black text-white mb-4 leading-tight">{course.title}</h1>
                                <p className="text-xl text-gray-300 max-w-2xl font-medium leading-relaxed">{course.desc}</p>
                            </div>
                            
                            <div className="bg-black/80 backdrop-blur-xl border border-white/10 p-8 rounded-[2rem] w-full md:w-96 shadow-2xl flex-shrink-0">
                                <div className="flex justify-between items-center mb-6">
                                    <span className="text-gray-500 uppercase font-black text-xs tracking-widest">قيمة الاستثمار</span>
                                    <span className="text-4xl font-black text-[#00FF88]">${course.price}</span>
                                </div>
                                <ul className="space-y-4 mb-8 text-sm font-bold text-gray-300">
                                    <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> وصول مدى الحياة للمحتوى</li>
                                    <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> شهادة سيادية معتمدة</li>
                                    <li className="flex items-center gap-3"><Icon name="Check" size={18} className="text-yellow-500"/> تفعيل عمولات التسويق (10-5-1%)</li>
                                </ul>
                                <button onClick={() => onBuy(course)} className={`w-full py-5 rounded-2xl font-black text-lg ${theme.btn} ${theme.btnText} hover:scale-105 transition-transform flex justify-center items-center gap-3 shadow-[0_10px_30px_rgba(255,215,0,0.3)]`}>
                                    <Icon name="Unlock" size={22} /> فك تشفير المنهج
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="max-w-[1400px] mx-auto w-full px-8 md:px-16 py-16 flex flex-col lg:flex-row gap-16">
                        <div className="w-full lg:w-1/3 space-y-10">
                            <div>
                                <h3 className="text-xl font-black mb-6 border-b border-white/10 pb-4">المدرب / المهندس الاستراتيجي</h3>
                                <div className="flex items-center gap-4 bg-white/5 p-4 rounded-2xl border border-white/5">
                                    <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center text-2xl">👤</div>
                                    <div>
                                        <h4 className="font-black text-lg">{course.instructor || 'أكاديمية MR7'}</h4>
                                        <p className="text-xs text-yellow-500 font-bold uppercase">{course.instructor_title || 'خبير استراتيجي'}</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div>
                                <h3 className="text-xl font-black mb-6 border-b border-white/10 pb-4">ماذا ستتعلم؟</h3>
                                <ul className="space-y-4 text-gray-400 font-medium">
                                    <li className="flex items-start gap-3"><Icon name="Target" size={20} className="text-[#00FF88] mt-1 shrink-0"/> إتقان استراتيجيات التحول والتضاعف في بيئة عدم اليقين.</li>
                                    <li className="flex items-start gap-3"><Icon name="Target" size={20} className="text-[#00FF88] mt-1 shrink-0"/> بناء رؤية مؤسسية وتوصيلها بفعالية لجيشك.</li>
                                    <li className="flex items-start gap-3"><Icon name="Target" size={20} className="text-[#00FF88] mt-1 shrink-0"/> فهم سيكولوجية الجماهير لتحفيز المبيعات.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="w-full lg:w-2/3">
                            <h3 className="text-2xl font-black mb-8 border-b border-white/10 pb-4">المحتوى الأكاديمي (Curriculum)</h3>
                            <div className="space-y-6">
                                {!course.curriculum || course.curriculum.length === 0 ? (
                                    <div className="text-center py-10 bg-white/5 rounded-xl border border-dashed border-white/10 text-gray-500">
                                        يتم تجهيز الفصول الدراسية حالياً.
                                    </div>
                                ) : (
                                    course.curriculum.map((mod, i) => (
                                        <div key={i} className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden">
                                            <div className="bg-white/5 p-5 font-black text-lg flex justify-between items-center">
                                                <span>القسم {i+1}: {mod.title}</span>
                                                <span className="text-xs text-gray-500">{mod.lessons ? mod.lessons.length : 0} دروس</span>
                                            </div>
                                            <div className="p-2">
                                                {mod.lessons && mod.lessons.map((lesson, j) => {
                                                    const iName = lesson.type === 'video' ? 'PlayCircle' : lesson.type === 'quiz' ? 'HelpCircle' : 'FileText';
                                                    return (
                                                        <div key={j} className="flex items-center justify-between p-4 hover:bg-white/5 rounded-xl transition-colors border-b border-white/5 last:border-0">
                                                            <div className="flex items-center gap-3">
                                                                <Icon name={iName} size={18} className="text-gray-500" />
                                                                <span className="font-bold text-sm text-gray-300">{lesson.title}</span>
                                                            </div>
                                                            <div className="flex items-center gap-3">
                                                                {lesson.isPreview ? (
                                                                    <button onClick={() => showToast('هذا الدرس متاح للمعاينة! سيتم فتحه في المشغل.', 'info')} className="text-[10px] bg-blue-500/20 text-blue-400 px-3 py-1 rounded-md font-black uppercase flex items-center gap-1"><Icon name="Eye" size={12}/> معاينة مجانية</button>
                                                                ) : (
                                                                    <Icon name="Lock" size={16} className="text-gray-600" />
                                                                )}
                                                            </div>
                                                        </div>
                                                    )
                                                })}
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        const AppContent = () => {
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
            const [selectedCourse, setSelectedCourse] = useState(null); 
            const [searchQ, setSearchQ] = useState('');
            const [selectedCategory, setSelectedCategory] = useState('الكل');
            const [toasts, setToasts] = useState([]);
            
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            const [coursesDB, setCoursesDB] = useState([
                { 
                    id: 1, phase: 'القيادة والإدارة الاستراتيجية', title: 'القيادة التحويلية في العصر الرقمي', hours: 20, price: 299, 
                    img: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800', 
                    desc: 'دورة مكثفة تهدف إلى تمكين القادة من قيادة التغيير بفعالية في بيئة رقمية سريعة التطور، وتحفيز فرق العمل لتحقيق رؤى طموحة.', 
                    locked: false, progress: 0,
                    instructor: "د. خالد السيادي", instructor_title: "خبير القيادة المؤسسية",
                    curriculum: [
                        {
                            id: 101, title: "فهم القيادة التحويلية",
                            lessons: [
                                { id: 1001, title: "مفهوم القيادة التحويلية وأهميتها", type: "video", content: "<p>في هذا الدرس نتناول كيف يختلف القائد التحويلي عن القائد التقليدي...</p>", isPreview: true },
                                { id: 1002, title: "اختبار الفهم الأول", type: "quiz", question: "ما هي الخاصية الأهم للقائد التحويلي؟", options: ["الحفاظ على الوضع الراهن", "التأثير المثالي والتحفيز الملهم", "إدارة الميزانيات بدقة"], correct: "التأثير المثالي والتحفيز الملهم", isPreview: true },
                                { id: 1003, title: "خصائص القائد التحويلي المتقدمة", type: "text", content: "<p>الرؤية، التأثير، التحفيز الفكري، والاعتبار الفردي...</p>" },
                            ]
                        },
                        {
                            id: 102, title: "بناء الرؤية المشتركة",
                            lessons: [
                                { id: 2001, title: "كيفية صياغة رؤية واضحة", type: "video", content: "<p>تعلم صياغة رؤية قابلة للقياس...</p>" },
                                { id: 2002, title: "تقنيات توصيل الرؤية بفعالية", type: "text", content: "<p>استراتيجيات التواصل مع أصحاب المصلحة...</p>" },
                                { id: 2003, title: "اختبار القسم الثاني", type: "quiz", question: "ما هو الهدف من توصيل الرؤية؟", options: ["بناء الالتزام وتحويلها لأهداف", "إرضاء الإدارة العليا فقط"], correct: "بناء الالتزام وتحويلها لأهداف" },
                            ]
                        },
                        {
                            id: 103, title: "التقييم النهائي والاعتماد",
                            lessons: [
                                { id: 3001, title: "الاختبار الاستراتيجي الشامل", type: "quiz", question: "كيف نتعامل مع مقاومة التغيير؟", options: ["بالتجاهل", "بالقوة", "ببناء ثقافة الثقة والتعاون"], correct: "ببناء ثقافة الثقة والتعاون" }
                            ]
                        }
                    ]
                },
                { 
                    id: 2, phase: 'الاستثمار والمالية', title: 'تحليل الأسهم وأسواق المال', hours: 25, price: 499, 
                    img: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800', 
                    desc: 'تعلم قراءة وتحليل القوائم المالية للشركات (الدخل، الميزانية، التدفقات النقدية) واستخدام النسب المالية للتنبؤ المالي واتخاذ القرارات.', 
                    locked: true, progress: 0,
                    instructor: "عمار المالي", instructor_title: "محلل مالي معتمد",
                    curriculum: [
                        {
                            id: 201, title: "مقدمة في أسواق الأسهم",
                            lessons: [
                                { id: 2001, title: "هيكل سوق الأسهم والبورصات", type: "video", isPreview: true },
                                { id: 2002, title: "أنواع الأسهم ومفاهيمها", type: "text" },
                            ]
                        },
                        {
                            id: 202, title: "التحليل الأساسي للأسهم",
                            lessons: [
                                { id: 2003, title: "قراءة القوائم المالية", type: "video" },
                                { id: 2004, title: "نماذج التقييم (خصم الأرباح)", type: "text" },
                            ]
                        }
                    ]
                },
                { 
                    id: 3, phase: 'التكنولوجيا والتحول', title: 'الذكاء الاصطناعي في الأعمال', hours: 15, price: 350, 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', 
                    desc: 'استخدام AI في التسويق والمالية وخدمة العملاء.', 
                    locked: true, progress: 0, instructor: "نور الدين تقني", instructor_title: "مهندس ذكاء اصطناعي", 
                    curriculum: [{id:1, title: "المقدمة", lessons:[{id:1, title:"ما هو الـ AI", type:"video", isPreview:true}]}] 
                },
                { 
                    id: 4, phase: 'ريادة الأعمال', title: 'من الفكرة إلى المشروع الشامل', hours: 25, price: 399, 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800', 
                    desc: 'نموذج العمل، دراسة الجدوى، والتمويل الأولي.', 
                    locked: true, progress: 0, instructor: 'خبير مجهول', instructor_title: 'مدرب', 
                    curriculum: [] 
                },
                { 
                    id: 5, phase: 'المهارات الشخصية', title: 'الذكاء العاطفي في بيئة العمل', hours: 14, price: 150, 
                    img: 'https://images.unsplash.com/photo-1552581234-26160f608093?w=800', 
                    desc: 'الوعي الذاتي، إدارة العلاقات، والتأثير الإيجابي.', 
                    locked: true, progress: 0, instructor: 'خبير مجهول', instructor_title: 'مدرب', 
                    curriculum: [] 
                },
                { 
                    id: 6, phase: 'الاقتصاد المستدام', title: 'الاستثمار في الطاقة المتجددة', hours: 16, price: 450, 
                    img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=800', 
                    desc: 'السندات الخضراء، طاقة الرياح، والتمويل المستدام.', 
                    locked: true, progress: 0, instructor: 'خبير مجهول', instructor_title: 'مدرب', 
                    curriculum: [] 
                },
            ];

            const categories = ["الكل", ...new Set(coursesDB.map(c => c.phase))];

            const filteredCourses = useMemo(() => {
                return coursesDB.filter(c => {
                    const matchSearch = c.title.includes(searchQ) || c.desc.includes(searchQ);
                    const matchCat = selectedCategory === 'الكل' || c.phase === selectedCategory;
                    return matchSearch && matchCat;
                });
            }, [searchQ, selectedCategory, coursesDB]);

            const handleBuyCourse = (course) => {
                showToast(`تم شراء المنهج '${course.title}' بنجاح! تم الخصم من محفظتك.`, 'success');
                setCoursesDB(prev => prev.map(c => c.id === course.id ? {...c, locked: false} : c));
                setSelectedCourse({...course, locked: false}); 
            };

            if (selectedCourse) {
                if (selectedCourse.locked) {
                    return <CourseSalesPage course={selectedCourse} onBack={() => setSelectedCourse(null)} theme={theme} onBuy={handleBuyCourse} showToast={showToast} />;
                } else {
                    return <CoursePlayer course={selectedCourse} onBack={() => setSelectedCourse(null)} theme={theme} showToast={showToast} />;
                }
            }

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col font-['Tajawal']`} dir="rtl">
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'error' ? 'bg-black/90 border-red-500/40 text-red-500' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : t.type === 'error' ? 'XCircle' : 'AlertCircle'} size={20} />
                                <span className="font-bold text-sm text-white">{t.msg}</span>
                            </div>
                        ))}
                    </div>

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

                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                                    {filteredCourses.map(course => {
                                        const lessonCount = course.curriculum ? course.curriculum.reduce((acc, mod) => acc + (mod.lessons ? mod.lessons.length : 0), 0) : 0;
                                        
                                        return (
                                        <div key={course.id} onClick={() => setSelectedCourse(course)} className="course-card rounded-[2rem] border border-white/10 overflow-hidden cursor-pointer group flex flex-col h-full relative bg-[#0a0a0a]">
                                            <div className="relative h-56 w-full overflow-hidden">
                                                <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                                                <img src={course.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                                                {course.locked && (
                                                    <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity">
                                                        <div className="bg-black/80 px-6 py-3 rounded-full border border-white/20 text-white flex items-center gap-2 font-black"><Icon name="Lock" size={20} /> عرض المنهج</div>
                                                    </div>
                                                )}
                                                {!course.locked && (
                                                    <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity">
                                                        <div className="bg-[#00FF88] px-6 py-3 rounded-full text-black flex items-center gap-2 font-black"><Icon name="PlayCircle" size={20} /> دخول القاعة</div>
                                                    </div>
                                                )}
                                            </div>
                                            
                                            <div className="p-6 flex flex-col flex-1">
                                                <span className="text-[10px] font-black uppercase tracking-widest mb-3" style={{color: theme.hex}}>{course.phase}</span>
                                                <h3 className="text-xl font-black mb-3 line-clamp-2 text-white leading-tight">{course.title}</h3>
                                                <div className="flex items-center gap-4 text-xs font-bold text-gray-500 mb-6">
                                                    <span className="flex items-center gap-1"><Icon name="Clock" size={14}/> {course.hours} ساعة</span>
                                                    <span className="flex items-center gap-1"><Icon name="BookOpen" size={14}/> {lessonCount} درس</span>
                                                </div>
                                                
                                                <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
                                                    {course.locked ? (
                                                        <div className="flex justify-between items-center w-full">
                                                          <span className="text-[10px] text-gray-500 font-bold uppercase">قيمة الاستثمار</span>
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
                                    )})}
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
                                   {coursesDB.filter(c => !c.locked).map(course => (
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
