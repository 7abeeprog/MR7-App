import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 GOD MODE - Unified Admin", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة بأمان تام ---
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

# --- 3. واجهة React المتقدمة (لوحة القيادة الشاملة V17.0 - RBAC Architecture) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <!-- CDNs مستقرة ومضادة للحظر -->
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
        ::-webkit-scrollbar-thumb { background: var(--accent-color); border-radius: 10px; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .premium-input { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); color: white; transition: all 0.3s ease; }
        .premium-input:focus { border-color: var(--accent-color); outline: none; box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2); }
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter { 0% { opacity: 0; transform: translateY(100%) scale(0.9); } 100% { opacity: 1; transform: translateY(0) scale(1); } }

        .stat-card { background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.05); padding: 24px; border-radius: 24px; transition: 0.3s; }
        .stat-card:hover { transform: translateY(-5px); border-color: var(--accent-color); box-shadow: 0 10px 30px rgba(0,0,0,0.4); }

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
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; color: #FFD700; font-weight: 900; letter-spacing: 2px;">MR7 GOD MODE</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Decentralized Command Architecture...</p>
    </div>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo, Component, useRef } = React;

        class ErrorBoundary extends Component {
            constructor(props) { super(props); this.state = { hasError: false }; }
            componentDidCatch(error, errorInfo) { this.setState({ hasError: true }); console.error(error); }
            render() { return this.state.hasError ? <div className="p-10 text-center text-red-500">حدث خطأ في عرض الواجهة. يرجى تحديث الصفحة.</div> : this.props.children; }
        }

        const Icon = ({ name, size = 24, className = "" }) => {
            const iconRef = useRef(null);
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
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" }
            };
            const themeName = window.__current_theme || "سلطة مطلقة 🔴";
            const theme = themes[themeName] || themes["سلطة مطلقة 🔴"];
            useEffect(() => { document.documentElement.style.setProperty('--accent-color', theme.hex); }, [theme]);

            // --- RBAC: Role Based Access Control ---
            const ROLES = {
                SUPER_ADMIN: { id: 'super_admin', name: 'الأدمن العام (السيادة المطلقة)', allowedTabs: ['radar', 'academy', 'marketplace', 'crowdfund', 'support', 'network'] },
                ACADEMY_ADMIN: { id: 'academy_admin', name: 'أدمن الأكاديمية (التعليم)', allowedTabs: ['academy'] },
                MARKET_ADMIN: { id: 'market_admin', name: 'أدمن المتجر (التجارة)', allowedTabs: ['marketplace'] },
                SUPPORT_ADMIN: { id: 'support_admin', name: 'أدمن الدعم الفني (العمليات)', allowedTabs: ['support'] },
            };
            const [currentRole, setCurrentRole] = useState(ROLES.SUPER_ADMIN);
            const [activeTab, setActiveTab] = useState('radar');
            
            // Auto-switch tab if role changes and current tab is not allowed
            useEffect(() => {
                if (!currentRole.allowedTabs.includes(activeTab)) {
                    setActiveTab(currentRole.allowedTabs[0]);
                }
            }, [currentRole]);

            const [toasts, setToasts] = useState([]);
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // --- Dummy Data Stores for Modules ---
            // 1. Marketplace Data
            const [pendingProducts, setPendingProducts] = useState([
                { id: 'p101', name: 'استراتيجية النفوذ الإقليمي', vendor: 'د. خالد السيادي', price: 150, type: 'رقمي', status: 'pending' },
                { id: 'p102', name: 'مكتب إداري في مدينة النبت', vendor: 'النبت العقارية', price: 25000, type: 'عقاري', status: 'pending' }
            ]);
            // 2. Crowdfunding Data
            const [pendingPitches, setPendingPitches] = useState([
                { id: 'cf1', title: 'مزرعة الذهب الأخضر', location: 'السودان', goal: 500000, owner: 'القائد (AX992)', status: 'pending' }
            ]);
            // 3. Support Tickets Data
            const [tickets, setTickets] = useState([
                { id: 't1', user: 'صالح (ليبيا)', issue: 'تأخر نزول عمولة الجيل الثاني في محفظتي.', aiReply: 'جاري مراجعة سجلات البلوكتشين الداخلية.', status: 'open', adminReply: '' }
            ]);
            // 4. Academy Data (Simplified)
            const [courses, setCourses] = useState([
                { id: 'c1', title: 'القيادة التحويلية', status: 'active', students: 1240 }
            ]);

            // --- Sub-Views (Micro-Frontends based on Roles) ---

            const RadarView = () => (
                <div className="animate-fade-in space-y-8">
                    <h2 className="text-3xl font-black flex items-center gap-3 mb-8"><Icon name="Activity" className={theme.accent} size={32}/> الرادار السيادي</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div className="stat-card border-t-4 border-[#00FF88]"><small className="text-gray-500 font-bold">السيولة المركزية</small><h4 className="text-3xl font-black text-[#00FF88]">$1,250,000</h4></div>
                        <div className="stat-card border-t-4 border-yellow-500"><small className="text-gray-500 font-bold">قوة الجيش الإجمالي</small><h4 className="text-3xl font-black text-yellow-500">14,250</h4></div>
                        <div className="stat-card border-t-4 border-blue-500"><small className="text-gray-500 font-bold">مشاريع التمويل النشطة</small><h4 className="text-3xl font-black text-blue-500">3</h4></div>
                        <div className="stat-card border-t-4 border-red-500"><small className="text-gray-500 font-bold">تذاكر دعم مفتوحة</small><h4 className="text-3xl font-black text-red-500">{tickets.filter(t=>t.status==='open').length}</h4></div>
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
                        <div className="glass-panel p-8 rounded-[2rem]">
                            <h3 className="text-xl font-black mb-6 border-b border-white/10 pb-4">الإشعارات الحية للإدارة</h3>
                            <div className="space-y-4">
                                <div className="bg-white/5 p-4 rounded-xl flex justify-between items-center"><span className="text-sm font-bold">منتج جديد ينتظر المراجعة في المتجر</span><button onClick={()=>setActiveTab('marketplace')} className="text-xs bg-yellow-500/20 text-yellow-500 px-3 py-1 rounded-lg font-black">مراجعة</button></div>
                                <div className="bg-white/5 p-4 rounded-xl flex justify-between items-center"><span className="text-sm font-bold">طلب تمويل جماعي جديد (السودان)</span><button onClick={()=>setActiveTab('crowdfund')} className="text-xs bg-blue-500/20 text-blue-400 px-3 py-1 rounded-lg font-black">مراجعة</button></div>
                            </div>
                        </div>
                    </div>
                </div>
            );

            const AcademyAdminView = () => (
                <div className="animate-fade-in space-y-8">
                    <div className="flex justify-between items-center">
                        <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="GraduationCap" className={theme.accent} size={32}/> إدارة الأكاديمية</h2>
                        <button onClick={()=>showToast('سيتم نقلك لغرفة هندسة المناهج المتقدمة', 'info')} className={`${theme.btn} ${theme.btnText} px-6 py-3 rounded-xl font-black flex items-center gap-2`}><Icon name="Plus" size={18}/> منهج جديد</button>
                    </div>
                    <div className="glass-panel p-4 rounded-[2rem] border border-white/5">
                        <table className="w-full text-right">
                            <thead><tr className="border-b border-white/10 text-gray-500 text-sm"><th className="p-4">البرنامج</th><th className="p-4">الطلاب</th><th className="p-4">الحالة</th><th className="p-4 text-center">إجراءات</th></tr></thead>
                            <tbody>
                                {courses.map(c => (
                                    <tr key={c.id} className="border-b border-white/5 hover:bg-white/5"><td className="p-4 font-black">{c.title}</td><td className="p-4 font-bold text-yellow-500">{c.students}</td><td className="p-4"><span className="bg-[#00FF88]/20 text-[#00FF88] px-2 py-1 rounded text-xs font-black">نشط</span></td>
                                    <td className="p-4 text-center"><button onClick={()=>showToast('تم فتح محرر الخارطة الأكاديمية (انظر النسخة السابقة للاستعراض التفصيلي)')} className="bg-white/10 px-4 py-2 rounded-lg text-xs font-bold hover:bg-white/20">تعديل المنهج ✏️</button></td></tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            );

            const MarketplaceAdminView = () => (
                <div className="animate-fade-in space-y-8">
                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Store" className="text-[#00FF88]" size={32}/> الرقابة التجارية (المتجر)</h2>
                    <div className="glass-panel p-8 rounded-[2.5rem] border border-white/5">
                        <h3 className="text-xl font-black mb-6">منتجات بانتظار الاعتماد السيادي</h3>
                        {pendingProducts.length === 0 ? <p className="text-gray-500">لا توجد منتجات معلقة.</p> : 
                            <div className="space-y-4">
                                {pendingProducts.map(p => (
                                    <div key={p.id} className="bg-black/50 border border-white/10 p-6 rounded-2xl flex flex-col md:flex-row justify-between items-center gap-4">
                                        <div>
                                            <h4 className="text-lg font-black">{p.name}</h4>
                                            <p className="text-sm text-gray-400 font-bold">التاجر: {p.vendor} | النوع: {p.type}</p>
                                        </div>
                                        <div className="flex items-center gap-6">
                                            <span className="text-2xl font-black text-[#00FF88]">${p.price}</span>
                                            <div className="flex gap-2">
                                                <button onClick={()=>{setPendingProducts(pendingProducts.filter(x=>x.id!==p.id)); showToast('تم الاعتماد. المنتج الآن معروض للعامة.', 'success');}} className="bg-[#00FF88] text-black px-6 py-2.5 rounded-xl font-black hover:scale-105 transition-transform shadow-[0_0_15px_rgba(0,255,136,0.3)] flex items-center gap-1"><Icon name="Check" size={16}/> اعتماد</button>
                                                <button onClick={()=>{setPendingProducts(pendingProducts.filter(x=>x.id!==p.id)); showToast('تم رفض المنتج وإخطار التاجر.', 'error');}} className="bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white px-4 py-2.5 rounded-xl font-black transition-colors"><Icon name="X" size={16}/></button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        }
                    </div>
                </div>
            );

            const CrowdfundAdminView = () => (
                <div className="animate-fade-in space-y-8">
                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Target" className="text-blue-500" size={32}/> رقابة التمويل والمشاريع الكبرى</h2>
                    <div className="glass-panel p-8 rounded-[2.5rem] border border-white/5">
                        <h3 className="text-xl font-black mb-6">دراسات جدوى بانتظار الطرح</h3>
                        {pendingPitches.length === 0 ? <p className="text-gray-500">لا توجد مشاريع معلقة.</p> : 
                            <div className="grid grid-cols-1 gap-6">
                                {pendingPitches.map(p => (
                                    <div key={p.id} className="bg-black/40 border border-white/5 p-6 rounded-2xl">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-lg text-[10px] font-black uppercase mb-2 inline-block">{p.location}</span>
                                                <h4 className="text-2xl font-black">{p.title}</h4>
                                                <p className="text-sm text-gray-500 font-bold mt-1">مقدم من: {p.owner}</p>
                                            </div>
                                            <div className="text-left">
                                                <span className="block text-[10px] text-gray-500 font-bold uppercase">التمويل المطلوب</span>
                                                <span className="text-3xl font-black text-yellow-500">${p.goal.toLocaleString()}</span>
                                            </div>
                                        </div>
                                        <div className="flex gap-3 border-t border-white/10 pt-5 mt-4">
                                            <button onClick={()=>showToast('سيتم فتح الملف بصيغة PDF للمراجعة الدقيقة', 'info')} className="bg-white/10 hover:bg-white/20 px-6 py-3 rounded-xl font-black text-sm transition-colors flex items-center gap-2"><Icon name="FileText" size={16}/> مراجعة دراسة الجدوى</button>
                                            <button onClick={()=>{setPendingPitches(pendingPitches.filter(x=>x.id!==p.id)); showToast('تمت الموافقة! المشروع الآن في ساحة التمويل العامة.', 'success');}} className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-xl font-black text-sm shadow-[0_0_20px_rgba(37,99,235,0.4)] flex items-center gap-2"><Icon name="CheckCircle2" size={16}/> إطلاق جولة التمويل</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        }
                    </div>
                </div>
            );

            const SupportAdminView = () => {
                const [replyText, setReplyText] = useState({});
                return (
                    <div className="animate-fade-in space-y-8">
                        <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="LifeBuoy" className="text-red-500" size={32}/> غرفة العمليات والدعم</h2>
                        <div className="glass-panel p-8 rounded-[2.5rem] border border-white/5">
                            <h3 className="text-xl font-black mb-6">برقيات الطوارئ وتذاكر الدعم</h3>
                            <div className="space-y-6">
                                {tickets.map(t => (
                                    <div key={t.id} className="bg-black/50 border-l-4 border-red-500 p-6 rounded-2xl shadow-lg">
                                        <div className="flex justify-between items-center mb-4 pb-4 border-b border-white/5">
                                            <span className="font-black flex items-center gap-2"><div className="w-8 h-8 bg-white/10 rounded-full flex justify-center items-center">👤</div> {t.user}</span>
                                            <span className="bg-red-500/20 text-red-500 px-3 py-1 rounded-md text-xs font-black">قيد المعالجة</span>
                                        </div>
                                        <p className="font-bold text-lg leading-relaxed mb-4">"{t.issue}"</p>
                                        <div className="bg-blue-500/10 border border-blue-500/20 p-4 rounded-xl mb-4">
                                            <span className="text-[10px] text-blue-400 font-black uppercase flex items-center gap-1 mb-2"><Icon name="Bot" size={12}/> رد الوكيل الذكي الأولي</span>
                                            <p className="text-sm font-bold text-gray-300">{t.aiReply}</p>
                                        </div>
                                        {t.status === 'open' ? (
                                            <div className="flex gap-3 mt-4">
                                                <input value={replyText[t.id] || ''} onChange={(e)=>setReplyText({...replyText, [t.id]: e.target.value})} placeholder="اكتب رد الإدارة النهائي هنا لإغلاق التذكرة..." className="flex-1 premium-input p-4 rounded-xl text-sm font-bold" />
                                                <button onClick={()=>{
                                                    if(!replyText[t.id]) return;
                                                    setTickets(tickets.map(x=>x.id===t.id?{...x, status:'closed', adminReply: replyText[t.id]}:x));
                                                    showToast('تم إرسال الرد وإغلاق البرقية.', 'success');
                                                }} className="bg-white text-black px-8 rounded-xl font-black hover:bg-gray-200 transition-colors">إرسال الرد وإغلاق</button>
                                            </div>
                                        ) : (
                                            <div className="bg-[#00FF88]/10 p-4 rounded-xl mt-4 border border-[#00FF88]/20">
                                                <span className="text-[10px] text-[#00FF88] font-black uppercase block mb-1">رد الإدارة</span>
                                                <p className="text-sm font-bold">{t.adminReply}</p>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            };

            const NetworkAdminView = () => (
                <div className="animate-fade-in space-y-8">
                    <h2 className="text-3xl font-black flex items-center gap-3"><Icon name="Network" className="text-purple-500" size={32}/> الدبلوماسية والتوسع (الإحالة)</h2>
                    <div className="glass-panel p-8 rounded-[2.5rem] border border-white/5 text-center py-16">
                        <Icon name="Link" size={60} className="mx-auto text-purple-500 mb-6" />
                        <h3 className="text-2xl font-black mb-4">مولد الروابط السيادية السري</h3>
                        <p className="text-gray-400 font-bold mb-8 max-w-lg mx-auto">تجاوز نظام التسجيل العادي وأصدر روابط دعوة مشفرة تمنح صلاحيات VIP فورية للقادة الجدد.</p>
                        <button onClick={()=>showToast('تم توليد ونسخ الرابط الدبلوماسي: https://mr7.com/invite?vip=X99', 'success')} className="bg-purple-600 hover:bg-purple-500 text-white px-10 py-5 rounded-2xl font-black text-lg shadow-[0_0_30px_rgba(147,51,234,0.4)] transition-all hover:scale-105 flex items-center gap-2 mx-auto"><Icon name="Wand2" size={20}/> توليد رابط VIP 👑</button>
                    </div>
                </div>
            );

            // --- Menu Mapping based on Role ---
            const ALL_MENU_ITEMS = [
                { id: 'radar', icon: 'Activity', label: 'الرادار العام' },
                { id: 'academy', icon: 'GraduationCap', label: 'شؤون الأكاديمية' },
                { id: 'marketplace', icon: 'Store', label: 'الرقابة التجارية' },
                { id: 'crowdfund', icon: 'Target', label: 'التمويل والمشاريع' },
                { id: 'network', icon: 'Network', label: 'الدعوات والانتشار' },
                { id: 'support', icon: 'LifeBuoy', label: 'غرفة العمليات' },
            ];

            const allowedMenuItems = ALL_MENU_ITEMS.filter(item => currentRole.allowedTabs.includes(item.id));

            return (
                <div className={`min-h-screen ${theme.bg} ${theme.text} flex flex-col md:flex-row overflow-hidden font-['Tajawal']`} dir="rtl">
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${theme.card} border-b md:border-b-0 md:border-l ${theme.borderLight} flex flex-col z-10 shadow-2xl shrink-0`}>
                        
                        <div className="p-8 pb-2 text-center md:text-right relative">
                            <div className={`${theme.btn} ${theme.btnText} p-3 rounded-2xl inline-block mb-4 shadow-[0_0_30px_rgba(255,75,75,0.3)]`}><Icon name="ShieldAlert" size={32} /></div>
                            <h1 className={`text-2xl font-black uppercase tracking-tighter ${theme.accent}`}>القيادة العليا</h1>
                            
                            {/* Role Simulator Dropdown */}
                            <div className="mt-4 bg-black/40 p-3 rounded-xl border border-white/10">
                                <label className="text-[9px] text-gray-500 uppercase font-black block mb-1">محاكي الصلاحيات (RBAC)</label>
                                <select 
                                    className="w-full bg-transparent text-xs font-bold text-white outline-none border-none cursor-pointer"
                                    value={currentRole.id}
                                    onChange={(e) => setCurrentRole(Object.values(ROLES).find(r => r.id === e.target.value))}
                                >
                                    {Object.values(ROLES).map(r => <option key={r.id} value={r.id} className="bg-black text-white">{r.name}</option>)}
                                </select>
                            </div>
                        </div>

                        <div className="flex flex-row md:flex-col gap-2 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1 mt-4">
                            {allowedMenuItems.map(btn => (
                                <button 
                                    key={btn.id} onClick={() => setActiveTab(btn.id)} 
                                    className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? `bg-white/5 border-r-4 ${theme.borderLight.replace('/20','')} ${theme.accent} shadow-md` : 'text-gray-500 hover:text-white hover:bg-white/5'}`}
                                >
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Area --- */}
                    <div className="flex-1 h-screen overflow-y-auto no-scrollbar p-6 md:p-10 relative">
                        {/* Dynamic Rendering based on Active Tab */}
                        {activeTab === 'radar' && <RadarView />}
                        {activeTab === 'academy' && <AcademyAdminView />}
                        {activeTab === 'marketplace' && <MarketplaceAdminView />}
                        {activeTab === 'crowdfund' && <CrowdfundAdminView />}
                        {activeTab === 'support' && <SupportAdminView />}
                        {activeTab === 'network' && <NetworkAdminView />}
                    </div>

                    {/* Toasts Container */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : t.type === 'error' ? 'bg-black/90 border-red-500/40 text-red-500' : 'bg-black/90 border-blue-500/40 text-blue-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : t.type === 'error' ? 'AlertCircle' : 'Info'} size={20} />
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

# --- 4. حقن المتغيرات السحابية ---
components.html(react_html, height=1000, scrolling=True)

# --- 5. أزرار التنقل السريع الخاصة ببايثون ---
st.markdown("---")
st.markdown("### 🗺️ مسارات الوصول السريعة للواجهات العامة")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🛒 معاينة المتجر العام"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🎓 معاينة الأكاديمية"):
        st.switch_page("pages/1_Education.py")
with c3:
    if st.button("🏠 العودة للرئيسية"):
        st.switch_page("app.py")
