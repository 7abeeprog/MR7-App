import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية في ستريمليت ---
st.set_page_config(
    page_title="MR7 Elite Operations Center", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة والنمط ---
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
current_balance = st.session_state.get('cash_balance', 1250000)

# --- 3. واجهة React المتقدمة (الإصدار 13.0 - دمج مركز التواصل والـ CRM) ---
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
            background-color: #030303;
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #FFD700; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: white;
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            border-color: #FFD700;
            box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.1);
            outline: none;
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        .chat-bubble-client { background: rgba(255,255,255,0.05); border-radius: 15px 15px 0 15px; margin: 10px 0; padding: 12px; }
        .chat-bubble-merchant { background: rgba(255,215,0,0.1); border-radius: 15px 15px 15px 0; margin: 10px 0; padding: 12px; border-right: 3px solid #FFD700; }

        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        #loading-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            background: #000; color: #FFD700; display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 99999;
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px;">جاري تشغيل مركز القيادة الموحد...</h2>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

        const Icon = ({ name, size = 24, className = "", fill = "none" }) => {
            const iconRef = useRef(null);
            useEffect(() => {
                if (iconRef.current && window.lucide) {
                    iconRef.current.innerHTML = ''; 
                    const i = document.createElement('i');
                    i.setAttribute('data-lucide', name);
                    if (className) i.setAttribute('class', className);
                    i.setAttribute('fill', fill);
                    iconRef.current.appendChild(i);
                    window.lucide.createIcons({ root: iconRef.current });
                }
            }, [name, size, className, fill]);
            return <span ref={iconRef} className={`inline-flex justify-center items-center ${className}`}></span>;
        };

        const App = () => {
            const [activeTab, setActiveTab] = useState('overview');
            const [toasts, setToasts] = useState([]);
            
            // --- 1. الأصول (Assets) ---
            const [assets, setAssets] = useState([
                { id: 1, name: 'برج السيادة الإداري', price: 1500000, commRates: [10,5,2,1,1,1,1,1,1,1], stock: 5, type: 'عقاري', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400' }
            ]);

            // --- 2. العمليات (Operations) ---
            const [orders, setOrders] = useState([
                { id: 'ORD-202', buyer: 'أحمد القائد', item: 'برج السيادة', amount: 1500000, status: 'قيد المراجعة' }
            ]);

            // --- 3. مركز التواصل (Communications & CRM) ---
            const [chats, setChats] = useState([
                { id: 1, sender: 'أحمد القائد', type: 'Client', lastMsg: 'هل يمكنني زيادة مبلغ القسط الأول؟', time: '10:30 AM', unread: true },
                { id: 2, sender: 'فريق تسويق القاهرة', type: 'Team', lastMsg: 'تم تجهيز فيديو 'برج السيادة' الجديد.', time: '09:15 AM', unread: false }
            ]);
            const [activeChat, setActiveChat] = useState(null);
            const [messageText, setMessageText] = useState('');

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            const handleSendMessage = () => {
                if(!messageText) return;
                showToast('تم إرسال برقية التواصل بنجاح');
                setMessageText('');
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-xl"><Icon name="Terminal" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">مركز القيادة</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Enterprise v13.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار'},
                                {id: 'inventory', icon: 'Box', label: 'الأصول'},
                                {id: 'operations', icon: 'Activity', label: 'العمليات'},
                                {id: 'communications', icon: 'MessageSquare', label: 'مركز التواصل', badge: '2'},
                                {id: 'marketing', icon: 'Zap', label: 'التسويق'},
                                {id: 'finance', icon: 'CreditCard', label: 'المالية'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center justify-between px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500 shadow-md' : 'text-gray-500 hover:text-white'}`}>
                                    <div className="flex items-center gap-4">
                                        <Icon name={btn.icon} size={18} /> {btn.label}
                                    </div>
                                    {btn.badge && <span className="bg-red-500 text-white text-[10px] px-1.5 py-0.5 rounded-full">{btn.badge}</span>}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-5">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500 shadow-xl">
                                        <small className="text-gray-500 font-bold uppercase">التدفق المالي</small>
                                        <h4 className="text-3xl font-black text-green-500">$3.4M</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">الطلبات النشطة</small>
                                        <h4 className="text-3xl font-black">{orders.length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">رسائل بانتظار الرد</small>
                                        <h4 className="text-3xl font-black text-blue-500">2</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-purple-500">
                                        <small className="text-gray-500 font-bold uppercase">الأصول الموثقة</small>
                                        <h4 className="text-3xl font-black">{assets.length}</h4>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (Logic CRUD) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col xl:flex-row gap-8">
                                    <div className="xl:w-2/5 glass-panel p-8 rounded-[2.5rem] h-fit">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="PlusCircle" className="text-yellow-500"/> هندسة أصل جديد</h3>
                                        <form className="space-y-4">
                                            <input placeholder="اسم الأصل..." required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            <div className="grid grid-cols-2 gap-3">
                                                <input type="number" placeholder="القيمة ($)" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <select className="w-full premium-input p-4 rounded-xl font-bold bg-black text-sm"><option>عقاري</option><option>منتج</option></select>
                                            </div>
                                            <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                                                <label className="text-[10px] font-black text-gray-500 block mb-2">تخصيص عمولات الأجيال (10 مستويات %)</label>
                                                <div className="grid grid-cols-5 gap-2">
                                                    {Array.from({length: 10}).map((_, i) => (
                                                        <input key={i} placeholder={`ج${i+1}`} className="premium-input p-2 rounded-lg text-center text-xs font-bold" />
                                                    ))}
                                                </div>
                                            </div>
                                            <button className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all shadow-xl">نشر الأصل 🚀</button>
                                        </form>
                                    </div>
                                    <div className="xl:w-3/5 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد الأصول الموثقة</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-xs border-b border-white/5 uppercase"><th className="pb-4 text-right">الأصل</th><th className="pb-4 text-center">المخزون</th><th className="pb-4 text-center">القيمة</th><th className="pb-4 text-center">إجراء</th></tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all">
                                                        <td className="py-4 flex items-center gap-4">
                                                            <img src={a.img} className="w-12 h-12 rounded-xl object-cover" />
                                                            <div className="font-bold text-sm">{a.name}</div>
                                                        </td>
                                                        <td className="py-4 text-center font-black">{a.stock}</td>
                                                        <td className="py-4 text-center text-[#00FF88] font-black">${a.price.toLocaleString()}</td>
                                                        <td className="py-4 text-center"><button className="text-red-500"><Icon name="Trash2" size={18}/></button></td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Communications & CRM (The Hub Interface) */}
                        {activeTab === 'communications' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto h-[75vh]">
                                <div className="flex h-full gap-6">
                                    {/* Chat List */}
                                    <div className="w-1/3 glass-panel rounded-[2.5rem] flex flex-col overflow-hidden">
                                        <div className="p-6 border-b border-white/10 flex justify-between items-center">
                                            <h3 className="text-xl font-black uppercase">الرسائل</h3>
                                            <Icon name="Filter" size={18} className="text-gray-500" />
                                        </div>
                                        <div className="flex-1 overflow-y-auto no-scrollbar p-2">
                                            {chats.map(chat => (
                                                <div 
                                                    key={chat.id} 
                                                    onClick={() => setActiveChat(chat)}
                                                    className={`p-4 rounded-2xl cursor-pointer transition-all mb-2 ${activeChat?.id === chat.id ? 'bg-white/10 border-r-4 border-yellow-500' : 'hover:bg-white/5 border border-transparent'}`}
                                                >
                                                    <div className="flex justify-between items-start mb-1">
                                                        <span className="font-black text-sm">{chat.sender}</span>
                                                        <small className="text-[10px] text-gray-500">{chat.time}</small>
                                                    </div>
                                                    <div className="flex justify-between items-center">
                                                        <p className="text-[11px] text-gray-400 truncate">{chat.lastMsg}</p>
                                                        {chat.unread && <div className="w-2 h-2 bg-blue-500 rounded-full"></div>}
                                                    </div>
                                                    <span className={`text-[8px] uppercase font-black px-2 py-0.5 rounded-md mt-2 inline-block ${chat.type === 'Client' ? 'bg-green-500/10 text-green-500' : 'bg-purple-500/10 text-purple-500'}`}>{chat.type}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Chat Window */}
                                    <div className="w-2/3 glass-panel rounded-[2.5rem] flex flex-col overflow-hidden relative">
                                        {activeChat ? (
                                            <>
                                                <div className="p-6 border-b border-white/10 bg-white/5 flex items-center justify-between">
                                                    <div className="flex items-center gap-4">
                                                        <div className="w-10 h-10 rounded-full bg-yellow-500 text-black flex items-center justify-center font-black">👤</div>
                                                        <div>
                                                            <h4 className="font-black">{activeChat.sender}</h4>
                                                            <small className="text-[#00FF88] text-[9px] font-bold uppercase">Online Now</small>
                                                        </div>
                                                    </div>
                                                    <div className="flex gap-4 opacity-50">
                                                        <Icon name="Phone" size={18} />
                                                        <Icon name="Info" size={18} />
                                                    </div>
                                                </div>
                                                <div className="flex-1 p-6 overflow-y-auto no-scrollbar space-y-4">
                                                    <div className="chat-bubble-client">
                                                        <p className="text-sm">أهلاً يا قائد، مهتم بشراء برج السيادة الإداري، هل هناك تسهيلات في دفع القسط الثالث؟</p>
                                                    </div>
                                                    <div className="chat-bubble-merchant">
                                                        <p className="text-sm">أهلاً بك يا شريك النجاح. نعم، نظامنا يدعم إعادة هيكلة الأقساط بعد سداد 30% من القيمة. سأرسل لك التفاصيل.</p>
                                                    </div>
                                                </div>
                                                <div className="p-6 border-t border-white/10 bg-black/20 flex gap-4">
                                                    <input 
                                                        value={messageText}
                                                        onChange={(e)=>setMessageText(e.target.value)}
                                                        placeholder="اكتب رسالتك القيادية هنا..." 
                                                        className="flex-1 premium-input p-4 rounded-xl font-bold text-sm" 
                                                    />
                                                    <button onClick={handleSendMessage} className="bg-yellow-500 text-black px-8 rounded-xl font-black transition-all hover:scale-105 active:scale-95"><Icon name="Send" size={20}/></button>
                                                </div>
                                            </>
                                        ) : (
                                            <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-40">
                                                <Icon name="MessageSquare" size={60} className="mb-4" />
                                                <p className="text-xl font-black">اختر محادثة لبدء القيادة اللحظية</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* ... (باقي التبويبات تتبع نفس هيكلة Logic CRUD في v12) ... */}
                    </div>

                    {/* --- Toasts Center --- */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                                <span className="font-bold text-sm text-white text-dir">{t.msg}</span>
                            </div>
                        ))}
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ErrorBoundary><App /></ErrorBoundary>);

        function ErrorBoundary({ children }) {
            const [hasError, setHasError] = useState(false);
            if (hasError) return <div className="p-10 text-red-500 font-black text-center h-screen flex items-center justify-center">⚠️ رصد خطأ في العقل الاقتصادي.. جاري إعادة التوثيق..</div>;
            return children;
        }
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل آمن ---
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=1150, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
