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

# --- 3. واجهة React المتقدمة (الإصدار 9.0 - المنطق الكامل للأصول والعمولات) ---
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
        <h2 style="margin-top:20px;">جاري تشغيل محرك الأصول والعمولات...</h2>
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
            const [activeTab, setActiveTab] = useState('overview');
            const [lang, setLang] = useState('ar');
            const [toasts, setToasts] = useState([]);
            const [balance, setBalance] = useState(LEADER_BALANCE_PLACEHOLDER);

            // --- 1. قاعدة بيانات الأصول (Logic: Assets Data) ---
            const [assets, setAssets] = useState([
                { 
                    id: 1, name: 'برج السيادة الإداري', stock: 5, price: 1500000, 
                    discount: 0, status: 'نشط', type: 'عقاري', commRate: 10,
                    img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400',
                    desc: 'برج إداري متكامل في العاصمة الإدارية الجديدة، مصمم ليكون المقر الرئيسي لقادة المنطقة.'
                },
                { 
                    id: 2, name: 'منظومة الطاقة X10', stock: 12, price: 12500, 
                    discount: 10, status: 'نشط', type: 'منتج', commRate: 15,
                    img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=400',
                    desc: 'محطة طاقة شمسية ذكية متنقلة توفر استدامة كاملة للمشاريع الميدانية.'
                },
                { 
                    id: 3, name: 'دبلوم هندسة الأرباح', stock: Infinity, price: 499, 
                    discount: 0, status: 'نشط', type: 'رقمي', commRate: 20,
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400',
                    desc: 'المنهج التعليمي الأقوى لبناء العقلية القيادية واستثمار الأجيال.'
                }
            ]);

            // --- 2. محرك العمليات (Logic: Orders) ---
            const [orders, setOrders] = useState([
                { id: 'ORD-101', buyer: 'أحمد القائد', item: 'منظومة الطاقة X10', amount: 11250, status: 'قيد المعالجة', date: 'اليوم' }
            ]);

            const showToast = (msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };

            // --- وظائف منطق الأعمال المحدثة ---
            
            const handleAddAsset = (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const newAsset = {
                    id: Date.now(),
                    name: formData.get('name'),
                    price: parseFloat(formData.get('price')),
                    commRate: parseFloat(formData.get('commRate')),
                    stock: formData.get('type') === 'رقمي' ? Infinity : parseInt(formData.get('stock')),
                    type: formData.get('type'),
                    img: formData.get('img') || 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400',
                    desc: formData.get('desc'),
                    discount: 0,
                    status: 'نشط'
                };
                setAssets([newAsset, ...assets]);
                showToast('تم إدراج الأصل الريادي بنظام العمولة المخصص');
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
                if(newStatus === 'مكتمل') showToast('تم اعتماد العملية وتوزيع العمولات');
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
                    <div className="w-full md:w-72 md:min-h-screen bg-[rgba(15,15,15,0.95)] border-b md:border-b-0 md:border-l border-white/10 flex flex-col z-10 shadow-2xl">
                        <div className="p-8 pb-6 text-center md:text-right">
                            <div className="bg-yellow-500 text-black p-3 rounded-2xl inline-block mb-4 shadow-[0_0_20px_rgba(255,215,0,0.4)]"><Icon name="Target" size={30} /></div>
                            <h1 className="text-xl font-black text-yellow-500 uppercase tracking-tighter">{t.title}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">MR7 Asset Engine v9.0</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-1 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: 'الرادار'},
                                {id: 'inventory', icon: 'Box', label: t.inventory},
                                {id: 'operations', icon: 'Zap', label: t.ops},
                                {id: 'marketing', icon: 'Megaphone', label: t.marketing}
                            ].map(btn => (
                                <button key={btn.id} onClick={() => setActiveTab(btn.id)} className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all whitespace-nowrap ${activeTab === btn.id ? 'bg-white/5 border-r-4 border-yellow-500 text-yellow-500 shadow-lg' : 'text-gray-500 hover:text-white'}`}>
                                    <Icon name={btn.icon} size={18} /> {btn.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Area --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir">
                        
                        {/* Tab: Overview */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-yellow-500">
                                        <small className="text-gray-500 font-bold uppercase">إجمالي العمولات الموزعة</small>
                                        <h4 className="text-3xl font-black text-yellow-500">$142,500</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-green-500">
                                        <small className="text-gray-500 font-bold uppercase">صافي المبيعات</small>
                                        <h4 className="text-3xl font-black text-green-500">$2.1M</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-blue-500">
                                        <small className="text-gray-500 font-bold uppercase">شركاء النجاح</small>
                                        <h4 className="text-3xl font-black">1,547</h4>
                                    </div>
                                    <div className="glass-panel p-6 rounded-[2rem] border-t-4 border-purple-500">
                                        <small className="text-gray-500 font-bold uppercase">إجمالي الأصول</small>
                                        <h4 className="text-3xl font-black">{assets.length}</h4>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    <div className="glass-panel p-8 rounded-[2.5rem]">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="TrendingUp" className="text-green-500" /> الأصول الأكثر ربحية</h3>
                                        <div className="space-y-4">
                                            {assets.slice(0, 3).map(a => (
                                                <div key={a.id} className="flex justify-between items-center bg-white/5 p-4 rounded-2xl border border-white/5">
                                                    <div className="flex items-center gap-3">
                                                        <img src={a.img} className="w-10 h-10 rounded-lg object-cover" />
                                                        <span className="font-bold">{a.name}</span>
                                                    </div>
                                                    <span className="text-[#00FF88] font-black">{a.commRate}% عمولة</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    
                                    <div className="glass-panel p-8 rounded-[2.5rem] bg-gradient-to-br from-yellow-500/10 to-transparent border-yellow-500/20">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="Award" className="text-yellow-500" /> توصية المحرك</h3>
                                        <p className="text-gray-400 font-medium leading-relaxed italic">
                                            "بناءً على طلب السوق الحالي، نقترح رفع عمولة 'منظومة الطاقة X10' بنسبة 2% لتحفيز شركاء النجاح في إقليم ليبيا ومصر خلال الـ 48 ساعة القادمة."
                                        </p>
                                        <button className="mt-8 bg-yellow-500 text-black px-6 py-2.5 rounded-xl font-black text-sm">تطبيق التوصية ✅</button>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Inventory (CRUD with Description, Image, Commission) */}
                        {activeTab === 'inventory' && (
                            <div className="animate-view space-y-8 max-w-7xl mx-auto">
                                <div className="flex flex-col xl:flex-row gap-8">
                                    {/* Form: Add Asset */}
                                    <div className="xl:w-1/3 glass-panel p-8 rounded-[2.5rem] sticky top-0 h-fit">
                                        <h3 className="text-xl font-black mb-6 flex items-center gap-3"><Icon name="PlusCircle" className="text-yellow-500"/> هندسة أصل جديد</h3>
                                        <form onSubmit={handleAddAsset} className="space-y-4">
                                            <input name="name" placeholder="اسم الأصل الاستراتيجي..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <div className="grid grid-cols-2 gap-3">
                                                <input name="price" type="number" placeholder="القيمة ($)..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                                <input name="commRate" type="number" placeholder="العمولة %..." required className="w-full premium-input p-4 rounded-xl font-bold" />
                                            </div>
                                            <div className="grid grid-cols-2 gap-3">
                                                <select name="type" className="w-full premium-input p-4 rounded-xl font-bold bg-black">
                                                    <option>منتج</option>
                                                    <option>عقاري</option>
                                                    <option>رقمي</option>
                                                </select>
                                                <input name="stock" type="number" placeholder="الكمية..." className="w-full premium-input p-4 rounded-xl font-bold" />
                                            </div>
                                            <input name="img" placeholder="رابط صورة الأصل (URL)..." className="w-full premium-input p-4 rounded-xl font-bold" />
                                            <textarea name="desc" placeholder="وصف القيمة المضافة للأصل..." required className="w-full premium-input p-4 rounded-xl font-bold min-h-[100px]"></textarea>
                                            
                                            <button type="submit" className="w-full py-4 bg-yellow-500 text-black rounded-xl font-black text-lg hover:scale-105 transition-all shadow-xl">إدراج الأصل في السوق 🚀</button>
                                        </form>
                                    </div>

                                    {/* List: Inventory Table */}
                                    <div className="xl:w-2/3 glass-panel p-8 rounded-[2.5rem] overflow-x-auto no-scrollbar">
                                        <h3 className="text-xl font-black mb-6">جرد الأصول الموثقة</h3>
                                        <table className="w-full text-dir">
                                            <thead>
                                                <tr className="text-gray-500 text-xs border-b border-white/5 uppercase">
                                                    <th className="pb-4 text-right">الأصل</th>
                                                    <th className="pb-4 text-center">المخزون</th>
                                                    <th className="pb-4 text-center">العمولة</th>
                                                    <th className="pb-4 text-center">القيمة</th>
                                                    <th className="pb-4 text-center">الحالة</th>
                                                    <th className="pb-4 text-center">إجراء</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {assets.map(a => (
                                                    <tr key={a.id} className="border-b border-white/5 hover:bg-white/5 transition-all group">
                                                        <td className="py-4 flex items-center gap-4">
                                                            <div className="w-14 h-14 rounded-xl overflow-hidden border border-white/10 group-hover:border-yellow-500/50 transition-colors">
                                                                <img src={a.img} className="w-full h-full object-cover" />
                                                            </div>
                                                            <div>
                                                                <div className="font-bold text-sm">{a.name}</div>
                                                                <div className="text-[10px] text-gray-500 line-clamp-1 max-w-[150px]">{a.desc}</div>
                                                            </div>
                                                        </td>
                                                        <td className="py-4 text-center font-black">{a.stock === Infinity ? '∞' : a.stock}</td>
                                                        <td className="py-4 text-center text-yellow-500 font-black">{a.commRate}%</td>
                                                        <td className="py-4 text-center text-green-500 font-black">${a.price.toLocaleString()}</td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={() => toggleAssetStatus(a.id)} className={`px-3 py-1 rounded-lg text-[10px] font-black ${a.status==='نشط'?'bg-green-500/20 text-green-500':'bg-gray-500/20 text-gray-500'}`}>{a.status}</button>
                                                        </td>
                                                        <td className="py-4 text-center">
                                                            <button onClick={() => deleteAsset(a.id)} className="text-gray-600 hover:text-red-500 transition-colors p-2"><Icon name="Trash2" size={18}/></button>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: Operations */}
                        {activeTab === 'operations' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black flex items-center gap-4"><Icon name="Zap" className="text-blue-500" size={32} /> مركز معالجة العمليات والطلبات</h2>
                                <div className="space-y-4">
                                    {orders.map(o => (
                                        <div key={o.id} className="glass-panel p-6 rounded-[2rem] flex flex-col md:flex-row justify-between items-center gap-6">
                                            <div className="flex items-center gap-5">
                                                <div className="p-4 bg-blue-500/10 text-blue-500 rounded-2xl"><Icon name="PackageCheck" size={24}/></div>
                                                <div>
                                                    <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{o.id} • {o.date}</span>
                                                    <h3 className="text-xl font-black">{o.buyer} <small className="text-xs bg-yellow-500/20 text-yellow-500 px-2 py-0.5 rounded-lg ml-2">{o.status}</small></h3>
                                                    <p className="text-sm text-gray-400 italic">اقتناء: {o.item}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-6">
                                                <span className="text-2xl font-black text-[#00FF88]">${o.amount.toLocaleString()}</span>
                                                {o.status === 'قيد المعالجة' && (
                                                    <div className="flex gap-2">
                                                        <button onClick={() => processOrder(o.id, 'مكتمل')} className="bg-green-500 text-black px-6 py-2.5 rounded-xl font-black text-xs hover:scale-105 transition-transform">اعتماد العملية</button>
                                                        <button onClick={() => processOrder(o.id, 'ملغى')} className="bg-red-500 text-white px-6 py-2.5 rounded-xl font-black text-xs hover:bg-red-600">إلغاء</button>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Tab: Marketing */}
                        {activeTab === 'marketing' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto text-center py-20">
                                <Icon name="Sparkles" size={60} className="mx-auto text-yellow-500 mb-6" />
                                <h2 className="text-3xl font-black">أدوات التسويق والولاء</h2>
                                <p className="text-gray-500 max-w-xl mx-auto">سيتم تفعيل نظام "هندسة العروض" و "توزيع نقاط الولاء" بشكل كامل عند ربط قاعدة البيانات السحابية المركزية في التحديث القادم.</p>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                                    <div className="glass-panel p-8 rounded-[2rem] border-dashed border-white/20 opacity-50">نظام الخصومات المؤقتة</div>
                                    <div className="glass-panel p-8 rounded-[2rem] border-dashed border-white/20 opacity-50">مولد كوبونات الشركاء</div>
                                    <div className="glass-panel p-8 rounded-[2rem] border-dashed border-white/20 opacity-50">تتبع روابط الإحالة الذكية</div>
                                </div>
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
