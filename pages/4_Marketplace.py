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

# --- 3. بناء واجهة React المتكاملة 2.2 (إصلاح السلة وحائط الأمنيات) ---
react_html = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        body { 
            font-family: 'Tajawal', sans-serif; 
            background-color: #020202; 
            margin: 0; 
            overflow-x: hidden; 
            color: white; 
        }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .glass { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
        }
        .product-card {
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .product-card:hover { 
            border-color: rgba(234, 179, 8, 0.4); 
            transform: translateY(-8px); 
        }
        .btn-action {
            transition: 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            padding: 12px;
            cursor: pointer;
        }
        .btn-action:active { transform: scale(0.9); }
        
        .wish-active { color: #ff4b4b !important; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-view { animation: fadeIn 0.5s ease-out; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

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
            const [balance, setBalance] = useState(LEADER_BALANCE_PLACEHOLDER);
            const [cart, setCart] = useState([]);
            const [wishlist, setWishlist] = useState([]);
            const [isCartOpen, setIsCartOpen] = useState(false);
            const [isGifting, setIsGifting] = useState(false);
            
            const [deliveryData, setDeliveryData] = useState({
                address: '',
                date: '',
                notes: ''
            });

            const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "استشارات تريليونية", "أصول فاخرة"];
            const COUNTRIES = ["الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "قطر", "المغرب", "تركيا", "عالمي"];

            const products = [
                { 
                    id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت العقارية', 
                    img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600', rating: 5.0, sales: 12,
                    desc: 'ناطحة سحاب ذكية في قلب العاصمة الإدارية، مزودة بأنظمة تحكم طاقي مستقل ومساحات عمل فاخرة للقادة.'
                },
                { 
                    id: 'p2', name: 'منظومة الطاقة X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', 
                    img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=600', rating: 4.8, sales: 85,
                    desc: 'وحدة طاقة شمسية هجينة بقدرة 20 كيلو واط، مصممة للمناخ الصحراوي القاسي مع ضمان شامل.'
                },
                { 
                    id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'MR7 Academy', 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600', rating: 4.9, sales: 1240,
                    desc: 'المنهج المتكامل لبناء جيوش المسوقين العابرة للحدود وإدارة السيولة الرقمية.'
                },
                { 
                    id: 'p4', name: 'وكيل الذكاء الاصطناعي السيادي', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'مختبرات السيادة', 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600', rating: 5.0, sales: 320,
                    desc: 'خوارزمية مخصصة لتحليل تقلبات السوق العالمية وتقديم توصيات استثمارية لحظية.'
                },
                { 
                    id: 'p5', name: 'يخت الامتياز الملكي', price: 850000, country: 'الإمارات', category: 'أصول فاخرة', vendor: 'مارين نبت', 
                    img: 'https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=600', rating: 4.9, sales: 3,
                    desc: 'يخت بطول 80 قدماً، مجهز بقاعة اجتماعات وقمرة قيادة ذكية.'
                },
                { 
                    id: 'p6', name: 'مزرعة الذهب الأخضر', price: 450000, country: 'السودان', category: 'عقارات سيادية', vendor: 'سودان فيجن', 
                    img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600', rating: 4.7, sales: 15,
                    desc: 'مشروع زراعي متكامل يعتمد على تقنيات الري الحديثة لإنتاج المحاصيل النادرة.'
                }
            ];

            useEffect(() => {
                lucide.createIcons();
            }, [searchTerm, selectedCountry, selectedCategory, isCartOpen, currentView, selectedProduct, cart, wishlist]);

            const filtered = products.filter(p => {
                const matchSearch = p.name.includes(searchTerm) || p.vendor.includes(searchTerm);
                const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
                const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
                return matchSearch && matchCountry && matchCategory;
            });

            // --- العمليات (Logic) ---
            const addToCart = (product) => {
                if (!cart.find(i => i.id === product.id)) {
                    setCart([...cart, product]);
                }
                setIsCartOpen(true);
            };

            const toggleWishlist = (product) => {
                if (wishlist.find(i => i.id === product.id)) {
                    setWishlist(wishlist.filter(i => i.id !== product.id));
                } else {
                    setWishlist([...wishlist, product]);
                }
            };

            const directToGift = (product) => {
                if (!cart.find(i => i.id === product.id)) {
                    setCart([...cart, product]);
                }
                setIsGifting(true);
                setCurrentView('checkout');
            };

            const removeFromCart = (id) => {
                setCart(cart.filter(item => item.id !== id));
            };

            const cartTotal = cart.reduce((s, i) => s + i.price, 0);

            // --- مكونات واجهة المستخدم ---
            
            const Header = () => (
                <nav className="flex flex-col md:flex-row justify-between items-center mb-10 gap-6 glass p-6 rounded-[2.5rem] sticky top-0 z-[100]">
                    <div className="flex items-center gap-4 cursor-pointer" onClick={() => setCurrentView('market')}>
                        <div className="bg-yellow-500 p-3 rounded-2xl shadow-xl text-black">
                            <Icon name="Store" size={28} />
                        </div>
                        <div>
                            <h1 className="text-2xl font-black text-yellow-500 tracking-tighter uppercase">MR7 GLOBAL</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest text-left">Marketplace</p>
                        </div>
                    </div>

                    <div className="flex-1 max-w-xl w-full relative text-black">
                        <input 
                            type="text" 
                            placeholder="ابحث عن أصول سيادية..."
                            className="w-full bg-white border-none rounded-2xl py-4 px-6 focus:ring-2 focus:ring-yellow-500 outline-none transition-all font-bold text-sm"
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="flex flex-col items-end">
                            <span className="text-[10px] text-gray-500 font-black uppercase">السيولة المتاحة</span>
                            <div className="flex items-center gap-2 text-[#00FF88] font-black text-xl">
                                <Icon name="Wallet" size={18} />
                                <span>${balance.toLocaleString()}</span>
                            </div>
                        </div>
                        <button onClick={() => setCurrentView('wishlist')} className="p-3 bg-white/5 rounded-2xl hover:bg-white/10 relative group transition-all">
                            <Icon name="Heart" size={24} className={wishlist.length > 0 ? "text-red-500" : "text-gray-400"} fill={wishlist.length > 0 ? "currentColor" : "none"} />
                            {wishlist.length > 0 && <span className="absolute -top-1 -left-1 bg-red-500 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full animate-bounce">{wishlist.length}</span>}
                        </button>
                        <button onClick={() => setIsCartOpen(true)} className="relative p-3 bg-white/5 rounded-2xl hover:bg-white/10 transition-all border border-white/5">
                            <Icon name="ShoppingBag" size={28} />
                            {cart.length > 0 && <span className="absolute -top-1 -left-1 bg-yellow-500 text-black text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-4 border-[#020202]">
                                {cart.length}
                            </span>}
                        </button>
                    </div>
                </nav>
            );

            // --- تفاصيل المنتج (Modal) ---
            const ProductModal = () => {
                if (!selectedProduct) return null;
                return (
                    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-black/95 backdrop-blur-xl animate-view">
                        <div className="glass w-full max-w-2xl rounded-[3.5rem] overflow-hidden relative border border-white/10">
                            <button onClick={() => setSelectedProduct(null)} className="absolute top-8 left-8 p-3 bg-white/5 rounded-full hover:bg-white/20 z-10 transition-all">
                                <Icon name="X" size={24} />
                            </button>
                            <img src={selectedProduct.img} className="w-full h-96 object-cover" />
                            <div className="p-10">
                                <div className="flex justify-between items-center mb-6">
                                    <span className="bg-yellow-500 text-black px-5 py-1.5 rounded-full text-xs font-black uppercase tracking-widest">{selectedProduct.category}</span>
                                    <span className="text-yellow-500 font-black tracking-widest">📍 {selectedProduct.country}</span>
                                </div>
                                <h2 className="text-4xl font-black mb-6">{selectedProduct.name}</h2>
                                <p className="text-gray-400 leading-relaxed mb-10 text-xl font-medium">{selectedProduct.desc}</p>
                                <div className="flex items-center justify-between border-t border-white/5 pt-8">
                                    <div className="flex flex-col">
                                        <span className="text-xs text-gray-500 uppercase font-bold mb-2">القيمة الاستثمارية</span>
                                        <span className="text-4xl font-black text-[#00FF88]">${selectedProduct.price.toLocaleString()}</span>
                                    </div>
                                    <div className="flex gap-4">
                                        <button 
                                            onClick={() => { toggleWishlist(selectedProduct); setSelectedProduct(null); }}
                                            className="bg-white/5 text-white px-6 py-5 rounded-2xl font-bold hover:bg-red-500/20 transition-all border border-white/10"
                                        >
                                            <Icon name="Heart" fill={wishlist.find(i=>i.id===selectedProduct.id) ? "currentColor" : "none"} className={wishlist.find(i=>i.id===selectedProduct.id) ? "text-red-500" : ""} />
                                        </button>
                                        <button 
                                            onClick={() => { addToCart(selectedProduct); setSelectedProduct(null); }}
                                            className="bg-yellow-500 text-black px-12 py-5 rounded-2xl font-black text-xl hover:scale-105 transition-all shadow-xl shadow-yellow-500/20"
                                        >
                                            ضخ الآن ⚡
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            // --- حائط الأمنيات (Wish Wall View) ---
            const WishlistView = () => (
                <div className="animate-view">
                    <div className="flex items-center gap-6 mb-12">
                        <button onClick={() => setCurrentView('market')} className="bg-white/5 p-4 rounded-2xl hover:bg-yellow-500 hover:text-black transition-all">
                            <Icon name="ArrowRight" size={28} />
                        </button>
                        <h2 className="text-4xl font-black tracking-tighter">حائط الأمنيات الاستراتيجي 🏛️</h2>
                    </div>
                    {wishlist.length === 0 ? (
                        <div className="text-center py-32 glass rounded-[3rem] opacity-30 border-dashed border-2">
                            <Icon name="Heart" size={100} className="mx-auto mb-6" />
                            <p className="text-2xl font-black">حائطك خالٍ حالياً.. ابنِ رؤيتك المستقبلية الآن</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                            {wishlist.map(p => (
                                <div key={p.id} className="glass p-8 rounded-[3rem] relative flex flex-col group border border-white/5">
                                    <div className="relative h-56 rounded-[2rem] overflow-hidden mb-6">
                                        <img src={p.img} className="w-full h-full object-cover group-hover:scale-110 transition-all duration-700" />
                                        <button 
                                            onClick={() => toggleWishlist(p)}
                                            className="absolute top-4 left-4 bg-black/60 p-3 rounded-full text-red-500"
                                        >
                                            <Icon name="X" size={18} />
                                        </button>
                                    </div>
                                    <h4 className="font-black text-2xl mb-2">{p.name}</h4>
                                    <p className="text-gray-500 text-sm mb-6 line-clamp-2">{p.desc}</p>
                                    <div className="mt-auto flex items-center justify-between border-t border-white/5 pt-6">
                                        <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                        <button onClick={() => addToCart(p)} className="bg-yellow-500 text-black px-6 py-3 rounded-xl font-black text-sm">نقل للسلة</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            );

            // --- صفحة الدفع (Checkout View) ---
            const CheckoutView = () => (
                <div className="animate-view max-w-6xl mx-auto py-12">
                    <div className="flex items-center justify-between mb-16">
                        <div className="flex items-center gap-6">
                            <button onClick={() => setCurrentView('market')} className="bg-white/5 p-4 rounded-2xl hover:bg-yellow-500 hover:text-black transition-all">
                                <Icon name="ArrowRight" size={28} />
                            </button>
                            <h2 className="text-4xl font-black tracking-tighter">إتمام العملية السيادية 🛡️</h2>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                        <div className="lg:col-span-2 space-y-8">
                            <div className="glass p-10 rounded-[3rem]">
                                <h3 className="text-2xl font-black mb-10 flex items-center gap-4 text-yellow-500">
                                    <Icon name="Package" /> الأصول المحددة للضخ
                                </h3>
                                <div className="space-y-6">
                                    {cart.map(item => (
                                        <div key={item.id} className="flex justify-between items-center bg-white/5 p-6 rounded-[2rem] border border-white/5 group">
                                            <div className="flex items-center gap-6">
                                                <img src={item.img} className="w-20 h-20 rounded-2xl object-cover" />
                                                <div>
                                                    <p className="font-black text-xl mb-1">{item.name}</p>
                                                    <div className="flex gap-4 items-center">
                                                        <span className="text-yellow-500 font-bold text-xs uppercase">📍 {item.country}</span>
                                                        <span className="text-gray-500 font-bold text-xs">🏛️ {item.vendor}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-8">
                                                <span className="text-2xl font-black text-[#00FF88]">${item.price.toLocaleString()}</span>
                                                <button onClick={() => removeFromCart(item.id)} className="text-gray-600 hover:text-red-500 transition-colors">
                                                    <Icon name="Trash2" size={22} />
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="glass p-10 rounded-[3rem]">
                                <h3 className="text-2xl font-black mb-10 flex items-center gap-4 text-yellow-500">
                                    <Icon name="Truck" /> بيانات الاستلام اللوجستية
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="space-y-3">
                                        <label className="text-xs font-bold text-gray-500 mr-2 uppercase tracking-widest">عنوان الاستلام الدقيق</label>
                                        <input 
                                            type="text" 
                                            placeholder="الإقليم، المدينة، الشارع..."
                                            className="w-full bg-white border-none rounded-2xl py-5 px-8 text-black font-bold text-sm outline-none focus:ring-4 focus:ring-yellow-500/20 transition-all"
                                            onChange={(e) => setDeliveryData({...deliveryData, address: e.target.value})}
                                        />
                                    </div>
                                    <div className="space-y-3">
                                        <label className="text-xs font-bold text-gray-500 mr-2 uppercase tracking-widest">موعد التنفيذ المفضل</label>
                                        <input 
                                            type="date" 
                                            className="w-full bg-white border-none rounded-2xl py-5 px-8 text-black font-bold text-sm outline-none focus:ring-4 focus:ring-yellow-500/20 transition-all"
                                            onChange={(e) => setDeliveryData({...deliveryData, date: e.target.value})}
                                        />
                                    </div>
                                    <div className="md:col-span-2 space-y-3">
                                        <label className="text-xs font-bold text-gray-500 mr-2 uppercase tracking-widest">ملاحظات توثيق العقد</label>
                                        <textarea 
                                            placeholder="أضف أي تعليمات استراتيجية لفريق العمليات..."
                                            className="w-full bg-white border-none rounded-2xl py-5 px-8 text-black font-bold text-sm outline-none min-h-[120px] focus:ring-4 focus:ring-yellow-500/20 transition-all"
                                            onChange={(e) => setDeliveryData({...deliveryData, notes: e.target.value})}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-8">
                            <div className="glass p-10 rounded-[3rem]">
                                <h3 className="text-xl font-black mb-10 italic border-b border-white/5 pb-4">موجز العملية</h3>
                                <div className="space-y-6 mb-12">
                                    <button 
                                        onClick={() => setIsGifting(false)}
                                        className={`w-full flex items-center justify-between p-6 rounded-[1.5rem] transition-all border ${!isGifting ? 'bg-yellow-500 text-black border-yellow-400' : 'bg-white/5 text-gray-400 border-white/5 hover:bg-white/10'}`}
                                    >
                                        <div className="text-right">
                                            <p className="font-black text-lg">اقتناء شخصي</p>
                                            <small className={!isGifting ? 'text-black/60 font-bold' : 'text-gray-600'}>ترحيل الملكية لمحفظتي</small>
                                        </div>
                                        <Icon name="ShieldCheck" size={28} />
                                    </button>

                                    <button 
                                        onClick={() => setIsGifting(true)}
                                        className={`w-full flex items-center justify-between p-6 rounded-[1.5rem] transition-all border ${isGifting ? 'bg-yellow-500 text-black border-yellow-400' : 'bg-white/5 text-gray-400 border-white/5 hover:bg-white/10'}`}
                                    >
                                        <div className="text-right">
                                            <p className="font-black text-lg">إرسال كهدية</p>
                                            <small className={isGifting ? 'text-black/60 font-bold' : 'text-gray-600'}>إهداء لقائد زميل</small>
                                        </div>
                                        <Icon name="Gift" size={28} />
                                    </button>

                                    {isGifting && (
                                        <div className="animate-view mt-6">
                                            <input 
                                                type="text" 
                                                placeholder="أدخل المعرف UUID للمستلم..."
                                                className="w-full bg-white border-none rounded-2xl py-5 px-8 text-black font-bold text-sm outline-none shadow-inner"
                                            />
                                        </div>
                                    )}
                                </div>

                                <div className="space-y-4 pt-4">
                                    <div className="flex justify-between items-center text-gray-400 font-bold">
                                        <span>قيمة الأصول:</span>
                                        <span>${cartTotal.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between items-center text-3xl font-black text-white">
                                        <span>المستحق:</span>
                                        <span className="text-[#00FF88]">${cartTotal.toLocaleString()}</span>
                                    </div>
                                </div>
                            </div>

                            <button 
                                onClick={() => {
                                    if(balance >= cartTotal) {
                                        setBalance(b => b - cartTotal);
                                        setCart([]);
                                        setCurrentView('market');
                                        alert("تم تأكيد الضخ المالي بنجاح! سيتم مراجعة بيانات السيادة اللوجستية.");
                                    } else {
                                        alert("عذراً، الرصيد المتاح لا يغطي تكلفة الأصول.");
                                    }
                                }}
                                className="w-full py-10 rounded-[3rem] font-black text-2xl bg-gradient-to-r from-yellow-600 to-yellow-400 text-black hover:scale-[1.03] transition-all shadow-[0_25px_60px_rgba(234,179,8,0.3)] flex items-center justify-center gap-4 uppercase"
                            >
                                <Icon name="Zap" />
                                تأكيد الضخ المالي 🚀
                            </button>
                        </div>
                    </div>
                </div>
            );

            // --- واجهة المتجر الرئيسية ---
            const MarketView = () => (
                <div className="animate-view">
                    <div className="flex gap-3 overflow-x-auto no-scrollbar mb-10 pb-2">
                        {CATEGORIES.map(cat => (
                            <button 
                                key={cat} 
                                onClick={() => setSelectedCategory(cat)}
                                className={`px-10 py-4 rounded-2xl text-sm font-black whitespace-nowrap transition-all ${selectedCategory === cat ? 'bg-yellow-500 text-black shadow-xl shadow-yellow-500/20' : 'bg-white/5 text-gray-500 hover:bg-white/10 hover:text-white'}`}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
                        {filtered.map(p => (
                            <div key={p.id} className="group glass rounded-[3rem] overflow-hidden product-card flex flex-col border border-white/5">
                                <div className="relative h-64 overflow-hidden cursor-pointer" onClick={() => setSelectedProduct(p)}>
                                    <img src={p.img} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000" />
                                    <div className="absolute top-6 right-6 bg-black/70 backdrop-blur-md px-4 py-2 rounded-xl flex items-center gap-2 border border-white/10 text-[10px] font-black uppercase tracking-tighter">
                                        <Icon name="MapPin" size={12} className="text-yellow-500" /> {p.country}
                                    </div>
                                    <div className="absolute bottom-6 right-6 bg-yellow-500 text-black px-4 py-1.5 rounded-xl text-[10px] font-black shadow-lg">
                                        {p.category}
                                    </div>
                                </div>
                                <div className="p-10 flex-1 flex flex-col">
                                    <div className="flex justify-between items-center mb-6">
                                        <div className="flex items-center gap-1.5 text-yellow-500 font-black px-3 py-1 bg-yellow-500/10 rounded-lg">
                                            <Icon name="Star" size={14} fill="currentColor" />
                                            <span className="text-xs">{p.rating}</span>
                                        </div>
                                        <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{p.sales} مبيعة</span>
                                    </div>
                                    <h3 className="text-2xl font-black mb-4 line-clamp-1 group-hover:text-yellow-500 transition-colors">{p.name}</h3>
                                    
                                    <div className="flex items-center justify-between border-t border-white/5 pt-8 mt-auto">
                                        <div className="flex flex-col">
                                            <span className="text-[10px] text-gray-500 font-bold uppercase mb-1">القيمة الاستحقاقية</span>
                                            <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                        </div>
                                        <div className="flex gap-2">
                                            <button 
                                                onClick={() => toggleWishlist(p)}
                                                className={`btn-action glass border-white/10 hover:border-red-500/50 ${wishlist.find(i=>i.id===p.id) ? 'text-red-500' : 'text-gray-400'}`}
                                                title="أضف لحائط الأمنيات"
                                            >
                                                <Icon name="Heart" size={20} fill={wishlist.find(i=>i.id===p.id) ? "currentColor" : "none"} />
                                            </button>
                                            <button 
                                                onClick={() => directToGift(p)}
                                                className="btn-action glass border-white/10 hover:border-yellow-500/50 text-gray-400 hover:text-yellow-500"
                                                title="إرسال كهدية"
                                            >
                                                <Icon name="Gift" size={20} />
                                            </button>
                                            <button 
                                                onClick={() => addToCart(p)}
                                                className="btn-action bg-yellow-500 text-black hover:bg-white transition-all shadow-lg"
                                                title="أضف للسلة"
                                            >
                                                <Icon name="ShoppingBag" size={20} />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );

            return (
                <div className="min-h-screen p-4 md:p-8 animate-view">
                    <Header />

                    <main className="max-w-[1600px] mx-auto pb-24">
                        {currentView === 'market' && <MarketView />}
                        {currentView === 'wishlist' && <WishlistView />}
                        {currentView === 'checkout' && <CheckoutView />}
                    </main>

                    <ProductModal />

                    {/* --- السلة الجانبية (Cart Sidebar) --- */}
                    {isCartOpen && (
                        <div className="fixed inset-0 z-[150] flex justify-end">
                            <div className="absolute inset-0 bg-black/80 backdrop-blur-md transition-all" onClick={() => setIsCartOpen(false)} />
                            <div className="relative w-full max-w-md bg-[#050505] border-l border-yellow-500/20 shadow-2xl h-full flex flex-col p-10 animate-view">
                                <div className="flex items-center justify-between mb-12">
                                    <div className="flex items-center gap-4">
                                        <div className="bg-yellow-500 p-2 rounded-xl text-black shadow-lg">
                                            <Icon name="ShoppingBag" size={28} />
                                        </div>
                                        <h2 className="text-3xl font-black tracking-tighter uppercase">سلة الضخ المالي</h2>
                                    </div>
                                    <button onClick={() => setIsCartOpen(false)} className="p-3 hover:bg-white/5 rounded-2xl transition-colors">
                                        <Icon name="X" size={28} />
                                    </button>
                                </div>
                                <div className="flex-1 overflow-y-auto space-y-6 no-scrollbar">
                                    {cart.length === 0 ? (
                                        <div className="text-center py-20 opacity-20">
                                            <Icon name="ShoppingBag" size={80} className="mx-auto mb-6" />
                                            <p className="text-xl font-black uppercase tracking-widest text-white">السلة فارغة</p>
                                        </div>
                                    ) : (
                                      cart.map(item => (
                                        <div key={item.id} className="bg-white/5 p-6 rounded-[2.5rem] border border-white/5 flex gap-6 animate-view group relative overflow-hidden">
                                            <img src={item.img} className="w-20 h-20 rounded-2xl object-cover border border-white/10" />
                                            <div className="flex-1">
                                                <h4 className="font-black text-lg line-clamp-1 mb-1">{item.name}</h4>
                                                <span className="text-[#00FF88] font-black text-xl">${item.price.toLocaleString()}</span>
                                                <p className="text-[10px] text-gray-500 font-bold mt-2 uppercase">📍 {item.country}</p>
                                            </div>
                                            <button onClick={() => removeFromCart(item.id)} className="text-gray-600 hover:text-red-500 transition-all p-2 bg-white/5 rounded-xl self-start">
                                                <Icon name="Trash2" size={18} />
                                            </button>
                                        </div>
                                      )))}
                                </div>
                                {cart.length > 0 && (
                                    <div className="mt-12 pt-10 border-t border-white/5 space-y-8 animate-view">
                                        <div className="flex justify-between items-center">
                                            <span className="text-gray-500 font-bold text-lg uppercase tracking-wider">الإجمالي المستحق</span>
                                            <span className="text-4xl font-black text-[#00FF88] tracking-tighter">${cartTotal.toLocaleString()}</span>
                                        </div>
                                        <button 
                                            onClick={() => { setIsCartOpen(false); setCurrentView('checkout'); }}
                                            className="w-full py-7 rounded-[2.5rem] font-black text-xl bg-yellow-500 text-black hover:scale-[1.02] transition-all shadow-[0_20px_50px_rgba(234,179,8,0.2)] uppercase tracking-tighter flex items-center justify-center gap-3"
                                        >
                                            التوجه لإتمام الضخ ⚡
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <footer className="mt-20 py-12 border-t border-white/5 text-center opacity-30 text-[10px] font-black uppercase tracking-[0.6em] text-white/50">
                        © 2026 MR7 EMPIRE | GLOBAL SOVEREIGN COMMERCE | BY THE COMMAND OF LEADERS
                    </footer>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات السحابية بشكل يدوي وآمن ---
current_balance = st.session_state.get('cash_balance', 1250000)
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. تشغيل المكون داخل ستريمليت ---
components.html(final_html, height=1800, scrolling=True)

# --- 6. منطق العودة (بايثون Core) ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي (Python Core)"):
    st.switch_page("app.py")
