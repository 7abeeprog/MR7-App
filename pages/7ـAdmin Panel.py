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

# --- 3. واجهة React المتقدمة (لوحة القيادة العليا V16.0) ---
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

            const [activeTab, setActiveTab] = useState('radar');
            const [toasts, setToasts] = useState([]);
            const [user, setUser] = useState(null);
            const [dbInstance, setDbInstance] = useState(null);

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // --- Data States ---
            const [courses, setCourses] = useState([
                { id: 1, title: 'القيادة التحويلية في العصر الرقمي', price: 299, students: 1240, status: 'active' },
                { id: 2, title: 'تحليل الأسهم وأسواق المال', price: 499, students: 850, status: 'active' },
                { id: 3, title: 'الذكاء الاصطناعي في الأعمال', price: 350, students: 2100, status: 'draft' }
            ]);

            const [certificates, setCertificates] = useState([
                { id: 'C-101', student: 'أحمد محمود', course: 'القيادة التحويلية', progress: 100, status: 'pending', date: '2026-04-14' },
                { id: 'C-102', student: 'سارة خالد', course: 'تحليل الأسهم', progress: 100, status: 'issued', date: '2026-04-12' },
                { id: 'C-103', student: 'صالح فهد', course: 'الذكاء الاصطناعي', progress: 100, status: 'pending', date: '2026-04-14' }
            ]);

            const [marketingStats, setMarketingStats] = useState({
                totalSales: 1250000,
                commissionsPaid: 187500,
                activeAffiliates: 3420,
                campaigns: [
                    { name: 'حملة التضاعف العشري (قانون 10)', roi: '+45%', active: true },
                    { name: 'غزو أسواق شمال أفريقيا', roi: '+22%', active: true },
                    { name: 'استقطاب قادة الويب 3', roi: 'N/A', active: false }
                ]
            });

            const [inviteDomain, setInviteDomain] = useState('https://mr7-app.streamlit.app');
            const [generatedLink, setGeneratedLink] = useState('');

            // --- Handlers ---
            const handleIssueCert = (id) => {
                setCertificates(prev => prev.map(c => c.id === id ? {...c, status: 'issued'} : c));
                showToast('تم اعتماد وإصدار الشهادة السيادية بنجاح!', 'success');
            };

            const toggleCourseStatus = (id) => {
                setCourses(prev => prev.map(c => {
                    if (c.id === id) {
                        const newStatus = c.status === 'active' ? 'draft' : 'active';
                        showToast(`تم تغيير حالة البرنامج إلى ${newStatus === 'active' ? 'نشط' : 'مسودة'}`);
                        return {...c, status: newStatus};
                    }
                    return c;
                }));
            };

            const generateInvite = (e) => {
                e.preventDefault();
                const refId = "MR7-VIP-" + Math.random().toString(36).substring(2, 8).toUpperCase();
                setGeneratedLink(`${inviteDomain}?ref=${refId}&auth=vip`);
                showToast('تم توليد الرابط الدبلوماسي المشفر.', 'success');
            };

            const copyLink = () => {
                navigator.clipboard.writeText(generatedLink);
                showToast('تم نسخ الرابط للحافظة.');
            };

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col md:flex-row overflow-hidden font-['Tajawal']`} dir="rtl">
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${theme.card} border-b md:border-b-0 md:border-l ${theme.borderLight} flex flex-col z-10 shadow-2xl`}>
                        <div className="p-8 pb-4 text-center md:text-right">
                            <div className={`${theme.btn} ${theme.btnText} p-4 rounded-2xl inline-block mb-4 shadow-[0_0_30px_rgba(255,75,75,0.4)]`}><Icon name="ShieldAlert" size={32} /></div>
                            <h1 className={`text-2xl font-black uppercase tracking-tighter ${theme.accent}`}>القيادة العليا</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Root Access Granted</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'radar', icon: 'Activity', label: 'الرادار والتحليلات'},
                                {id: 'programs', icon: 'BookOpen', label: 'إدارة المناهج'},
                                {id: 'certificates', icon: 'Award', label: 'اعتماد الشهادات'},
                                {id: 'marketing', icon: 'TrendingUp', label: 'خطط التسويق'},
                                {id: 'injector', icon: 'DatabaseZap', label: 'الحقن السحابي'},
                                {id: 'invites', icon: 'Link', label: 'الروابط الدبلوماسية'}
                            ].map(btn => (
                                <button 
                                    key={btn.id} onClick={() => setActiveTab(btn.id)} 
                                    className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 border-r-4 ${theme.borderLight.replace('/20','')} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}
                                >
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-6 md:p-10 h-screen overflow-y-auto no-scrollbar">
                        
                        {/* Tab: Radar */}
                        {activeTab === 'radar' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto">
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
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">المسوقين النشطين</small>
                                        <h4 className="text-3xl font-black text-blue-500">{marketingStats.activeAffiliates.toLocaleString()}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-purple-500">
                                        <small className="text-gray-500 font-bold uppercase">طلبات الشهادات</small>
                                        <h4 className="text-3xl font-black text-purple-500">{certificates.filter(c=>c.status==='pending').length}</h4>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[2rem]">
                                        <h3 className="text-xl font-black mb-6">نشاط الأقاليم (خارطة الحرارة)</h3>
                                        <div className="space-y-4">
                                            <div><div className="flex justify-between text-sm font-bold mb-1"><span>مصر</span><span className="text-[#00FF88]">45%</span></div><div className="w-full h-2 bg-white/5 rounded-full"><div className="h-full bg-[#00FF88] w-[45%]"></div></div></div>
                                            <div><div className="flex justify-between text-sm font-bold mb-1"><span>السعودية</span><span className="text-yellow-500">30%</span></div><div className="w-full h-2 bg-white/5 rounded-full"><div className="h-full bg-yellow-500 w-[30%]"></div></div></div>
                                            <div><div className="flex justify-between text-sm font-bold mb-1"><span>ليبيا</span><span className="text-blue-500">15%</span></div><div className="w-full h-2 bg-white/5 rounded-full"><div className="h-full bg-blue-500 w-[15%]"></div></div></div>
                                            <div><div className="flex justify-between text-sm font-bold mb-1"><span>السودان</span><span className="text-purple-500">10%</span></div><div className="w-full h-2 bg-white/5 rounded-full"><div className="h-full bg-purple-500 w-[10%]"></div></div></div>
                                        </div>
                                    </div>
                                    <div className="glass-panel p-8 rounded-[2rem] flex flex-col justify-center items-center text-center opacity-50 border border-dashed border-white/20">
                                        <Icon name="BarChart3" size={60} className="mb-4 text-gray-500" />
                                        <h3 className="text-xl font-black mb-2">رسم بياني للمبيعات</h3>
                                        <p className="text-sm font-bold text-gray-400">سيتم تفعيل الرسوم البيانية التفاعلية عند اكتمال جمع البيانات الربع سنوية.</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Programs Manager */}
                        {activeTab === 'programs' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto">
                                <div className="flex justify-between items-center mb-8">
                                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="BookOpen" className={theme.accent} size={32}/> إدارة المناهج الأكاديمية</h2>
                                    <button onClick={()=>showToast('سيتم توجيهك لاستوديو المبدعين لإضافة كورس جديد', 'info')} className={`${theme.btn} ${theme.btnText} px-6 py-3 rounded-xl font-black flex items-center gap-2`}><Icon name="Plus" size={18}/> برنامج جديد</button>
                                </div>

                                <div className="glass-panel p-2 rounded-[2rem] overflow-x-auto border border-white/5">
                                    <table className="w-full text-right">
                                        <thead>
                                            <tr className="border-b border-white/10 text-gray-400 text-sm">
                                                <th className="p-6 font-bold">اسم البرنامج</th>
                                                <th className="p-6 font-bold">السعر</th>
                                                <th className="p-6 font-bold">الطلاب</th>
                                                <th className="p-6 font-bold text-center">الحالة</th>
                                                <th className="p-6 font-bold text-center">إجراءات</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {courses.map(c => (
                                                <tr key={c.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                    <td className="p-6 font-black">{c.title}</td>
                                                    <td className="p-6 text-[#00FF88] font-black">${c.price}</td>
                                                    <td className="p-6 font-bold">{c.students.toLocaleString()}</td>
                                                    <td className="p-6 text-center">
                                                        <span className={`px-3 py-1 rounded-lg text-xs font-black uppercase ${c.status === 'active' ? 'bg-[#00FF88]/20 text-[#00FF88]' : 'bg-gray-500/20 text-gray-400'}`}>
                                                            {c.status === 'active' ? 'نشط' : 'مسودة'}
                                                        </span>
                                                    </td>
                                                    <td className="p-6 flex justify-center gap-2">
                                                        <button onClick={()=>toggleCourseStatus(c.id)} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors" title={c.status==='active'?'إيقاف':'تفعيل'}><Icon name={c.status==='active'?'EyeOff':'Eye'} size={16}/></button>
                                                        <button onClick={()=>showToast('فتح محرر المنهج...', 'info')} className="p-2 bg-blue-500/20 hover:bg-blue-500/40 rounded-lg text-blue-400 transition-colors" title="تعديل"><Icon name="Edit3" size={16}/></button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}

                        {/* Tab: Certificates */}
                        {activeTab === 'certificates' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="Award" className="text-purple-500" size={32}/> اعتماد الشهادات السيادية</h2>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                                    <div className="glass-panel p-8 rounded-[2rem] border border-white/5 flex items-center justify-between">
                                        <div><h4 className="text-gray-400 font-bold mb-1">طلبات معلقة</h4><span className="text-4xl font-black text-yellow-500">{certificates.filter(c=>c.status==='pending').length}</span></div>
                                        <div className="bg-yellow-500/10 p-4 rounded-full text-yellow-500"><Icon name="Clock" size={32}/></div>
                                    </div>
                                    <div className="glass-panel p-8 rounded-[2rem] border border-white/5 flex items-center justify-between">
                                        <div><h4 className="text-gray-400 font-bold mb-1">شهادات مُصدرة</h4><span className="text-4xl font-black text-[#00FF88]">{certificates.filter(c=>c.status==='issued').length}</span></div>
                                        <div className="bg-[#00FF88]/10 p-4 rounded-full text-[#00FF88]"><Icon name="CheckCircle2" size={32}/></div>
                                    </div>
                                </div>

                                <div className="glass-panel p-4 rounded-[2rem] border border-white/5">
                                    {certificates.map(cert => (
                                        <div key={cert.id} className="flex flex-col md:flex-row justify-between items-center p-6 border-b border-white/5 last:border-0 gap-4">
                                            <div className="flex items-center gap-4 w-full md:w-auto">
                                                <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center text-xl">👤</div>
                                                <div>
                                                    <h4 className="font-black text-lg">{cert.student}</h4>
                                                    <p className="text-xs text-gray-400 font-bold">أكمل: <span className="text-white">{cert.course}</span> ({cert.progress}%)</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                                                <span className="text-xs text-gray-500 font-bold">{cert.date}</span>
                                                {cert.status === 'pending' ? (
                                                    <button onClick={()=>handleIssueCert(cert.id)} className="bg-[#00FF88] hover:bg-[#00cc66] text-black px-6 py-2.5 rounded-xl font-black text-sm transition-transform hover:scale-105 shadow-[0_0_20px_rgba(0,255,136,0.3)]">اعتماد وإصدار 📜</button>
                                                ) : (
                                                    <span className="bg-white/10 text-gray-300 px-6 py-2.5 rounded-xl font-black text-sm flex items-center gap-2"><Icon name="Check" size={16}/> تم الإصدار</span>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing Plans */}
                        {activeTab === 'marketing' && (
                            <div className="animate-fade-in space-y-8 max-w-7xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="TrendingUp" className="text-blue-500" size={32}/> خطط التسويق والتضاعف</h2>
                                
                                <div className="glass-panel p-8 rounded-[2.5rem] border border-white/5 mb-8">
                                    <h3 className="text-2xl font-black mb-6 text-white border-b border-white/10 pb-4">حملات الاستقطاب النشطة</h3>
                                    <div className="space-y-6">
                                        {marketingStats.campaigns.map((camp, i) => (
                                            <div key={i} className="flex justify-between items-center bg-black/50 p-6 rounded-2xl border border-white/5">
                                                <div className="flex items-center gap-4">
                                                    <div className={`p-3 rounded-xl ${camp.active ? 'bg-[#00FF88]/20 text-[#00FF88]' : 'bg-gray-500/20 text-gray-500'}`}><Icon name="Target" size={24}/></div>
                                                    <div>
                                                        <h4 className="font-black text-lg">{camp.name}</h4>
                                                        <span className={`text-[10px] font-black uppercase ${camp.active ? 'text-[#00FF88]' : 'text-gray-500'}`}>{camp.active ? 'تعمل الآن' : 'متوقفة'}</span>
                                                    </div>
                                                </div>
                                                <div className="text-center">
                                                    <span className="block text-xs text-gray-500 font-bold mb-1">عائد الحملة (ROI)</span>
                                                    <span className={`text-xl font-black ${camp.roi === 'N/A' ? 'text-gray-500' : 'text-yellow-500'}`}>{camp.roi}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <button onClick={()=>showToast('جاري بناء محرر الحملات المتقدم...', 'info')} className="w-full mt-6 py-4 bg-white/5 hover:bg-white/10 rounded-2xl font-black transition-colors border border-dashed border-white/20 text-gray-300 flex justify-center items-center gap-2"><Icon name="Plus" size={20}/> إطلاق حملة استراتيجية جديدة</button>
                                </div>
                            </div>
                        )}

                        {/* Tab: Bulk Injector (من النسخة القديمة للحفاظ على الأداة) */}
                        {activeTab === 'injector' && (
                            <div className="animate-fade-in space-y-8 max-w-5xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="DatabaseZap" className={theme.accent} size={32}/> محرك الحقن السحابي للبرامج (PDF)</h2>
                                <div className="glass-panel p-10 rounded-[3rem] border border-white/5 text-center">
                                    <Icon name="FileText" size={60} className="mx-auto mb-6 text-gray-600" />
                                    <h3 className="text-2xl font-black mb-4">حقن رحلة الـ 100 يوم</h3>
                                    <p className="text-gray-400 mb-8 max-w-xl mx-auto">هذه الأداة مخصصة لاستخراج وقراءة بيانات ملف Comprehensive_Training_Package.pdf وحقن الـ 100 برنامج دفعة واحدة في قاعدة بيانات Firebase.</p>
                                    <button onClick={()=>showToast('تم إيقاف الحقن لتجنب تكرار البيانات. البيانات موجودة بالفعل في الأكاديمية.', 'warning')} className="bg-yellow-500 text-black px-10 py-5 rounded-2xl font-black text-lg hover:scale-105 transition-transform shadow-[0_0_30px_rgba(255,215,0,0.3)]">بدء عملية الحقن السحابي ⚡</button>
                                </div>
                            </div>
                        )}

                        {/* Tab: Invites (الروابط الدبلوماسية) */}
                        {activeTab === 'invites' && (
                            <div className="animate-fade-in space-y-8 max-w-4xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="Link" className={theme.accent} size={32}/> نظام الدعوات الدبلوماسية</h2>
                                <div className="glass-panel p-10 rounded-[3rem] border border-white/5">
                                    <form onSubmit={generateInvite} className="space-y-6">
                                        <div>
                                            <label className="text-xs font-black text-gray-500 uppercase tracking-widest block mb-2">النطاق الرسمي للتطبيق</label>
                                            <input value={inviteDomain} onChange={e=>setInviteDomain(e.target.value)} className="w-full premium-input p-4 rounded-xl font-bold text-left" dir="ltr"/>
                                        </div>
                                        <button type="submit" className={`w-full ${theme.btn} ${theme.btnText} py-5 rounded-2xl font-black text-xl hover:scale-[1.02] transition-transform shadow-xl flex justify-center items-center gap-2`}><Icon name="Wand2" size={24}/> توليد رابط تسجيل VIP</button>
                                    </form>
                                    {generatedLink && (
                                        <div className="mt-8 p-6 bg-black/40 rounded-2xl border border-[#00FF88]/30">
                                            <h4 className="text-[#00FF88] font-black mb-4 flex items-center gap-2"><Icon name="CheckCircle2" size={20}/> الرابط جاهز</h4>
                                            <div className="flex flex-col md:flex-row gap-4 items-center">
                                                <div className="flex-1 w-full bg-white/5 p-4 rounded-xl font-mono text-sm text-gray-300 break-all border border-white/10" dir="ltr">{generatedLink}</div>
                                                <button onClick={copyLink} className="w-full md:w-auto bg-white/20 hover:bg-white/30 text-white px-8 py-4 rounded-xl font-black transition-colors">نسخ</button>
                                            </div>
                                        </div>
                                    )}
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
