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

# --- 3. واجهة React المتقدمة (الإصدار 8.0 - المنطق الكامل والتفاعلية القصوى) ---
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
        <h2 style="margin-top:20px;">جاري شحن محرك العمليات الذكي...</h2>
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

        const translations = {
            ar: {
                title: "مركز الإدارة الماسية", marketing: "التسويق والولاء", 
                inventory: "المخزون والأصول", ops: "مركز العمليات", loyalty: "نقاط الولاء",
                offers: "العروض المحدودة", add_asset: "إضافة أصل جديد", delete: "حذف"
            },
            en: {
                title: "Diamond Admin Desk", marketing: "Marketing & Loyalty", 
                inventory: "Inventory & Assets", ops: "Operations Center", loyalty: "Loyalty Points",
                offers: "Flash Offers", add_asset: "Add New Asset", delete: "Delete"
            }
        };

        const App = () => {
            // --- Global State (The Brain) ---
            const [activeTab, setActiveTab] = useState('overview');
            const [lang, setLang] = useState('ar');
            const [toasts, setToasts] = useState([]);
            const [balance, setBalance] = useState(LEADER_BALANCE_PLACEHOLDER);

            // 1. منطق المنتجات والمخزون
            const [assets, setAssets] = useState([
                { id: 1, name: 'برج السيادة الإداري', stock: 5, price: 1500000, discount: 0, status: 'نشط', type: 'عقاري' },
                { id: 2, name: 'منظومة الطاقة X10', stock: 12, price: 12500, discount: 10, status: 'نشط', type: 'منتج' },
                { id: 3, name: 'دبلوم هندسة الأرباح', stock: Infinity, price: 499, discount: 0, status: 'نشط', type: 'رقمي' }
            ]);

            // 2. منطق الطلبات
            const [orders, setOrders] = useState([
                { id: 'ORD-101', buyer: 'أحمد القائد', item: 'منظومة الطاقة X10', amount: 11250, status: 'قيد المعالجة', date: 'اليوم' },
                { id: 'ORD-102', buyer: 'سارة المستثمرة', item: 'دبلوم هندسة الأرباح', amount: 499, status: 'مكتمل', date: 'أمس' }
            ]);

            // 3. منطق المرتجعات
            const [returns, setReturns] = useState([
                { id: 'RET-55', buyer: 'كريم ناصر', item: 'منظومة الطاقة X10', reason: 'عطل فني في البطارية', status: 'منتظر' }
            ]);

            // 4. منطق التقسيط
            const [installments, setInstallments] = useState([
                { id: 'INS-01', user: 'ياسين علي', item: 'برج السيادة', total: 1500000, paid: 500000, next_due: '2026-05-01' }
            ]);

            // --- التنبيهات ---
            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- وظائف منطق الأعمال (Actions) ---
            
            const handleAddAsset = (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const newAsset = {
                    id: Date.now(),
                    name: formData.get('name'),
                    price: parseFloat(formData.get('price')),
                    stock: formData.get('type') === 'رقمي' ? Infinity : parseInt(formData.get('stock')),
                    type: formData.get('type'),
                    discount: 0,
                    status: 'نشط'
                };
                setAssets([newAsset, ...assets]);
                showToast('تم إدراج الأصل الجديد في السجلات الإمبراطورية');
                e.target.reset();
            };

            const deleteAsset = (id) => {
                setAssets(assets.filter(a => a.id !== id));
                showToast('تم حذف الأصل بنجاح', 'warning');
            };

            const toggleAssetStatus = (id) => {
                setAssets(assets.map(a => a.id === id ? {...a, status: a.status === 'نشط' ? 'مخفي' : 'نشط'} : a));
                showToast('تم تحديث حالة الظهور');
            };

            const processOrder = (id, newStatus) => {
                setOrders(orders.map(o => o.id === id ? {...o, status: newStatus} : o));
                if(newStatus === 'مكتمل') showToast('تم تأكيد العملية بنجاح');
                if(newStatus === 'ملغى') showToast('تم إلغاء الطلب وإرجاع السيولة', 'warning');
            };

            const payInstallment = (id) => {
                setInstallments(installments.map(i => {
                    if(i.id === id) {
                        const amount = 100000; // قسط ثابت كمثال
                        showToast(`تم تحصيل قسط بقيمة $${amount.toLocaleString()}`);
                        return {...i, paid: i.paid + amount};
                    }
                    return i;
                }));
            };

            const updateDiscount = (id, val) => {
                setAssets(assets.map(a => a.id === id ? {...a, discount: parseInt(val)} : a));
            };

            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            const t = translations[lang] || translations['ar'];
            const isRTL = lang === 'ar';

            return (
                <div className="min-h-screen bg-[#030303] text-white flex flex-col md:flex-row overflow-hidden transition-all duration-500">
                    
                    {/* --- Sidebar --- */}
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10">
                        <div className="p-8 pb-6">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-[0_0_20px_rgba(255,215,0,0.3)]"><Icon name="Zap" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Logic Hub v8.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار'},
                                {id: 'inventory', icon: 'Box', label: t.inventory},
                                {id: 'operations', icon: 'Activity', label: t.ops},
                                {id: 'marketing', icon: 'Megaphone', label: t.marketing},
                                {id: 'finance', icon: 'CreditCard', label: 'المالية'}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Area --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview (Dynamic KPIs) */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500">
                                        <small className="text-gray-500 font-bold uppercase">صافي الأرباح</small>
                                        <h4 className="text-3xl font-black text-green-500">$2.4M</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">الطلبات النشطة</small>
                                        <h4 className="text-3xl font-black">{orders.filter(o=>o.status!=='مكتمل').length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-red-500">
                                        <small className="text-gray-500 font-bold uppercase">المرتجعات</small>
                                        <h4 className="text-3xl font-black text-red-500">{returns.length}</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">إجمالي الأصول</small>
                                        <h4 className="text-3xl font-black">{assets.length}</h4>
                                    </div>
                                </div>

                                <div className="glass-panel p-8 rounded-[2.5rem]">
                                    <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="Clock" /> السجل اللحظي للعمليات</h3>
                                    <div className="space-y-4">
                                        {orders.slice(0, 3).map(o => (
                                            <div key={o.id} className="flex justify-between items-center p-4 bg-white/5 rounded-2xl">
                                                <div className="flex items-center gap-4">
                                                    <div className={`w-2 h-2 rounded-full ${o.status==='مكتمل'?'bg-green-500':'bg-yellow-500'}`}></div>
                                                    <span className="font-bold">{o.buyer} اشتري {o.item}</span>
                                                </div>
                                                <span className="text-gray-500 text-xs">{o.date}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (Logic: Add/Delete/Toggle) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <div className="flex flex-col lg:flex-row gap-8">
                                    {/* Form */}
                                    <div className="lg:w-1/3 glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">إضافة أصل استراتيجي</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="اسم المنتج..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <input name="price" type="number" placeholder="السعر ($)..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black">
                                                <option>منتج</option>
                                                <option>عقاري</option>
                                                <option>رقمي</option>
                                            </select>
                                            <input name="stock" type="number" placeholder="الكمية..." className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <button type="submit" className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all">إدراج الأصل 🚀</button>
                                        </form>
                                    </div>

                                    {/* List */}
                                    <div className="lg:w-2/3 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد المخزون الحالي</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-xs border-b border-white/5 uppercase">
                                                    <th className="pb-4 text-right">الأصل</th>
                                                    <th className="pb-4 text-center">المخزون</th>
                                                    <th className="pb-4 text-center">السعر</th>
                                                    <th className="pb-4 text-center">الحالة</th>
                                                    <th className="pb-4 text-center">إجراء</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all">
                                                        <td className="py-4 font-bold">{a.name} <br/><small className="text-gray-500">{a.type}</small></td>
                                                        <td className="py-4 text-center font-black">{a.stock === Infinity ? '∞' : a.stock}</td>
                                                        <td className="py-4 text-center text-green-500 font-black">${a.price.toLocaleString()}</td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={() => toggleAssetStatus(a.id)} className={`px-3 py-1 rounded-lg text-[10px] font-black ${a.status==='نشط'?'bg-green-500/20 text-green-500':'bg-gray-500/20 text-gray-500'}`}>{a.status}</button>
                                                        </td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={() => deleteAsset(a.id)} className="text-red-500 hover:scale-125 transition-transform"><Icon name="Trash2" size={18}/></button>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Operations (Logic: Process/Returns) */}
                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="RefreshCcw" size={32} /> مركز معالجة العمليات والمرتجعات</h2>
                                <div className="grid grid-cols-1 gap-6">
                                    {orders.map(o => (
                                        <div key={o.id} className="glass-panel p-6 rounded-[2rem] flex flex-col md:flex-row justify-between items-center gap-6">
                                            <div>
                                                <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{o.id}</span>
                                                <h3 className="text-xl font-black">{o.buyer} <small className="text-xs text-blue-500 ml-2">{o.status}</small></h3>
                                                <p className="text-sm text-gray-400 italic">اقتناء: {o.item}</p>
                                            </div>
                                            <div className="flex items-center gap-4">
                                                <span className="text-xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                                {o.status === 'قيد المعالجة' && (
                                                    <div className="flex gap-2">
                                                        <button onClick={() => processOrder(o.id, 'مكتمل')} className="bg-green-500 text-black px-4 py-2 rounded-xl font-black text-xs">اعتماد</button>
                                                        <button onClick={() => processOrder(o.id, 'ملغى')} className="bg-red-500 text-white px-4 py-2 rounded-xl font-black text-xs">إلغاء</button>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="mt-12">
                                    <h3 className="text-2xl font-black mb-6 text-red-500">طلبات المرتجعات النشطة</h3>
                                    {returns.map(r => (
                                        <div key={r.id} className="glass-panel p-6 rounded-[2rem] border-r-4 border-red-500 mb-4 flex justify-between items-center">
                                            <div>
                                                <h4 className="font-black">{r.buyer}</h4>
                                                <p className="text-sm text-gray-400">السبب: {r.reason}</p>
                                            </div>
                                            <button onClick={() => { setReturns(returns.filter(re=>re.id!==r.id)); showToast('تم تسوية المرتجع بنجاح'); }} className="bg-white/5 border border-white/10 px-4 py-2 rounded-xl font-black text-xs">تسوية العملية</button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing (Logic: Global Discount Sync) */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="TrendingUp" size={32} /> هندسة الخصومات والنقاط</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">التحكم الفوري في الخصومات</h3>
                                        <div className="space-y-6">
                                            {assets.slice(0, 3).map(a => (
                                                <div key={a.id} className="flex justify-between items-center">
                                                    <span className="font-bold">{a.name}</span>
                                                    <div className="flex items-center gap-3">
                                                        <input 
                                                            type="range" min="0" max="50" value={a.discount} 
                                                            onChange={(e) => updateDiscount(a.id, e.target.value)} 
                                                            className="accent-yellow-500" 
                                                        />
                                                        <span className="text-yellow-500 font-black w-8">{a.discount}%</span>
                                                    </div>
                                                </div>
                                            ))}
                                            <button onClick={() => showToast('تم تعميم الخصومات على المتجر العالمي')} className="w-full py-4 bg-white/5 border border-white/10 rounded-xl font-black hover:bg-white/10 transition-all">حفظ وتعميم الخصومات 💾</button>
                                        </div>
                                    </div>

                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6">نظام نقاط الولاء</h3>
                                        <div className="space-y-6">
                                            <div className="flex justify-between items-center">
                                                <span>نقاط لكل 1$ شراء</span>
                                                <input type="number" defaultValue="5" className="premium-input w-20 p-2 rounded-lg text-center font-black" />
                                            </div>
                                            <div className="bg-yellow-500/10 p-6 rounded-[1.5rem] border border-yellow-500/20">
                                                <h4 className="font-black text-yellow-500 mb-2">إحصائية الولاء</h4>
                                                <p className="text-sm opacity-70">إجمالي النقاط الموزعة في شبكتك: 1,240,500 نقطة</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Finance (Logic: Installments Progress) */}
                        {activeTab === 'finance' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="CreditCard" size={32} /> إدارة الأقساط والاشتراكات</h2>
                                {installments.map(ins => {
                                    const prog = (ins.paid / ins.total) * 100;
                                    return (
                                        <div key={ins.id} className="glass-panel p-8 rounded-[2.5rem]">
                                            <div className="flex justify-between mb-4">
                                                <h4 className="text-xl font-black">{ins.user} - {ins.item}</h4>
                                                <span className="text-yellow-500 font-black">القسط القادم: {ins.next_due}</span>
                                            </div>
                                            <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden mb-4">
                                                <div className="h-full bg-blue-500 transition-all duration-1000" style={{width: `${prog}%`}}></div>
                                            </div>
                                            <div className="flex justify-between text-xs font-bold text-gray-400">
                                                <span>تم سداد: ${ins.paid.toLocaleString()}</span>
                                                <span>المتبقي: ${(ins.total - ins.paid).toLocaleString()}</span>
                                            </div>
                                            <button onClick={() => payInstallment(ins.id)} className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg font-black text-xs hover:bg-blue-700 transition-all shadow-lg">تسجيل دفعة جديدة 💰</button>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                    </div>
                    
                    {/* --- Toasts Container --- */}
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
            if (hasError) return <div className="p-10 text-red-500 font-black text-center">⚠️ حدث خطأ تقني.. جاري إعادة المزامنة..</div>;
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
