import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية في ستريمليت ---
st.set_page_config(
    page_title="MR7 Global Marketplace", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة (Firebase) ---
fb_config_str = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
auth_token = st.secrets.get("__initial_auth_token", "")
current_theme = st.session_state.get('app_theme', "غامق إمبراطوري 🖤")

# --- 3. واجهة React المتكاملة (النسخة الاحترافية المُثلى) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        :root {
            --mr7-gold: #FFD700;
            --mr7-emerald: #00FF88;
            --mr7-dark: #030303;
            --mr7-card: rgba(15, 15, 15, 0.7);
        }
        body { 
            font-family: 'Tajawal', sans-serif; 
            background-color: var(--mr7-dark); 
            margin: 0; 
            overflow-x: hidden; 
            color: white; 
            scroll-behavior: smooth;
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--mr7-gold); }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        /* تأثيرات الزجاج الفاخرة */
        .glass-panel { 
            background: var(--mr7-card); 
            backdrop-filter: blur(24px); 
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }
        
        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: white;
            transition: all 0.3s ease;
        }
        .premium-input:focus {
            border-color: var(--mr7-gold);
            box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.1);
            outline: none;
            background: rgba(255, 255, 255, 0.05);
        }

        .product-card { 
            background: linear-gradient(145deg, rgba(20,20,20,0.9) 0%, rgba(10,10,10,0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        }
        .product-card:hover { 
            border-color: rgba(255, 215, 0, 0.3); 
            transform: translateY(-10px); 
            box-shadow: 0 20px 40px rgba(255, 215, 0, 0.08);
        }
        
        .btn-hover-gold { transition: all 0.3s ease; }
        .btn-hover-gold:hover {
            background-color: #FFEA00;
            color: black !important;
            box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
            transform: scale(1.02);
        }

        /* أنيميشن الدخول */
        .animate-fade-in { animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .animate-slide-in { animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        /* Toast Animation */
        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo, useCallback } = React;

        const Icon = ({ name, size = 24, className = "", fill = "none" }) => {
            const LucideIcon = lucide[name];
            return LucideIcon ? <i data-lucide={name} className={className} style={{ width: size, height: size, fill: fill }}></i> : null;
        };

        const App = () => {
            const [currentView, setCurrentView] = useState('market'); 
            const [selectedProduct, setSelectedProduct] = useState(null);
            const [searchTerm, setSearchTerm] = useState('');
            const [selectedCountry, setSelectedCountry] = useState('الكل');
            const [selectedCategory, setSelectedCategory] = useState('الكل');
            const [cart, setCart] = useState([]);
            const [wishlist, setWishlist] = useState([]);
            const [isCartOpen, setIsCartOpen] = useState(false);
            const [isGifting, setIsGifting] = useState(false);
            const [balance, setBalance] = useState(LEADER_BALANCE_PLACEHOLDER);
            const [toasts, setToasts] = useState([]);
            
            const [deliveryData, setDeliveryData] = useState({ address: '', date: '', notes: '' });

            const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "استشارات تريليونية", "أصول فاخرة"];
            const COUNTRIES = ["الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "قطر", "المغرب", "تركيا", "عالمي"];

            const products = [
                { 
                    id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت العقارية', 
                    img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800', rating: 5.0, sales: 12,
                    desc: 'تحفة معمارية في العاصمة الإدارية الجديدة، مصممة بأعلى معايير الاستدامة والذكاء الاصطناعي لإدارة المكاتب التنفيذية الخاصة بقادة الإمبراطورية.'
                },
                { 
                    id: 'p2', name: 'منظومة الطاقة X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', 
                    img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=800', rating: 4.8, sales: 85,
                    desc: 'محطة طاقة شمسية هجينة متنقلة قادرة على تغذية مجمعات سكنية كاملة، مع نظام تخزين طاقة متطور وتقنيات تبريد مدمجة مصممة للمناخ القاسي.'
                },
                { 
                    id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'MR7 Academy', 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800', rating: 4.9, sales: 1240,
                    desc: 'المنهج الدراسي الأكثر تأثيراً لبناء العقلية الاستثمارية السيادية وتحويل الأفكار إلى تدفقات نقدية عابرة للحدود عبر قوة التضاعف العشري.'
                },
                { 
                    id: 'p4', name: 'وكيل الذكاء الاصطناعي', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'مختبرات السيادة', 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', rating: 5.0, sales: 320,
                    desc: 'عميل مستقل مبرمج لخدمتك حصرياً، يقوم بإدارة محفظتك المالية وتحليل الأسواق العالمية لتنبيهك بفرص الضخ المالي الأكثر ربحية لحظياً.'
                },
                { 
                    id: 'p5', name: 'يخت الامتياز الملكي', price: 850000, country: 'الإمارات', category: 'أصول فاخرة', vendor: 'رويال مارين', 
                    img: 'https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=800', rating: 4.9, sales: 3,
                    desc: 'يخت ملكي بطول 90 قدماً، مجهز بأحدث تقنيات الملاحة، مهبط مروحيات مصغر، وقاعة اجتماعات بانورامية لعقد صفقات القادة الكبرى.'
                },
                { 
                    id: 'p6', name: 'مزرعة الذهب الأخضر', price: 450000, country: 'السودان', category: 'عقارات سيادية', vendor: 'سودان فيجن', 
                    img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800', rating: 4.7, sales: 15,
                    desc: 'مشروع زراعي ذكي يمتد على 500 فدان، يعتمد على تقنيات الري المؤتمتة لإنتاج المحاصيل العضوية النادرة للسوق العالمي.'
                }
            ];

            // إعادة تحديث الأيقونات عند تغير الحالة
            useEffect(() => { lucide.createIcons(); }, [searchTerm, selectedCountry, selectedCategory, isCartOpen, currentView, selectedProduct, cart, wishlist, toasts]);

            // --- نظام الإشعارات الذكي (Toasts) ---
            const showToast = useCallback((msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => {
                    setToasts(prev => prev.filter(t => t.id !== id));
                }, 3000);
            }, []);

            // --- العمليات ---
            const addToCart = (product) => {
                setCart(prev => {
                    if (prev.find(item => item.id === product.id)) {
                        showToast('الأصل موجود بالفعل في السلة', 'warning');
                        return prev;
                    }
                    showToast(`تم إضافة ${product.name} للسلة بنجاح`);
                    return [...prev, product];
                });
            };

            const toggleWishlist = (product) => {
                setWishlist(prev => {
                    const exists = prev.find(i => i.id === product.id);
                    if (exists) {
                        showToast(`تم إزالة ${product.name} من الأمنيات`, 'warning');
                        return prev.filter(i => i.id !== product.id);
                    }
                    showToast(`تم إضافة ${product.name} لحائط الأمنيات`);
                    return [...prev, product];
                });
            };

            const cartTotal = cart.reduce((s, i) => s + i.price, 0);

            const filtered = useMemo(() => products.filter(p => {
                const matchSearch = p.name.includes(searchTerm) || p.vendor.includes(searchTerm);
                const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
                const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
                return matchSearch && matchCountry && matchCategory;
            }), [products, searchTerm, selectedCountry, selectedCategory]);

            // --- المكونات الفرعية ---
            
            const ToastContainer = () => (
                <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                    {toasts.map(t => (
                        <div key={t.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${t.type === 'success' ? 'bg-black/80 border-[#00FF88]/30 text-[#00FF88]' : 'bg-black/80 border-yellow-500/30 text-yellow-500'}`}>
                            <Icon name={t.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                            <span className="font-bold text-sm text-white">{t.msg}</span>
                        </div>
                    ))}
                </div>
            );

            // 1. النافذة السينمائية للمنتج (Cinematic Modal)
            const ProductModal = () => {
                if (!selectedProduct) return null;
                return (
                    <div className="fixed inset-0 z-[300] flex items-center justify-center p-4 sm:p-8 bg-black/90 backdrop-blur-xl animate-fade-in">
                        <div className="glass-panel w-full max-w-5xl rounded-[2.5rem] overflow-hidden relative flex flex-col md:flex-row h-full max-h-[85vh]">
                            <button onClick={() => setSelectedProduct(null)} className="absolute top-6 left-6 p-3 bg-black/50 text-white rounded-full hover:bg-yellow-500 hover:text-black z-10 transition-all border border-white/10">
                                <Icon name="X" size={24} />
                            </button>
                            
                            <div className="w-full md:w-1/2 h-64 md:h-full relative">
                                <img src={selectedProduct.img} className="w-full h-full object-cover" />
                                <div className="absolute inset-0 bg-gradient-to-r from-black/80 to-transparent md:hidden"></div>
                            </div>
                            
                            <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-between overflow-y-auto no-scrollbar">
                                <div>
                                    <div className="flex flex-wrap gap-3 mb-6">
                                        <span className="bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest">{selectedProduct.category}</span>
                                        <span className="bg-white/5 text-gray-300 border border-white/10 px-4 py-1.5 rounded-full text-xs font-black flex items-center gap-1"><Icon name="MapPin" size={14}/> {selectedProduct.country}</span>
                                    </div>
                                    <h2 className="text-4xl font-black mb-4 text-white">{selectedProduct.name}</h2>
                                    <div className="flex items-center gap-4 mb-8 text-sm font-bold text-gray-400">
                                        <span className="flex items-center gap-1 text-yellow-500"><Icon name="Star" size={16} fill="currentColor" /> {selectedProduct.rating}</span>
                                        <span>•</span>
                                        <span className="flex items-center gap-1"><Icon name="Store" size={16} /> {selectedProduct.vendor}</span>
                                    </div>
                                    <p className="text-gray-300 leading-relaxed text-lg mb-8 font-medium">{selectedProduct.desc}</p>
                                </div>
                                
                                <div className="border-t border-white/10 pt-8">
                                    <div className="flex flex-col mb-8">
                                        <span className="text-xs text-gray-500 uppercase font-black tracking-widest mb-2">القيمة الاستثمارية (USD)</span>
                                        <span className="text-5xl font-black text-[#00FF88]">${selectedProduct.price.toLocaleString()}</span>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <button 
                                            onClick={() => { toggleWishlist(selectedProduct); setSelectedProduct(null); }}
                                            className={`py-4 rounded-2xl font-black text-lg transition-all border ${wishlist.find(i=>i.id===selectedProduct.id) ? 'bg-red-500/10 text-red-500 border-red-500/30' : 'bg-white/5 text-white border-white/10 hover:bg-white/10'} flex items-center justify-center gap-2`}
                                        >
                                            <Icon name="Heart" fill={wishlist.find(i=>i.id===selectedProduct.id) ? "currentColor" : "none"} /> أمنية
                                        </button>
                                        <button 
                                            onClick={() => { addToCart(selectedProduct); setSelectedProduct(null); setIsCartOpen(true); }}
                                            className="bg-yellow-500 text-black py-4 rounded-2xl font-black text-lg btn-hover-gold flex items-center justify-center gap-2"
                                        >
                                            <Icon name="ShoppingBag" /> إضافة للسلة
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            // 2. الهيدر الاحترافي الموحد
            const Navbar = () => (
                <nav className="glass-panel flex flex-col md:flex-row justify-between items-center mb-10 gap-6 p-4 md:p-6 rounded-[2rem] sticky top-4 z-[100] mx-4 md:mx-auto max-w-[1600px]">
                    <div className="flex items-center gap-5 cursor-pointer group" onClick={() => setCurrentView('market')}>
                        <div className="bg-gradient-to-br from-yellow-400 to-yellow-600 p-3.5 rounded-2xl shadow-[0_0_20px_rgba(255,215,0,0.3)] text-black group-hover:scale-105 transition-transform">
                            <Icon name="Globe" size={28} />
                        </div>
                        <div>
                            <h1 className="text-2xl md:text-3xl font-black text-white tracking-tighter uppercase mb-0.5">MR7 <span className="text-yellow-500">MARKET</span></h1>
                            <p className="text-[9px] md:text-[10px] text-gray-400 font-bold uppercase tracking-[0.3em]">Sovereign Commerce</p>
                        </div>
                    </div>

                    <div className="flex-1 max-w-2xl w-full relative">
                        <Icon name="Search" size={20} className="absolute right-5 top-1/2 -translate-y-1/2 text-gray-400" />
                        <input 
                            type="text" 
                            placeholder="البحث الشامل عن الأصول الإمبراطورية..."
                            className="w-full premium-input rounded-2xl py-4 pr-14 pl-6 text-sm font-bold"
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="flex items-center gap-4 sm:gap-6">
                        <div className="hidden lg:flex flex-col items-end mr-4 pr-6 border-r border-white/10">
                            <span className="text-[10px] text-gray-500 font-black uppercase tracking-widest">خزنة السيولة</span>
                            <div className="flex items-center gap-2 text-[#00FF88] font-black text-2xl">
                                <Icon name="Wallet" size={20} />
                                <span>${balance.toLocaleString()}</span>
                            </div>
                        </div>
                        <button onClick={() => setCurrentView('wishlist')} className="p-3.5 bg-white/5 rounded-2xl hover:bg-white/10 transition-all relative border border-white/5 group" title="حائط الأمنيات">
                            <Icon name="Heart" size={24} className={`group-hover:text-red-500 transition-colors ${wishlist.length > 0 ? "text-red-500" : "text-gray-300"}`} fill={wishlist.length > 0 ? "currentColor" : "none"} />
                            {wishlist.length > 0 && <span className="absolute -top-2 -left-2 bg-red-500 text-white text-[11px] font-black w-6 h-6 flex items-center justify-center rounded-full shadow-[0_0_10px_rgba(239,68,68,0.5)]">{wishlist.length}</span>}
                        </button>
                        <button onClick={() => setIsCartOpen(true)} className="p-3.5 bg-white/5 rounded-2xl hover:bg-white/10 transition-all relative border border-white/5 group" title="السلة">
                            <Icon name="ShoppingBag" size={24} className="group-hover:text-yellow-500 transition-colors text-gray-300" />
                            {cart.length > 0 && <span className="absolute -top-2 -left-2 bg-yellow-500 text-black text-[11px] font-black w-6 h-6 flex items-center justify-center rounded-full shadow-[0_0_10px_rgba(255,215,0,0.5)]">{cart.length}</span>}
                        </button>
                    </div>
                </nav>
            );

            // 3. واجهة السوق (Market View)
            const MarketView = () => (
                <div className="animate-fade-in px-4 md:px-8 pb-10">
                    <div className="flex gap-3 overflow-x-auto no-scrollbar mb-8 pb-2">
                        {CATEGORIES.map(cat => (
                            <button 
                                key={cat} 
                                onClick={() => setSelectedCategory(cat)}
                                className={`px-6 md:px-8 py-3 rounded-2xl text-xs md:text-sm font-black whitespace-nowrap transition-all border ${selectedCategory === cat ? 'bg-yellow-500 text-black border-yellow-500 shadow-[0_0_20px_rgba(255,215,0,0.2)]' : 'bg-transparent text-gray-400 border-white/10 hover:border-white/30 hover:text-white'}`}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>

                    <div className="mb-10 flex flex-wrap items-center gap-3">
                        <div className="flex items-center gap-2 text-gray-500 font-black text-sm px-2 uppercase tracking-widest">
                            <Icon name="Filter" size={16} /> تصفية جغرافية:
                        </div>
                        <div className="flex gap-2 overflow-x-auto no-scrollbar">
                            {COUNTRIES.map(c => (
                                <button 
                                    key={c} 
                                    onClick={() => setSelectedCountry(c)}
                                    className={`px-4 py-2 rounded-xl text-xs font-black transition-all border ${selectedCountry === c ? 'bg-white text-black border-white' : 'bg-white/5 text-gray-400 border-white/5 hover:bg-white/10'}`}
                                >
                                    {c}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {filtered.map(p => (
                            <div key={p.id} className="group product-card rounded-[2rem] overflow-hidden flex flex-col relative">
                                <div className="relative h-56 overflow-hidden cursor-pointer" onClick={() => setSelectedProduct(p)}>
                                    <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                                    <img src={p.img} className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110" />
                                    <div className="absolute top-4 right-4 z-20 bg-black/60 backdrop-blur-md px-3 py-1 rounded-xl flex items-center gap-1.5 border border-white/10 text-[10px] font-black uppercase text-white">
                                        <Icon name="MapPin" size={12} className="text-yellow-500" /> {p.country}
                                    </div>
                                    <div className="absolute bottom-4 left-4 z-20 bg-yellow-500 text-black px-3 py-1 rounded-lg text-[10px] font-black shadow-lg">
                                        {p.category}
                                    </div>
                                </div>
                                <div className="p-6 flex-1 flex flex-col">
                                    <div className="flex justify-between items-center mb-4">
                                        <div className="flex items-center gap-1.5 text-yellow-500 font-black text-xs">
                                            <Icon name="Star" size={14} fill="currentColor" /> {p.rating}
                                        </div>
                                        <span className="text-[10px] text-gray-500 font-black uppercase tracking-widest flex items-center gap-1"><Icon name="TrendingUp" size={12} className="text-[#00FF88]" /> {p.sales}</span>
                                    </div>
                                    <h3 className="text-xl font-black mb-2 line-clamp-1 group-hover:text-yellow-500 transition-colors cursor-pointer" onClick={() => setSelectedProduct(p)}>{p.name}</h3>
                                    <p className="text-gray-500 text-[11px] font-bold mb-6 italic flex items-center gap-1"><Icon name="Store" size={12}/> {p.vendor}</p>
                                    
                                    <div className="mt-auto flex items-center justify-between border-t border-white/5 pt-5">
                                        <div className="flex flex-col">
                                            <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                        </div>
                                        <div className="flex gap-2">
                                            <button onClick={() => toggleWishlist(p)} className={`p-2.5 rounded-xl transition-colors border ${wishlist.find(i=>i.id===p.id) ? 'bg-red-500/20 border-red-500/30 text-red-500' : 'bg-white/5 border-white/5 text-gray-400 hover:bg-white/10 hover:text-white'}`} title="أمنية">
                                                <Icon name="Heart" size={18} fill={wishlist.find(i=>i.id===p.id) ? "currentColor" : "none"} />
                                            </button>
                                            <button onClick={() => { setIsGifting(true); addToCart(p); setCurrentView('checkout'); }} className="p-2.5 rounded-xl bg-white/5 border border-white/5 text-gray-400 hover:bg-white/10 hover:text-yellow-500 transition-colors" title="إرسال كهدية">
                                                <Icon name="Gift" size={18} />
                                            </button>
                                            <button onClick={() => addToCart(p)} className="p-2.5 rounded-xl bg-yellow-500 text-black btn-hover-gold" title="إضافة للسلة">
                                                <Icon name="ShoppingBag" size={18} />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );

            // 4. حائط الأمنيات (Wishlist View)
            const WishlistView = () => (
                <div className="animate-fade-in px-4 md:px-8 pb-20">
                    <div className="flex items-center gap-6 mb-10 border-b border-white/10 pb-6">
                        <button onClick={() => setCurrentView('market')} className="p-3 bg-white/5 rounded-xl hover:bg-yellow-500 hover:text-black transition-all border border-white/5"><Icon name="ArrowRight" size={24} /></button>
                        <h2 className="text-3xl md:text-4xl font-black tracking-tighter">حائط الأمنيات 🏛️</h2>
                    </div>
                    {wishlist.length === 0 ? (
                        <div className="text-center py-24 bg-white/5 rounded-[2rem] border border-dashed border-white/10">
                            <Icon name="Heart" size={60} className="mx-auto mb-4 text-gray-600" />
                            <p className="text-xl font-black text-gray-400">لا توجد أمنيات مسجلة. عد للسوق لبناء رؤيتك.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {wishlist.map(p => (
                                <div key={p.id} className="bg-[#0A0A0A] border border-white/5 p-5 rounded-[2rem] group relative hover:border-yellow-500/30 transition-colors">
                                    <div className="relative h-48 rounded-2xl overflow-hidden mb-5">
                                        <img src={p.img} className="w-full h-full object-cover group-hover:scale-105 transition-all duration-700" />
                                        <button onClick={() => toggleWishlist(p)} className="absolute top-3 left-3 bg-black/60 backdrop-blur-md p-2.5 rounded-full text-red-500 hover:bg-red-500 hover:text-white transition-colors">
                                            <Icon name="Trash2" size={16} />
                                        </button>
                                    </div>
                                    <h4 className="text-xl font-black mb-3 line-clamp-1">{p.name}</h4>
                                    <div className="flex justify-between items-center mt-auto">
                                        <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                        <button onClick={() => addToCart(p)} className="bg-white/10 hover:bg-yellow-500 hover:text-black text-white px-4 py-2.5 rounded-xl font-black text-sm transition-all flex items-center gap-2">
                                            <Icon name="ShoppingBag" size={16} /> نقل للسلة
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            );

            // 5. صفحة الدفع التنفيذية (Executive Checkout)
            const CheckoutView = () => (
                <div className="animate-fade-in px-4 md:px-8 pb-20 max-w-[1400px] mx-auto">
                    <div className="flex items-center gap-6 mb-10 border-b border-white/10 pb-6">
                        <button onClick={() => setCurrentView('market')} className="p-3 bg-white/5 rounded-xl hover:bg-yellow-500 hover:text-black transition-all border border-white/5"><Icon name="ArrowRight" size={24} /></button>
                        <h2 className="text-3xl md:text-4xl font-black tracking-tighter">إتمام العملية 🛡️</h2>
                    </div>
                    
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                        <div className="lg:col-span-2 space-y-8">
                            {/* نوع الاستحواذ */}
                            <div className="glass-panel p-8 rounded-[2rem]">
                                <h3 className="text-xl font-black flex items-center gap-3 text-yellow-500 mb-6"><span className="bg-yellow-500 text-black w-6 h-6 flex items-center justify-center rounded-full text-xs">1</span> طبيعة الضخ المالي</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                    <div onClick={() => setIsGifting(false)} className={`p-5 rounded-[1.5rem] border-2 cursor-pointer transition-all ${!isGifting ? 'border-yellow-500 bg-yellow-500/10' : 'border-white/5 bg-white/5 hover:border-white/20'}`}>
                                        <div className="flex justify-between items-start mb-3">
                                            <div className={`p-2.5 rounded-lg ${!isGifting ? 'bg-yellow-500 text-black' : 'bg-white/10 text-gray-400'}`}><Icon name="ShieldCheck" size={20}/></div>
                                            {!isGifting && <div className="w-5 h-5 rounded-full bg-yellow-500 flex items-center justify-center text-black"><Icon name="Check" size={12}/></div>}
                                        </div>
                                        <h4 className="text-lg font-black mb-1">محفظتي الشخصية</h4>
                                        <p className="text-xs text-gray-400 font-medium">توثيق الأصول باسمك.</p>
                                    </div>
                                    
                                    <div onClick={() => setIsGifting(true)} className={`p-5 rounded-[1.5rem] border-2 cursor-pointer transition-all ${isGifting ? 'border-yellow-500 bg-yellow-500/10' : 'border-white/5 bg-white/5 hover:border-white/20'}`}>
                                        <div className="flex justify-between items-start mb-3">
                                            <div className={`p-2.5 rounded-lg ${isGifting ? 'bg-yellow-500 text-black' : 'bg-white/10 text-gray-400'}`}><Icon name="Gift" size={20}/></div>
                                            {isGifting && <div className="w-5 h-5 rounded-full bg-yellow-500 flex items-center justify-center text-black"><Icon name="Check" size={12}/></div>}
                                        </div>
                                        <h4 className="text-lg font-black mb-1">إرسال كهدية</h4>
                                        <p className="text-xs text-gray-400 font-medium">نقل الملكية لقائد آخر.</p>
                                    </div>
                                </div>
                                {isGifting && (
                                    <div className="animate-fade-in mt-5">
                                        <input type="text" placeholder="المعرف الرقمي للمستلم (UUID)..." className="w-full premium-input rounded-xl py-4 px-5 font-bold text-sm" />
                                    </div>
                                )}
                            </div>

                            {/* البيانات اللوجستية */}
                            <div className="glass-panel p-8 rounded-[2rem]">
                                <h3 className="text-xl font-black flex items-center gap-3 text-yellow-500 mb-6"><span className="bg-yellow-500 text-black w-6 h-6 flex items-center justify-center rounded-full text-xs">2</span> بيانات التوثيق</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest">العنوان الدقيق</label>
                                        <input type="text" placeholder="المدينة، المنطقة..." className="w-full premium-input rounded-xl py-3.5 px-4 text-sm font-bold" onChange={(e) => setDeliveryData({...deliveryData, address: e.target.value})} />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest">تاريخ التنفيذ</label>
                                        <input type="date" className="w-full premium-input rounded-xl py-3.5 px-4 text-sm font-bold text-white" style={{colorScheme: 'dark'}} onChange={(e) => setDeliveryData({...deliveryData, date: e.target.value})} />
                                    </div>
                                    <div className="md:col-span-2 space-y-2">
                                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest">ملاحظات العقد</label>
                                        <textarea placeholder="أي تفاصيل لفريق العمليات..." className="w-full premium-input rounded-xl py-3.5 px-4 text-sm font-bold min-h-[100px]" onChange={(e) => setDeliveryData({...deliveryData, notes: e.target.value})}></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* ملخص الاستحقاق */}
                        <div>
                            <div className="glass-panel p-8 rounded-[2rem] sticky top-32">
                                <h3 className="text-xl font-black mb-6 border-b border-white/10 pb-4">ملخص الأصول</h3>
                                <div className="space-y-4 mb-8 max-h-[40vh] overflow-y-auto no-scrollbar">
                                    {cart.length === 0 ? <p className="text-gray-500 text-center py-4 text-sm">لا توجد أصول مختارة.</p> : 
                                      cart.map(item => (
                                        <div key={item.id} className="flex gap-4 bg-white/5 p-3 rounded-xl border border-white/5">
                                            <img src={item.img} className="w-14 h-14 rounded-lg object-cover" />
                                            <div className="flex-1 flex flex-col justify-center">
                                                <h4 className="font-black text-sm line-clamp-1">{item.name}</h4>
                                                <span className="text-sm font-black text-[#00FF88]">${item.price.toLocaleString()}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <div className="border-t border-white/10 pt-6 mb-6 space-y-3 text-sm">
                                    <div className="flex justify-between font-bold text-gray-400"><span>إجمالي الأصول</span><span>${cartTotal.toLocaleString()}</span></div>
                                    <div className="flex justify-between font-bold text-gray-400"><span>رسوم التوثيق</span><span className="text-[#00FF88]">معفاة</span></div>
                                    <div className="flex justify-between text-2xl font-black text-white pt-3 border-t border-white/5">
                                        <span>المستحق</span><span className="text-yellow-500">${cartTotal.toLocaleString()}</span>
                                    </div>
                                </div>
                                <button 
                                    onClick={() => {
                                        if(balance >= cartTotal) {
                                            setBalance(b => b - cartTotal);
                                            setCart([]);
                                            setCurrentView('market');
                                            showToast('تم تأكيد عملية الاستحواذ بنجاح!');
                                        } else {
                                            showToast('رصيد الخزنة غير كافٍ للعملية', 'warning');
                                        }
                                    }}
                                    disabled={cart.length === 0}
                                    className="w-full py-5 rounded-2xl font-black text-lg bg-yellow-500 text-black btn-hover-gold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                >
                                    <Icon name="Zap" size={20} /> تأكيد الدفع 
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            );

            // --- الفوتر الاحترافي (Premium Footer) ---
            const Footer = () => (
                <footer className="mt-10 border-t border-white/10 bg-[#050505] py-16 relative overflow-hidden">
                    {/* تأثيرات إضاءة خلفية للفوتر */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[80%] h-[1px] bg-gradient-to-r from-transparent via-yellow-500/50 to-transparent"></div>
                    
                    <div className="max-w-[1600px] mx-auto px-6 md:px-12 flex flex-col md:flex-row justify-between items-center gap-10">
                        
                        {/* الشعار والهوية */}
                        <div className="flex items-center gap-5">
                            <div className="bg-yellow-500 p-3 rounded-2xl text-black shadow-[0_0_15px_rgba(255,215,0,0.2)]">
                                <Icon name="ShieldCheck" size={28} />
                            </div>
                            <div className="text-right md:text-right">
                                <h3 className="font-black text-2xl tracking-widest uppercase text-white mb-1">MR7 Empire</h3>
                                <p className="text-[10px] text-gray-500 uppercase tracking-[0.4em] font-bold">Global Sovereign Commerce</p>
                            </div>
                        </div>

                        {/* أزرار العمليات السريعة (الهدايا والأمنيات) */}
                        <div className="flex flex-wrap justify-center gap-4">
                            <button 
                                onClick={() => { setIsGifting(true); setCurrentView('checkout'); window.scrollTo(0,0); }} 
                                className="flex items-center gap-3 bg-white/5 hover:bg-yellow-500/10 border border-white/10 hover:border-yellow-500/50 text-gray-300 hover:text-yellow-500 transition-all px-6 py-3.5 rounded-2xl font-bold text-sm group"
                            >
                                <Icon name="Gift" size={18} className="group-hover:scale-110 transition-transform" /> مركز الهدايا السيادية
                            </button>
                            <button 
                                onClick={() => { setCurrentView('wishlist'); window.scrollTo(0,0); }} 
                                className="flex items-center gap-3 bg-white/5 hover:bg-red-500/10 border border-white/10 hover:border-red-500/50 text-gray-300 hover:text-red-500 transition-all px-6 py-3.5 rounded-2xl font-bold text-sm group"
                            >
                                <Icon name="Heart" size={18} className="group-hover:scale-110 transition-transform" /> حائط الأمنيات
                            </button>
                        </div>

                    </div>
                </footer>
            );

            return (
                <div className="min-h-screen flex flex-col relative bg-[#020202]">
                    <Navbar />

                    <main className="flex-1 w-full max-w-[1600px] mx-auto pt-2 pb-10">
                        {currentView === 'market' && <MarketView />}
                        {currentView === 'wishlist' && <WishlistView />}
                        {currentView === 'checkout' && <CheckoutView />}
                    </main>

                    <Footer />
                    
                    <ProductModal />
                    <ToastContainer />

                    {/* --- السلة الجانبية (Slide-over Cart) --- */}
                    {isCartOpen && (
                        <div className="fixed inset-0 z-[400] flex justify-end">
                            <div className="absolute inset-0 bg-black/70 backdrop-blur-sm transition-opacity" onClick={() => setIsCartOpen(false)} />
                            <div className="relative w-full max-w-[420px] bg-[#0A0A0A] border-r border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.8)] h-full flex flex-col animate-slide-in">
                                <div className="flex items-center justify-between p-8 border-b border-white/5">
                                    <div className="flex items-center gap-4">
                                        <div className="bg-yellow-500/10 text-yellow-500 p-2.5 rounded-xl border border-yellow-500/20"><Icon name="ShoppingBag" size={22} /></div>
                                        <h2 className="text-xl font-black uppercase tracking-widest text-white">سلة الضخ</h2>
                                    </div>
                                    <button onClick={() => setIsCartOpen(false)} className="p-2.5 bg-white/5 rounded-xl hover:bg-white/10 transition-colors text-gray-400 hover:text-white"><Icon name="X" size={20} /></button>
                                </div>
                                
                                <div className="flex-1 overflow-y-auto p-6 space-y-4 no-scrollbar">
                                    {cart.length === 0 ? (
                                        <div className="h-full flex flex-col justify-center items-center opacity-40 text-center">
                                            <Icon name="ShoppingCart" size={60} className="mb-4 text-gray-500" />
                                            <p className="text-lg font-black uppercase tracking-widest text-gray-400">لا توجد أصول</p>
                                        </div>
                                    ) : (
                                      cart.map(item => (
                                        <div key={item.id} className="bg-[#111] p-4 rounded-2xl border border-white/5 flex gap-4 relative group hover:border-yellow-500/30 transition-colors animate-fade-in">
                                            <img src={item.img} className="w-20 h-20 rounded-xl object-cover border border-white/5" />
                                            <div className="flex-1 flex flex-col justify-center pr-2">
                                                <h4 className="font-black text-sm line-clamp-1 mb-1 text-white">{item.name}</h4>
                                                <span className="text-[#00FF88] font-black text-lg">${item.price.toLocaleString()}</span>
                                            </div>
                                            <button onClick={() => {
                                                removeFromCart(item.id);
                                                showToast(`تم إزالة ${item.name}`, 'warning');
                                            }} className="absolute top-2 left-2 p-1.5 bg-black/60 backdrop-blur-md rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-500/20 opacity-0 group-hover:opacity-100 transition-all">
                                                <Icon name="Trash2" size={14} />
                                            </button>
                                        </div>
                                      ))
                                    )}
                                </div>
                                
                                {cart.length > 0 && (
                                    <div className="p-8 bg-[#0A0A0A] border-t border-white/5 shadow-[0_-10px_30px_rgba(0,0,0,0.5)] z-10">
                                        <div className="flex justify-between items-center mb-6">
                                            <span className="text-gray-400 font-bold uppercase tracking-widest text-xs">المستحق</span>
                                            <span className="text-3xl font-black text-yellow-500">${cartTotal.toLocaleString()}</span>
                                        </div>
                                        <button onClick={() => { setIsCartOpen(false); setCurrentView('checkout'); window.scrollTo(0,0); }} className="w-full py-4 rounded-xl font-black text-lg bg-yellow-500 text-black btn-hover-gold flex justify-center items-center gap-2">
                                            تأكيد الاستحواذ <Icon name="ArrowLeft" size={20} />
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات (آمن بدون Syntax Error) ---
current_balance = st.session_state.get('cash_balance', 1250000)
# الاستبدال المباشر في النص لحماية كود React
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. تشغيل واجهة React ---
components.html(final_html, height=1400, scrolling=True)

# --- 6. أزرار التحكم الخاصة ببايثون (Streamlit Core) ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي (Python Core)"):
    st.switch_page("app.py")
