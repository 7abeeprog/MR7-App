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

# --- 3. واجهة React المتقدمة (أكاديمية التريليون V15.0 - الجيمفيكيشن والربط السحابي) ---
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
    
    <!-- إدراج دوال Firebase الضرورية للربط السحابي (doc, setDoc, getDoc) -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getFirestore, collection, onSnapshot, query, where, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        window.firebaseModules = { initializeApp, getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, getFirestore, collection, onSnapshot, query, where, doc, setDoc, getDoc };
    </script>

    <style>
        body { font-family: 'Tajawal', sans-serif; margin: 0; overflow-x: hidden; scroll-behavior: smooth; background-color: #020202; color: white; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 30px 60px rgba(0,0,0,0.6); }
        .course-card { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); background: linear-gradient(180deg, rgba(20,20,20,0.9) 0%, rgba(5,5,5,1) 100%); }
        .course-card:hover { transform: translateY(-10px) scale(1.02); z-index: 10; box-shadow: 0 20px 40px rgba(0,0,0,0.8); border-color: var(--accent-color); }
        .premium-input { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); color: white; transition: all 0.3s ease; }
        .premium-input:focus { outline: none; border-color: var(--accent-color); box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1); }
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .animate-pop { animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes popIn { 0% { opacity: 0; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1); } }

        .certificate-bg {
            background: linear-gradient(135deg, #111, #000); border: 10px solid var(--accent-color); padding: 40px; position: relative;
            box-shadow: 0 0 50px rgba(255,215,0,0.2) inset;
        }
        .certificate-bg::before { content: ''; position: absolute; inset: 5px; border: 2px dashed rgba(255,215,0,0.3); pointer-events: none; }

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
        <div style="border: 4px solid rgba(255,255,255,0.1); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FFD700; font-weight: 900; letter-spacing: 2px;">MR7 ACADEMY</h2>
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

        // --- محرك الصوت للصدمات الإيجابية (Gamification Audio) ---
        const playSound = (type) => {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                
                if (type === 'success') {
                    // صوت احتفالي متصاعد (Tada)
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
                    osc.frequency.exponentialRampToValueAtTime(1046.50, ctx.currentTime + 0.15); // C6
                    gain.gain.setValueAtTime(0.1, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                    osc.start(); osc.stop(ctx.currentTime + 0.5);
                } else if (type === 'error') {
                    // صوت تنبيه منخفض (Buzzer)
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, ctx.currentTime);
                    gain.gain.setValueAtTime(0.1, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                    osc.start(); osc.stop(ctx.currentTime + 0.3);
                }
            } catch(e) { console.log("Audio not supported or blocked"); }
        };

        // =====================================================================
        // Micro-Frontend 1: Course Player (مشغل الكورس المتكامل LMS)
        // =====================================================================
        const CoursePlayerView = ({ course, onBack, theme, showToast, user, dbInstance, appId }) => {
            const [activeLessonId, setActiveLessonId] = useState(null);
            const [completedLessons, setCompletedLessons] = useState([]);
            const [quizState, setQuizState] = useState({}); // { lessonId: 'idle' | 'passed' | 'failed' }
            const [showCertificate, setShowCertificate] = useState(false);
            const [isLoadingProgress, setIsLoadingProgress] = useState(true);

            // جلب التقدم السحابي عند فتح الكورس
            useEffect(() => {
                const fetchProgress = async () => {
                    if (user && dbInstance && window.firebaseModules) {
                        try {
                            const { doc, getDoc } = window.firebaseModules;
                            const docRef = doc(dbInstance, 'artifacts', appId, 'users', user.uid, 'education_progress', course.id.toString());
                            const docSnap = await getDoc(docRef);
                            if (docSnap.exists()) {
                                const data = docSnap.data();
                                setCompletedLessons(data.completed || []);
                            }
                        } catch (e) { console.warn("Could not fetch progress:", e); }
                    }
                    setIsLoadingProgress(false);
                };
                fetchProgress();
            }, [user, dbInstance, course.id, appId]);

            // تحديد الدرس الأول أو آخر درس غير مكتمل
            useEffect(() => {
                if (!isLoadingProgress && !activeLessonId && course.curriculum) {
                    let targetLesson = null;
                    for (const mod of course.curriculum) {
                        for (const l of mod.lessons) {
                            if (!completedLessons.includes(l.id)) {
                                targetLesson = l.id; break;
                            }
                        }
                        if (targetLesson) break;
                    }
                    if (!targetLesson && course.curriculum[0]?.lessons[0]) {
                        targetLesson = course.curriculum[0].lessons[0].id; // لو كله خلص، افتح أول درس
                    }
                    setActiveLessonId(targetLesson);
                }
            }, [isLoadingProgress, completedLessons, course.curriculum, activeLessonId]);

            const currentLesson = useMemo(() => {
                for (const mod of (course.curriculum || [])) {
                    const l = mod.lessons.find(x => x.id === activeLessonId);
                    if (l) return l;
                }
                return null;
            }, [activeLessonId, course.curriculum]);

            const flatLessons = useMemo(() => {
                let all = [];
                (course.curriculum || []).forEach(mod => all.push(...mod.lessons));
                return all;
            }, [course.curriculum]);

            // دالة إنهاء الدرس والربط السحابي
            const markLessonComplete = async (lessonId) => {
                let newCompleted = [...completedLessons];
                if (!newCompleted.includes(lessonId)) {
                    newCompleted.push(lessonId);
                    setCompletedLessons(newCompleted);
                    
                    // الحفظ السحابي
                    if (user && dbInstance && window.firebaseModules) {
                        try {
                            const { doc, setDoc } = window.firebaseModules;
                            const docRef = doc(dbInstance, 'artifacts', appId, 'users', user.uid, 'education_progress', course.id.toString());
                            await setDoc(docRef, { completed: newCompleted, lastUpdated: new Date().toISOString() }, { merge: true });
                        } catch (e) { console.warn("Failed to save progress:", e); }
                    }
                }
                return newCompleted;
            };

            const handleNextLesson = async () => {
                const newCompleted = await markLessonComplete(activeLessonId);
                
                const currentIndex = flatLessons.findIndex(l => l.id === activeLessonId);
                if (currentIndex >= 0 && currentIndex < flatLessons.length - 1) {
                    setActiveLessonId(flatLessons[currentIndex + 1].id);
                } else {
                    // تم إنهاء كل الدروس
                    playSound('success');
                    setShowCertificate(true);
                }
            };

            const handleQuizAnswer = async (selectedOption) => {
                if (selectedOption === currentLesson.correct) {
                    playSound('success');
                    setQuizState({...quizState, [currentLesson.id]: 'passed'});
                    showToast('إجابة عبقرية! +50 نقطة سيادة 🌟', 'success');
                    await markLessonComplete(currentLesson.id);
                } else {
                    playSound('error');
                    setQuizState({...quizState, [currentLesson.id]: 'failed'});
                    showToast('القائد يدرس أخطاءه. أعد المحاولة!', 'error');
                    setTimeout(() => setQuizState({...quizState, [currentLesson.id]: 'idle'}), 2000);
                }
            };

            const progress = flatLessons.length === 0 ? 0 : (completedLessons.length / flatLessons.length) * 100;

            if (isLoadingProgress) return <div className="min-h-screen bg-[#050505] flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#FFD700]"></div></div>;

            if (showCertificate) {
                return (
                    <div className="min-h-screen bg-[#050505] flex flex-col items-center justify-center p-8 animate-fade-in" dir="rtl">
                        <div className="certificate-bg w-full max-w-4xl text-center rounded-xl bg-black">
                            <Icon name="Award" size={80} className="mx-auto mb-6 text-yellow-500" />
                            <h1 className="text-5xl font-black text-white mb-2 tracking-widest">شهادة إنجاز سيادية</h1>
                            <p className="text-xl text-yellow-500 font-bold mb-8">أكاديمية MR7 تشهد بأن</p>
                            <h2 className="text-4xl font-black text-white mb-8 border-b-2 border-white/20 pb-4 inline-block px-10">القائد الاستراتيجي</h2>
                            <p className="text-2xl text-gray-300 mb-4">قد أتم بنجاح متطلبات رحلة الـ 100 يوم في:</p>
                            <h3 className="text-3xl font-black text-[#00FF88] mb-10">{course.title}</h3>
                            <div className="flex justify-between items-center px-10 text-gray-500 font-bold text-sm">
                                <div>تاريخ الاعتماد: {new Date().toLocaleDateString()}</div>
                                <div>رقم الوثيقة: MR7-{course.id}-{Math.floor(Math.random()*10000)}</div>
                                <div>الاعتماد: الإدارة العليا</div>
                            </div>
                        </div>
                        <button onClick={onBack} className="mt-10 px-8 py-4 bg-white/10 hover:bg-white/20 text-white rounded-xl font-black transition-colors flex items-center gap-2 border border-white/20">
                            <Icon name="ArrowRight" size={20} /> العودة لمركز القيادة
                        </button>
                    </div>
                );
            }

            return (
                <div className="min-h-screen flex flex-col animate-fade-in bg-[#050505]" dir="rtl">
                    <nav className="glass-panel border-b border-white/10 px-8 py-4 flex items-center justify-between z-50">
                        <div className="flex items-center gap-6">
                            <button onClick={onBack} className="flex items-center gap-2 bg-white/5 hover:bg-white/10 px-4 py-2 rounded-xl font-bold transition-all border border-white/10 text-sm"><Icon name="ArrowRight" size={16} /> خروج</button>
                            <div>
                                <span className="text-[10px] text-yellow-500 font-black uppercase tracking-widest">{course.phase}</span>
                                <h2 className="text-lg font-black text-white">{course.title}</h2>
                            </div>
                        </div>
                        <div className="w-48">
                            <div className="flex justify-between text-[10px] font-bold mb-1 text-gray-400"><span>التقدم</span><span>{progress.toFixed(0)}%</span></div>
                            <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden"><div className="h-full bg-[#00FF88] transition-all duration-1000" style={{width: `${progress}%`}}></div></div>
                        </div>
                    </nav>

                    <div className="flex flex-1 overflow-hidden h-[calc(100vh-76px)]">
                        {/* مساحة العرض (Player/Content) */}
                        <div className="flex-1 overflow-y-auto no-scrollbar bg-black relative flex flex-col">
                            {currentLesson ? (
                                <div className="flex-1 flex flex-col">
                                    {currentLesson.type === 'video' && (
                                        <div className="w-full aspect-video bg-[#111] relative flex items-center justify-center border-b border-white/10 shrink-0">
                                            <img src={course.img} className="absolute inset-0 w-full h-full object-cover opacity-30" />
                                            <div className="z-10 bg-yellow-500 w-20 h-20 rounded-full flex items-center justify-center text-black cursor-pointer hover:scale-110 transition-transform shadow-[0_0_30px_rgba(255,215,0,0.4)]"><Icon name="Play" size={30} className="ml-2"/></div>
                                        </div>
                                    )}
                                    
                                    <div className="max-w-4xl mx-auto p-10 w-full flex-1 flex flex-col">
                                        <h1 className="text-3xl font-black mb-2">{currentLesson.title}</h1>
                                        <p className="text-gray-500 text-sm font-bold mb-8 flex items-center gap-2"><Icon name="Clock" size={14}/> الوقت المقدر: {currentLesson.duration || '10 دقائق'}</p>

                                        {currentLesson.type === 'quiz' ? (
                                            <div className="flex-1">
                                                {quizState[currentLesson.id] === 'passed' ? (
                                                    <div className="bg-[#00FF88]/10 border border-[#00FF88]/30 p-10 rounded-3xl text-center animate-pop">
                                                        <div className="w-24 h-24 bg-[#00FF88] rounded-full text-black flex items-center justify-center mx-auto mb-6 shadow-[0_0_40px_rgba(0,255,136,0.5)]"><Icon name="Check" size={50}/></div>
                                                        <h3 className="text-3xl font-black text-[#00FF88] mb-4">إجابة استراتيجية صحيحة!</h3>
                                                        <p className="text-gray-300 mb-8">لقد أثبتّ جدارتك في فهم هذا المبدأ. تقدم نحو المستوى التالي.</p>
                                                        <button onClick={handleNextLesson} className="px-10 py-4 bg-[#00FF88] text-black font-black rounded-xl text-lg hover:scale-105 transition-transform flex items-center justify-center gap-2 mx-auto">المهمة التالية <Icon name="ArrowLeft" size={20}/></button>
                                                    </div>
                                                ) : (
                                                    <div className="bg-white/5 border border-white/10 p-8 rounded-3xl">
                                                        <h3 className="text-xl font-bold mb-8 text-yellow-500 flex items-center gap-2"><Icon name="Target"/> تحدي الذكاء القيادي:</h3>
                                                        <p className="text-2xl mb-8 leading-relaxed font-bold">{currentLesson.question}</p>
                                                        <div className="grid grid-cols-1 gap-4">
                                                            {(currentLesson.options || []).map((opt, i) => (
                                                                <button 
                                                                    key={i} 
                                                                    onClick={() => handleQuizAnswer(opt)} 
                                                                    className={`text-right p-6 rounded-2xl font-bold text-lg border transition-all ${quizState[currentLesson.id] === 'failed' ? 'bg-red-500/10 border-red-500/30 text-white' : 'bg-[#111] border-white/10 text-gray-300 hover:border-yellow-500 hover:bg-yellow-500/10'}`}
                                                                >
                                                                    <span className="bg-white/10 px-3 py-1 rounded-lg ml-3 text-sm">{i+1}</span> {opt}
                                                                </button>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        ) : currentLesson.type === 'assignment' ? (
                                            <div className="flex-1 bg-white/5 border border-dashed border-white/20 p-8 rounded-3xl">
                                                <div className="flex items-center gap-3 mb-6 text-blue-400"><Icon name="Briefcase" size={28}/> <h3 className="text-2xl font-black">دراسة حالة / تكليف تنفيذي</h3></div>
                                                <div className="text-gray-300 leading-relaxed text-lg mb-8" dangerouslySetInnerHTML={{__html: currentLesson.content}}></div>
                                                <textarea placeholder="اكتب خطتك الاستراتيجية هنا أو ارفق رابط مستند..." className="w-full h-32 bg-black border border-white/10 rounded-xl p-4 text-white focus:border-blue-500 outline-none mb-6"></textarea>
                                                {completedLessons.includes(currentLesson.id) ? (
                                                    <button onClick={handleNextLesson} className="w-full py-4 bg-[#00FF88] text-black font-black rounded-xl">تم التسليم - الانتقال للتالي</button>
                                                ) : (
                                                    <button onClick={() => { playSound('success'); handleNextLesson(); }} className="w-full py-4 bg-blue-500 text-white font-black rounded-xl hover:bg-blue-600 transition-colors">إرسال التكليف للإدارة العليا</button>
                                                )}
                                            </div>
                                        ) : (
                                            <div className="flex-1 flex flex-col">
                                                <div className="text-gray-300 leading-relaxed text-lg mb-10 flex-1" dangerouslySetInnerHTML={{__html: currentLesson.content || 'محتوى الدرس...'}}></div>
                                                <div className="border-t border-white/10 pt-8 mt-auto flex justify-between items-center">
                                                    <div className="text-gray-500 text-sm font-bold flex items-center gap-2"><Icon name="Info" size={16}/> سيتم حفظ تقدمك سحابياً</div>
                                                    <button onClick={() => { playSound('success'); handleNextLesson(); }} className="px-10 py-4 bg-yellow-500 text-black font-black rounded-xl shadow-[0_0_20px_rgba(255,215,0,0.2)] flex items-center gap-2 hover:scale-105 transition-transform">إتمام والانتقال <Icon name="ArrowLeft" size={20}/></button>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ) : (
                                <div className="h-full flex items-center justify-center text-gray-500"><p className="font-bold text-xl">اختر درساً من القائمة الجانبية</p></div>
                            )}
                        </div>

                        {/* القائمة الجانبية للمنهج (Sidebar) */}
                        <div className="w-96 bg-[#0a0a0a] border-r border-white/10 overflow-y-auto no-scrollbar flex flex-col">
                            <div className="p-6 border-b border-white/5 shrink-0">
                                <h3 className="font-black text-xl mb-1">المنهج الدراسي</h3>
                                <p className="text-xs text-gray-500 font-bold">{completedLessons.length} من {flatLessons.length} مكتمل</p>
                            </div>
                            <div className="flex-1">
                                {(course.curriculum || []).map((mod, i) => (
                                    <div key={i} className="border-b border-white/5">
                                        <div className="p-4 bg-[#111] font-black text-sm text-yellow-500 sticky top-0 z-10 border-b border-white/5">القسم {i + 1}: {mod.title}</div>
                                        {(mod.lessons || []).map((lesson, j) => {
                                            const isDone = completedLessons.includes(lesson.id);
                                            const isActive = activeLessonId === lesson.id;
                                            let icon = lesson.type === 'video' ? 'PlayCircle' : lesson.type === 'quiz' ? 'HelpCircle' : lesson.type === 'assignment' ? 'Briefcase' : 'FileText';
                                            if (isDone) icon = 'CheckCircle2';
                                            
                                            return (
                                                <div key={lesson.id} onClick={() => setActiveLessonId(lesson.id)} className={`p-4 pl-6 cursor-pointer flex items-start gap-3 transition-colors ${isActive ? 'bg-white/10 border-r-4 border-yellow-500' : 'hover:bg-white/5 border-r-4 border-transparent'}`}>
                                                    <Icon name={icon} size={18} className={`mt-0.5 shrink-0 ${isDone ? 'text-[#00FF88]' : (isActive ? 'text-yellow-500' : 'text-gray-600')}`} />
                                                    <div>
                                                        <span className={`text-sm font-bold block leading-tight mb-1 ${isActive ? 'text-white' : 'text-gray-400'}`}>{j+1}. {lesson.title}</span>
                                                        <span className="text-[10px] text-gray-600 font-bold">{lesson.duration || '10 د'}</span>
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        // =====================================================================
        // Micro-Frontend 2: Sales Page (بقاء نفس التصميم القوي)
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
                            <button onClick={() => onBuy(course)} className="w-full py-5 rounded-2xl font-black text-lg bg-yellow-500 text-black hover:scale-105 transition-transform flex justify-center items-center gap-3 shadow-[0_10px_30px_rgba(255,215,0,0.3)]"><Icon name="Unlock" size={22} /> فك التشفير وخصم الرصيد</button>
                        </div>
                    </div>
                </div>
            </div>
        );

        // =====================================================================
        // Micro-Frontend 3: Main App (الحاضنة الرئيسية)
        // =====================================================================
        const AppContent = () => {
            const theme = { hex: "#FFD700", btn: "bg-[#FFD700]", btnText: "text-black" }; 
            
            const [selectedCourse, setSelectedCourse] = useState(null);
            const [activeCategory, setActiveCategory] = useState('الكل');
            const [toasts, setToasts] = useState([]);
            
            // Firebase States
            const [user, setUser] = useState(null);
            const [dbInstance, setDbInstance] = useState(null);
            const [unlockedIds, setUnlockedIds] = useState([1]); // كورس 1 مجاني للجميع
            
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // تهيئة Firebase
            useEffect(() => {
                const initFb = async () => {
                    let attempts = 0;
                    while (!window.firebaseModules && attempts < 50) { await new Promise(r => setTimeout(r, 100)); attempts++; }
                    if (window.firebaseModules) {
                        const { initializeApp, getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, getFirestore } = window.firebaseModules;
                        const config = JSON.parse(window.__firebase_config || '{}');
                        if(Object.keys(config).length > 0) {
                            const app = initializeApp(config);
                            const auth = getAuth(app);
                            setDbInstance(getFirestore(app));
                            
                            const token = window.__initial_auth_token;
                            if (token) await signInWithCustomToken(auth, token).catch(e=>console.log(e));
                            else await signInAnonymously(auth).catch(e=>console.log(e));

                            onAuthStateChanged(auth, (u) => {
                                setUser(u);
                            });
                        }
                    }
                };
                initFb();
            }, []);

            // بناء منهج عميق (رحلة 100 يوم) للتجربة الحية
            const coursesDB = [
                { 
                    id: 1, phase: 'المرحلة 1: العقلية', title: 'القيادة التحويلية وصناعة الإمبراطوريات', hours: 20, price: 299, 
                    img: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800', desc: 'تفكيك وبرمجة العقل البشري للعمل بعقلية السيادة والتحول من التفكير الفردي إلى المؤسسي.',
                    curriculum: [
                        { id: 101, title: "الأسس السيكولوجية للسيادة", lessons: [
                            { id: 1001, title: "الجين القيادي: هل يُولد أم يُصنع؟", type: "video", duration: "12:00", content: "<p>في هذا الفيديو، سنحلل كيف استطاع القادة التاريخيون بناء إمبراطورياتهم...</p>" },
                            { id: 1002, title: "اختبار الوعي الاستراتيجي", type: "quiz", question: "كيف يتعامل القائد التحويلي مع فشل فريقه في مهمة أولى؟", options: ["يوبخهم لتجنب تكرار الخطأ", "يعتبره درساً ويحلل الفجوة التنفيذية معهم", "يستبدل الفريق فوراً"], correct: "يعتبره درساً ويحلل الفجوة التنفيذية معهم" },
                            { id: 1003, title: "تحليل قوة الدوبامين", type: "text", duration: "05:00", content: "<p>استخدام المكافآت الصغيرة (Micro-Rewards) لضمان ولاء الجيوش التسويقية...</p>" }
                        ]},
                        { id: 102, title: "التنفيذ على أرض الواقع", lessons: [
                            { id: 2001, title: "قانون الـ 10 للتضاعف", type: "video", duration: "25:00" },
                            { id: 2002, title: "دراسة حالة: بناء مجتمع MR7", type: "assignment", duration: "45:00", content: "<p>قم بكتابة ورقة استراتيجية من 300 كلمة تصف فيها كيف ستقنع أول 10 قادة بالانضمام لجيشك...</p>" },
                            { id: 2003, title: "الاختبار النهائي للمرحلة", type: "quiz", question: "ما هو المحرك الأساسي للاقتصاد المغلق؟", options: ["تقليل الأسعار", "الولاء وتدوير السيولة داخل نفس المنظومة"], correct: "الولاء وتدوير السيولة داخل نفس المنظومة" }
                        ]}
                    ]
                },
                { 
                    id: 2, phase: 'المرحلة 2: الاقتصاد', title: 'هندسة الثروات وتضاعف السيولة', hours: 25, price: 499, 
                    img: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800', desc: 'تعلم قراءة وتحليل القوائم المالية وبناء اقتصادك السيادي المستقل.',
                    curriculum: [ { id: 201, title: "الاقتصاد السيادي", lessons: [ { id: 2001, title: "التدفقات النقدية اللامركزية", type: "video" } ] } ]
                },
                { 
                    id: 3, phase: 'المرحلة 3: التقنية', title: 'تحالف العقول: البشر والذكاء الاصطناعي', hours: 15, price: 350, 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', desc: 'كيف تجعل الذكاء الاصطناعي مستشارك الاستراتيجي المطيع.', curriculum: []
                }
            ];

            // تحديد الكورسات المفتوحة والمغلقة ديناميكياً
            const mappedCourses = coursesDB.map(c => ({...c, locked: !unlockedIds.includes(c.id)}));

            const handleBuy = async (course) => {
                playSound('success');
                showToast(`تم خصم ${course.price}$ وفتح المنهج بنجاح!`, 'success');
                setUnlockedIds([...unlockedIds, course.id]);
                setSelectedCourse({...course, locked: false}); 
                
                // هنا يمكن مستقبلاً إضافة كود خصم الرصيد الحقيقي من Firebase Firestore
            };

            if (selectedCourse) {
                if (selectedCourse.locked) {
                    return <SalesPageView course={selectedCourse} onBack={() => setSelectedCourse(null)} onBuy={handleBuy} />;
                } else {
                    return <CoursePlayerView course={selectedCourse} onBack={() => setSelectedCourse(null)} theme={theme} showToast={showToast} user={user} dbInstance={dbInstance} appId={window.__app_id} />;
                }
            }

            return (
                <div className="min-h-screen bg-[#050505] text-white flex flex-col font-['Tajawal'] animate-fade-in" dir="rtl">
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3">
                        {toasts.map(t => (
                            <div key={t.id} className={`bg-black/90 border px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl flex items-center gap-3 ${t.type==='error' ? 'border-red-500/40 text-red-500' : 'border-[#00FF88]/40 text-[#00FF88]'}`}>
                                <Icon name={t.type==='error' ? 'AlertCircle' : 'CheckCircle2'} size={20} /> <span className="font-bold text-sm">{t.msg}</span>
                            </div>
                        ))}
                    </div>

                    <div className="max-w-[1600px] mx-auto w-full px-6 md:px-10 py-10">
                        <div className="flex flex-col md:flex-row justify-between items-center mb-10 border-b border-white/10 pb-8 gap-4">
                            <div className="flex items-center gap-4">
                                <div className="bg-yellow-500 text-black p-3 rounded-2xl"><Icon name="GraduationCap" size={32} /></div>
                                <div><h1 className="text-3xl font-black uppercase tracking-tighter m-0">MR7 <span className="text-yellow-500">ACADEMY</span></h1><p className="text-xs text-gray-500 font-bold uppercase tracking-[0.2em] m-0">رحلة الـ 100 يوم للسيادة</p></div>
                            </div>
                            <div className="bg-white/5 border border-white/10 p-4 rounded-xl flex items-center gap-4">
                                <div><span className="text-[10px] text-gray-500 block uppercase font-bold">الرصيد المتاح للتعليم</span><span className="text-xl font-black text-[#00FF88]">$50,000</span></div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                            {mappedCourses.map(course => (
                                <div key={course.id} onClick={() => setSelectedCourse(course)} className="course-card bg-[#0a0a0a] rounded-[2rem] border border-white/10 overflow-hidden cursor-pointer group flex flex-col h-full relative">
                                    <div className="relative h-56 w-full overflow-hidden">
                                        <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                                        <img src={course.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                                        <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity">
                                            {course.locked ? 
                                                <div className="bg-black/80 px-6 py-3 rounded-full border border-white/20 text-white flex items-center gap-2 font-black"><Icon name="Lock" size={20} /> فك التشفير</div> : 
                                                <div className="bg-[#00FF88] px-6 py-3 rounded-full text-black flex items-center gap-2 font-black"><Icon name="PlayCircle" size={20} /> متابعة التعلم</div>
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
                                                <div className="w-full"><div className="flex justify-between text-[10px] font-bold mb-1 text-[#00FF88]"><span>منهج متاح</span><span><Icon name="Unlock" size={14}/></span></div></div>
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

        const App = () => (<ErrorBoundary><AppContent /></ErrorBoundary>);
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات للواجهة ---
components.html(react_html, height=1000, scrolling=True)

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
