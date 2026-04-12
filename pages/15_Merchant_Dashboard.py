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

# --- 3. واجهة React المتقدمة (الإصدار 10.0 - العقل الاقتصادي المتكامل) ---
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

        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        .pulse-red { animation: pulse-red-anim 2s infinite; }
        @keyframes pulse-red-anim {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }

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
        <h2 style="margin-top:20px;">جاري إقلاع المحرك الاقتصادي السيادي...</h2>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

        // --- مكون الأيقونات المصفح ---
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
            const [lang, setLang] = useState('ar');
            const [toasts, setToasts] = useState([]);
            const [balance, setBalance] = useState(Number(LEADER_BALANCE_PLACEHOLDER));

            // --- 1. إدارة الأصول (Assets CRUD) ---
            const [assets, setAssets] = useState([
                { id: 1, name: 'برج السيادة الإداري', stock: 5, price: 1500000, type: 'عقاري', commRate: 10, discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400', desc: 'مقر قيادي عالمي.' },
                { id: 2, name: 'دبلوم هندسة الأرباح', stock: Infinity, price: 499, type: 'رقمي', commRate: 15, discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400', desc: 'صناعة عقلية المليار.' }
            ]);

            // --- 2. إدارة العمليات والمرتجعات (Orders & Returns) ---
            const [orders, setOrders] = useState([
                { id: 'ORD-77', buyer: 'أحمد القائد', item: 'دبلوم هندسة الأرباح', amount: 499, status: 'قيد المعالجة', date: 'منذ ساعة' }
            ]);
            const [returns, setReturns] = useState([
                { id: 'RET-12', buyer: 'سارة خالد', item: 'منظومة طاقة', reason: 'طلب استبدال فني', status: 'منتظر' }
            ]);

            // --- 3. الأنظمة المالية (Installments & Subs) ---
            const [installments, setInstallments] = useState([
                { id: 'INS-01', user: 'ياسين علي', item: 'برج السيادة', total: 1500000, paid: 500000, next_due: '2026-05-01' }
            ]);
            const [subscriptions, setSubscriptions] = useState([
                { id: 'SUB-10', user: 'مجموعة النبت', plan: 'دعم تقني سنوي', price: 5000, status: 'نشط' }
            ]);

            // --- 4. التسويق والولاء (Loyalty & Discounts) ---
            const [loyaltyPoints, setLoyaltyPoints] = useState(124500);
            const [globalDiscount, setGlobalDiscount] = useState(0);

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- محركات المنطق ---
            const handleAddAsset = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                const n = {
                    id: Date.now(),
                    name: f.get('name'), price: parseFloat(f.get('price')), commRate: parseFloat(f.get('comm')),
                    stock: f.get('type') === 'رقمي' ? Infinity : parseInt(f.get('stock')),
                    type: f.get('type'), img: f.get('img'), desc: f.get('desc'), status: 'نشط', discount: 0
                };
                setAssets([n, ...assets]);
                showToast('تم إدراج الأصل وتحديث قاعدة البيانات');
                e.target.reset();
            };

            const processReturn = (id, approved) => {
                setReturns(returns.filter(r => r.id !== id));
                showToast(approved ? 'تمت الموافقة على المرتجع' : 'تم رفض المرتجع لعدم استيفاء الشروط', approved ? 'success' : 'warning');
            };

            const collectInstallment = (id) => {
                setInstallments(installments.map(i => i.id === id ? {...i, paid: i.paid + 100000} : i));
                showToast('تم تحصيل دفعة بقيمة $100,000 وتوثيقها مالياً');
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar (Command Menu) --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10 shadow-2xl">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-xl"><Icon name="Cpu" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">العقل التجاري</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Economic Brain v10.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار'},
                                {id: 'inventory', icon: 'Box', label: 'المخزون'},
                                {id: 'operations', icon: 'Activity', label: 'العمليات'},
                                {id: 'marketing', icon: 'Megaphone', label: 'التسويق'},
                                {id: 'finance', icon: 'CreditCard', label: 'المالية الاستراتيجية'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Arena --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto pt-10">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500 shadow-xl">
                                        <small className="text-gray-500 font-bold uppercase">صافي التدفق المالي</small>
                                        <h4 className="text-3xl font-black text-green-500">$2.4M</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">الطلبات النشطة</small>
                                        <h4 className="text-3xl font-black">{orders.length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-red-500 pulse-red">
                                        <small className="text-gray-500 font-bold uppercase">المرتجعات العالقة</small>
                                        <h4 className="text-3xl font-black text-red-500">{returns.length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">رصيد الولاء</small>
                                        <h4 className="text-3xl font-black text-blue-500">{loyaltyPoints.toLocaleString()}</h4>
                                    </div>
                                </div>

                                <div className="glass-panel p-8 rounded-[3rem] mt-10">
                                    <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="Bell" className="text-yellow-500"/> رادار التنبيهات الذكي</h3>
                                    <div className="space-y-4">
                                        <div className="p-4 bg-red-500/10 rounded-2xl border border-red-500/20 text-red-500 font-bold flex justify-between items-center">
                                            <span>تنبيه: قسط 'برج السيادة' للمستخدم ياسين علي مستحق خلال 48 ساعة.</span>
                                            <button onClick={()=>collectInstallment('INS-01')} className="bg-red-500 text-white px-4 py-1.5 rounded-xl text-xs">تحصيل فوري</button>
                                        </div>
                                        <div className="p-4 bg-yellow-500/10 rounded-2xl border border-yellow-500/20 text-yellow-500 font-bold">
                                            تنبيه: مخزون 'برج السيادة' يقترب من النفاد (المتبقي: 5).
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (Logic CRUD) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col lg:flex-row gap-8">
                                    <div className="lg:w-1/3 glass-panel p-8 rounded-[2.5rem] h-fit sticky top-0">
                                        <h3 className="text-xl font-black mb-6">هندسة أصل جديد</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="اسم المنتج..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <div className="grid grid-cols-2 gap-2">
                                                <input name="price" type="number" placeholder="السعر ($)" required className="w-full premium-input p-4 rounded-xl font-bold" />
                                                <input name="comm" type="number" placeholder="العمولة %" required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            </div>
                                            <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black">
                                                <option>منتج</option><option>عقاري</option><option>رقمي</option>
                                            </select>
                                            <input name="stock" type="number" placeholder="الكمية" className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <textarea name="desc" placeholder="وصف المنتج..." className="w-full premium-input p-4 rounded-xl font-bold h-24"></textarea>
                                            <button type="submit" className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all">إدراج الأصل 🚀</button>
                                        </form>
                                    </div>
                                    <div className="lg:w-2/3 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد الأصول والعدادات</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-xs border-b border-white/5 uppercase"><th className="pb-4 text-right">الأصل</th><th className="pb-4 text-center">المخزون</th><th className="pb-4 text-center">العمولة</th><th className="pb-4 text-center">إجراء</th></tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all group">
                                                        <td className="py-4 flex items-center gap-4">
                                                            <img src={a.img} className="w-12 h-12 rounded-xl object-cover" />
                                                            <div><div className="font-bold">{a.name}</div><small className="text-gray-500">{a.type}</small></div>
                                                        </td>
                                                        <td className="py-4 text-center font-black">{a.stock === Infinity ? '∞' : a.stock}</td>
                                                        <td className="py-4 text-center text-yellow-500 font-black">{a.commRate}%</td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={()=>setAssets(assets.filter(as=>as.id!==a.id))} className="text-red-500 hover:scale-125 transition-transform"><Icon name="Trash2" size={18}/></button>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Operations (Logic: Returns) */}
                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="RefreshCcw" size={32} /> المرتجعات ومعالجة الطلبات</h2>
                                <div className="grid grid-cols-1 gap-6">
                                    <h3 className="text-xl font-black text-red-500">طلبات المرتجعات (تحتاج قرار)</h3>
                                    {returns.map(r => (
                                        <div key={r.id} className="glass-panel p-6 rounded-[2rem] border-r-4 border-red-500 flex justify-between items-center">
                                            <div><h4 className="font-black">{r.buyer} <small className="text-gray-400">#{r.id}</small></h4><p className="text-sm opacity-70">السبب: {r.reason}</p></div>
                                            <div className="flex gap-2">
                                                <button onClick={()=>processReturn(r.id, true)} className="bg-green-500 text-black px-4 py-2 rounded-xl font-black text-xs">قبول</button>
                                                <button onClick={()=>processReturn(r.id, false)} className="bg-red-500 text-white px-4 py-2 rounded-xl font-black text-xs">رفض</button>
                                            </div>
                                        </div>
                                    ))}
                                    <hr className="border-white/5 my-4" />
                                    <h3 className="text-xl font-black">سجل العمليات الأخير</h3>
                                    {orders.map(o => (
                                        <div key={o.id} className="glass-panel p-6 rounded-[2rem] flex justify-between items-center">
                                            <div><h4 className="font-black">{o.buyer} <small className="text-blue-500">{o.status}</small></h4><p className="text-xs text-gray-500">{o.item}</p></div>
                                            <span className="text-xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing (Logic: Loyalty Config) */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Zap" size={32} /> هندسة العروض ونقاط الولاء</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">نظام نقاط الولاء (Loyalty Matrix)</h3>
                                        <div className="space-y-6">
                                            <div className="flex justify-between items-center">
                                                <span>نقاط مقابل كل $1 شراء</span>
                                                <input type="number" defaultValue="5" className="premium-input w-20 p-2 rounded-lg text-center font-black" />
                                            </div>
                                            <div className="bg-yellow-500/10 p-6 rounded-[2rem] border border-yellow-500/20">
                                                <h4 className="text-yellow-500 font-black mb-1">الرصيد الموزع حالياً</h4>
                                                <p className="text-3xl font-black">{loyaltyPoints.toLocaleString()} <small className="text-xs">نقطة</small></p>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">الخصومات العامة (Global Offers)</h3>
                                        <div className="space-y-6">
                                            <label className="text-xs font-bold text-gray-500 uppercase block">تطبيق خصم عام على كافة الأصول (%)</label>
                                            <div className="flex items-center gap-4">
                                                <input type="range" min="0" max="50" value={globalDiscount} onChange={(e)=>setGlobalDiscount(e.target.value)} className="flex-1 accent-yellow-500" />
                                                <span className="text-2xl font-black text-yellow-500">{globalDiscount}%</span>
                                            </div>
                                            <button onClick={()=>showToast('تم تفعيل الخصومات على واجهة المشتري')} className="w-full py-4 bg-white/5 border border-white/10 rounded-2xl font-black hover:bg-white/10 transition-all">اعتماد العرض الآن ⚡</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Finance (Logic: Installments) */}
                        {activeTab === 'finance' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="CreditCard" size={32} /> إدارة الأقساط والاشتراكات الدورية</h2>
                                {installments.map(i => {
                                    const prog = (i.paid / i.total) * 100;
                                    return (
                                        <div key={i.id} className="glass-panel p-8 rounded-[2.5rem]">
                                            <div className="flex justify-between mb-4">
                                                <h4 className="text-xl font-black">{i.user} - {i.item}</h4>
                                                <span className="text-yellow-500 font-black">تاريخ الاستحقاق: {i.next_due}</span>
                                            </div>
                                            <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden mb-4">
                                                <div className="h-full bg-blue-500 transition-all duration-1000" style={{width: `${prog}%`}}></div>
                                            </div>
                                            <div className="flex justify-between text-xs font-bold text-gray-400">
                                                <span>تم تحصيل: ${i.paid.toLocaleString()}</span>
                                                <span>المتبقي: ${(i.total - i.paid).toLocaleString()}</span>
                                            </div>
                                            <button onClick={()=>collectInstallment(i.id)} className="mt-6 px-6 py-2.5 bg-blue-600 text-white rounded-xl font-black text-xs hover:bg-blue-700 transition-all">تسجيل تحصيل يدوي 💰</button>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ErrorBoundary><App /></ErrorBoundary>);

        function ErrorBoundary({ children }) {
            const [hasError, setHasError] = useState(false);
            if (hasError) return <div className="p-10 text-red-500 font-black text-center h-screen flex items-center justify-center">⚠️ رصد خطأ في الواجهة.. جاري الإصلاح آلياً.</div>;
            return children;
        }
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل آمن ---
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. عرض الواجهة (Render) ---
components.html(final_html, height=1050, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للسوق العالمي (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة لمركز القيادة الرئيسي (Home)"):
        st.switch_page("app.py")
