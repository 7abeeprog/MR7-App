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

# --- 3. واجهة React المتقدمة (الإصدار 12.0 - النظام الشامل للسيادة الاقتصادية) ---
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

        .pulse-gold { animation: pulse-gold-anim 2s infinite; }
        @keyframes pulse-gold-anim {
            0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
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
        <div style="border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <h2 style="margin-top:20px; font-weight: 900; letter-spacing: 2px;">MR7 ECONOMIC BRAIN</h2>
        <p style="color: #666; font-size: 12px; margin-top: 10px;">Initializing Sovereign Systems v12.0</p>
    </div>

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

        // --- المكونات المساعدة (Guarded Components) ---
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
            const [balance, setBalance] = useState(Number(LEADER_BALANCE_PLACEHOLDER));

            // --- 1. محرك الأصول والمخزون (Assets Engine) ---
            const [assets, setAssets] = useState([
                { id: 1, name: 'برج السيادة الإداري', stock: 5, price: 1500000, type: 'عقاري', commRates: [10, 5, 2, 1, 1, 1, 1, 1, 1, 1], discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400', desc: 'تحفة معمارية للقيادة.' },
                { id: 2, name: 'دبلوم هندسة الأرباح', stock: Infinity, price: 499, type: 'رقمي', commRates: [15, 7, 3, 1, 1, 1, 1, 1, 1, 1], discount: 0, status: 'نشط', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400', desc: 'صناعة عقول التريليون.' }
            ]);

            // --- 2. محرك العمليات والمرتجعات (Operations Engine) ---
            const [orders, setOrders] = useState([
                { id: 'ORD-202', buyer: 'أحمد القائد', item: 'منظومة طاقة X10', amount: 12500, status: 'قيد المعالجة', date: 'اليوم' }
            ]);
            const [returns, setReturns] = useState([
                { id: 'RET-05', buyer: 'سارة خالد', item: 'دبلوم هندسة الأرباح', reason: 'طلب استبدال مسار', status: 'منتظر' }
            ]);

            // --- 3. المحرك المالي (Finance Engine: Installments & Subs) ---
            const [installments, setInstallments] = useState([
                { id: 'INS-01', user: 'ياسين علي', item: 'برج السيادة', total: 1500000, paid: 500000, next_due: '2026-05-01' }
            ]);
            const [subscriptions, setSubscriptions] = useState([
                { id: 'SUB-10', user: 'مجموعة النبت', plan: 'دعم تقني نخبوي', price: 1500, status: 'نشط' }
            ]);

            // --- 4. محرك التسويق والولاء (Marketing & Loyalty) ---
            const [loyaltyPoints, setLoyaltyPoints] = useState(124500);
            const [flashOffers, setFlashOffers] = useState([
                { id: 1, assetName: 'برج السيادة', discount: 10, timeLeft: '02:15:45' }
            ]);

            // --- التنبيهات (Reminders) ---
            const reminders = useMemo(() => [
                { id: 1, text: `تنبيه: قسط مستحق لـ ${installments[0].user}`, priority: 'high' },
                { id: 2, text: `مخزون 'برج السيادة' منخفض جداً (${assets[0].stock})`, priority: 'medium' }
            ], [installments, assets]);

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- وظائف المنطق التفاعلي (Business Actions) ---
            
            const handleAddAsset = (e) => {
                e.preventDefault();
                const f = new FormData(e.target);
                const customComm = Array.from({length: 10}).map((_, i) => parseFloat(f.get(`c${i+1}`) || 0));
                const n = {
                    id: Date.now(),
                    name: f.get('name'), price: parseFloat(f.get('price')),
                    commRates: customComm,
                    stock: f.get('type') === 'رقمي' ? Infinity : parseInt(f.get('stock')),
                    type: f.get('type'), img: f.get('img'), desc: f.get('desc'), status: 'نشط', discount: 0
                };
                setAssets([n, ...assets]);
                showToast('تم إدراج الأصل وتوثيقه في السجلات');
                e.target.reset();
            };

            const confirmOrder = (id) => {
                setOrders(orders.map(o => o.id === id ? {...o, status: 'مكتمل'} : o));
                setLoyaltyPoints(prev => prev + 500);
                showToast('تم تأكيد العملية وتوزيع نقاط الولاء');
            };

            const payInstallment = (id) => {
                setInstallments(installments.map(i => i.id === id ? {...i, paid: i.paid + 100000} : i));
                showToast('تم تحصيل دفعة بقيمة $100,000');
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar (Navigation Hub) --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10 shadow-2xl">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-xl"><Icon name="Cpu" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">العقل الاقتصادي</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Enterprise Engine v12.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار الاستراتيجي'},
                                {id: 'inventory', icon: 'Box', label: 'الأصول والمخزون'},
                                {id: 'operations', icon: 'Activity', label: 'مركز العمليات'},
                                {id: 'finance', icon: 'CreditCard', label: 'المجمع المالي'},
                                {id: 'marketing', icon: 'Zap', label: 'التسويق والولاء'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500 shadow-md' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Arena --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview (Intelligence & Reminders) */}
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
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-red-500 pulse-gold">
                                        <small className="text-gray-500 font-bold uppercase">تنبيهات حرجة</small>
                                        <h4 className="text-3xl font-black text-red-500">{reminders.length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">رصيد الولاء</small>
                                        <h4 className="text-3xl font-black text-blue-500">{loyaltyPoints.toLocaleString()}</h4>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[3rem]">
                                        <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="Bell" className="text-yellow-500"/> التنبيهات والمهام العاجلة</h3>
                                        <div className="space-y-4">
                                            {reminders.map(rem => (
                                                <div key={rem.id} className={`p-4 rounded-2xl border flex justify-between items-center ${rem.priority === 'high' ? 'bg-red-500/10 border-red-500/20 text-red-500' : 'bg-yellow-500/10 border-yellow-500/20 text-yellow-500'}`}>
                                                    <span className="font-bold">{rem.text}</span>
                                                    <button onClick={()=>showToast('جاري معالجة التنبيه...')} className="bg-white/10 px-3 py-1 rounded-lg text-[10px] font-black uppercase">معالجة</button>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="glass-panel p-8 rounded-[3rem] bg-gradient-to-br from-yellow-500/5 to-transparent">
                                        <h3 className="text-2xl font-black mb-6 flex items-center gap-3"><Icon name="Zap" className="text-yellow-500"/> عروض الصاعقة النشطة</h3>
                                        {flashOffers.map(offer => (
                                            <div key={offer.id} className="p-6 bg-black/40 rounded-2xl border border-yellow-500/30">
                                                <div className="flex justify-between items-center">
                                                    <div>
                                                        <h4 className="text-xl font-black">{offer.assetName}</h4>
                                                        <span className="text-green-500 font-black">خصم نخبوي {offer.discount}%</span>
                                                    </div>
                                                    <div className="text-center">
                                                        <small className="text-gray-500 block font-bold">ينتهي خلال</small>
                                                        <span className="text-2xl font-black text-yellow-500 tabular-nums">{offer.timeLeft}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (Logic CRUD with 10 Levels & Images) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col xl:flex-row gap-8">
                                    {/* Asset Creation Form */}
                                    <div className="xl:w-2/5 glass-panel p-8 rounded-[2.5rem] h-fit">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="PlusCircle" className="text-yellow-500"/> هندسة أصل جديد</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="اسم الأصل الاستراتيجي..." required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="price" type="number" placeholder="القيمة ($)" required className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black text-sm">
                                                    <option>عقاري</option><option>منتج</option><option>رقمي</option>
                                                </select>
                                            </div>
                                            <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                                                <label className="text-[10px] font-black text-gray-500 uppercase block mb-3">خارطة عمولات الأجيال (10 مستويات %)</label>
                                                <div className="grid grid-cols-5 gap-2">
                                                    {Array.from({length: 10}).map((_, i) => (
                                                        <input key={i} name={`c${i+1}`} type="number" defaultValue="1" className="premium-input p-2 rounded-lg text-center text-xs font-bold" title={`مستوى ${i+1}`} />
                                                    ))}
                                                </div>
                                            </div>
                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="stock" type="number" placeholder="الكمية" className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                                <input name="img" placeholder="رابط الصورة..." className="w-full premium-input p-4 rounded-xl font-bold text-sm" />
                                            </div>
                                            <textarea name="desc" placeholder="وصف الأصل..." className="w-full premium-input p-4 rounded-xl font-bold h-20 text-sm"></textarea>
                                            <button type="submit" className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all">نشر الأصل في الإمبراطورية 🚀</button>
                                        </form>
                                    </div>

                                    {/* Inventory Table */}
                                    <div className="xl:w-3/5 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد الأصول الموثقة</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-xs border-b border-white/5 uppercase">
                                                    <th className="pb-4 text-right">الأصل</th>
                                                    <th className="pb-4 text-center">المخزون</th>
                                                    <th className="pb-4 text-center">القيمة</th>
                                                    <th className="pb-4 text-center">إجراء</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all group">
                                                        <td className="py-4 flex items-center gap-4">
                                                            <img src={a.img} className="w-12 h-12 rounded-xl object-cover" />
                                                            <div><div className="font-bold text-sm">{a.name}</div><small className="text-[10px] text-gray-500">{a.type}</small></div>
                                                        </td>
                                                        <td className="py-4 text-center font-black">
                                                            {a.stock === Infinity ? <span className="text-green-500 text-lg">∞</span> : a.stock}
                                                        </td>
                                                        <td className="py-4 text-center text-[#00FF88] font-black">${a.price.toLocaleString()}</td>
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

                        {/* Tab: Operations (Processing & Returns) */}
                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="RefreshCcw" size={32} /> مركز معالجة العمليات والمرتجعات</h2>
                                <div className="space-y-6">
                                    <h3 className="text-xl font-black text-red-500 flex items-center gap-2"><Icon name="AlertCircle" size={18}/> المرتجعات بانتظار القرار</h3>
                                    {returns.map(r => (
                                        <div key={r.id} className="glass-panel p-6 rounded-[2rem] border-r-4 border-red-500 flex justify-between items-center">
                                            <div>
                                                <h4 className="font-black text-xl">{r.buyer} <small className="text-gray-400 font-bold">#{r.id}</small></h4>
                                                <p className="text-sm opacity-70">المنتج: {r.item} | السبب: {r.reason}</p>
                                            </div>
                                            <div className="flex gap-2">
                                                <button onClick={()=>{setReturns(returns.filter(re=>re.id!==r.id)); showToast('تم قبول المرتجع');}} className="bg-green-500 text-black px-5 py-2 rounded-xl font-black text-xs">قبول</button>
                                                <button onClick={()=>{setReturns(returns.filter(re=>re.id!==r.id)); showToast('تم رفض المرتجع', 'warning');}} className="bg-red-500 text-white px-5 py-2 rounded-xl font-black text-xs">رفض</button>
                                            </div>
                                        </div>
                                    ))}
                                    <hr className="border-white/5" />
                                    <h3 className="text-xl font-black">الطلبات الواردة</h3>
                                    {orders.map(o => (
                                        <div key={o.id} className="glass-panel p-6 rounded-[2rem] flex justify-between items-center">
                                            <div className="flex items-center gap-5">
                                                <div className="p-4 bg-yellow-500/10 text-yellow-500 rounded-2xl"><Icon name="FileText" size={24}/></div>
                                                <div>
                                                    <h4 className="font-black text-xl">{o.buyer} <small className="text-blue-500 text-xs font-bold mr-2">{o.status}</small></h4>
                                                    <p className="text-sm text-gray-500">{o.item} • {o.date}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-6">
                                                <span className="text-2xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                                {o.status === 'قيد المعالجة' && <button onClick={()=>confirmOrder(o.id)} className="bg-yellow-500 text-black px-6 py-2.5 rounded-xl font-black text-xs hover:scale-105 transition-transform">اعتماد وتوزيع العمولات</button>}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Finance (Installments & Subs) */}
                        {activeTab === 'finance' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="CreditCard" size={32} /> المحرك المالي والاشتراكات</h2>
                                <div className="grid grid-cols-1 gap-6">
                                    <h3 className="text-xl font-black text-blue-500">متابعة الأقساط والتحصيل</h3>
                                    {installments.map(i => {
                                        const prog = (i.paid / i.total) * 100;
                                        return (
                                            <div key={i.id} className="glass-panel p-8 rounded-[2.5rem] relative overflow-hidden">
                                                <div className="flex justify-between mb-4 relative z-10">
                                                    <div>
                                                        <h4 className="text-xl font-black">{i.user} - {i.item}</h4>
                                                        <span className="text-xs text-gray-500 font-bold uppercase tracking-widest">{i.id}</span>
                                                    </div>
                                                    <span className="text-yellow-500 font-black">القسط التالي: {i.next_due}</span>
                                                </div>
                                                <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden mb-4 relative z-10">
                                                    <div className="h-full bg-blue-500 transition-all duration-1000 shadow-[0_0_15px_rgba(59,130,246,0.5)]" style={{width: `${prog}%`}}></div>
                                                </div>
                                                <div className="flex justify-between text-xs font-bold text-gray-400 relative z-10">
                                                    <span>تم تحصيل: ${i.paid.toLocaleString()}</span>
                                                    <span>المتبقي: ${(i.total - i.paid).toLocaleString()}</span>
                                                </div>
                                                <button onClick={()=>payInstallment(i.id)} className="mt-6 px-6 py-2.5 bg-blue-600 text-white rounded-xl font-black text-xs hover:bg-blue-700 transition-all shadow-lg relative z-10">تحصيل دفعة يدوية 💰</button>
                                            </div>
                                        );
                                    })}
                                    
                                    <h3 className="text-xl font-black text-green-500 mt-8">الاشتراكات الدورية النشطة</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {subscriptions.map(s => (
                                            <div key={s.id} className="glass-panel p-6 rounded-[2rem] border-l-4 border-green-500 flex justify-between items-center">
                                                <div>
                                                    <h4 className="font-black">{s.user}</h4>
                                                    <p className="text-xs text-gray-400">{s.plan}</p>
                                                </div>
                                                <span className="text-xl font-black text-white">${s.price.toLocaleString()}<small className="text-[10px] text-gray-500">/شهر</small></span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing (Discounts & Loyalty Points Config) */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto pt-5">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Zap" size={32} /> هندسة الولاء والعروض</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[3rem]">
                                        <h3 className="text-xl font-black mb-6">نظام نقاط الولاء السيادي</h3>
                                        <div className="space-y-6">
                                            <div className="flex justify-between items-center">
                                                <span>نقاط مقابل كل $1 ضخ مالي</span>
                                                <input type="number" defaultValue="5" className="premium-input w-20 p-2 rounded-lg text-center font-black" />
                                            </div>
                                            <div className="bg-yellow-500/10 p-6 rounded-[2rem] border border-yellow-500/20 text-center">
                                                <h4 className="text-yellow-500 font-black mb-2">إجمالي النقاط الموزعة</h4>
                                                <p className="text-4xl font-black">{loyaltyPoints.toLocaleString()}</p>
                                            </div>
                                            <button onClick={()=>showToast('تم حفظ إعدادات نظام الولاء')} className="w-full py-4 bg-white/5 border border-white/10 rounded-2xl font-black hover:bg-white/10 transition-all">تحديث محرك المكافآت 💾</button>
                                        </div>
                                    </div>
                                    <div className="glass-panel p-8 rounded-[3rem]">
                                        <h3 className="text-xl font-black mb-6">إدارة الخصومات والندرة</h3>
                                        <div className="space-y-6">
                                            <div className="p-4 bg-red-500/10 rounded-2xl border border-red-500/20">
                                                <h4 className="text-red-500 font-black mb-2">تفعيل عرض صاعق (Flash Offer)</h4>
                                                <select className="w-full premium-input p-3 rounded-xl bg-black mb-3">
                                                    {assets.map(a => <option key={a.id}>{a.name}</option>)}
                                                </select>
                                                <div className="grid grid-cols-2 gap-2">
                                                    <input type="number" placeholder="الخصم %" className="premium-input p-3 rounded-xl" />
                                                    <input type="number" placeholder="المدة (ساعة)" className="premium-input p-3 rounded-xl" />
                                                </div>
                                                <button onClick={()=>showToast('تم إطلاق العرض الصاعق بنجاح')} className="w-full mt-4 py-3 bg-red-500 text-white rounded-xl font-black text-sm hover:brightness-110 transition-all">إطلاق العرض الآن ⚡</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                    </div>

                    {/* --- Toasts Center --- */}
                    <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map(t => (
                            <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : 'bg-black/90 border-yellow-500/40 text-yellow-500'}`}>
                                <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                                <span className="font-bold text-sm text-white">{t.msg}</span>
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
