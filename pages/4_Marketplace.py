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

# --- 3. بناء واجهة React المتكاملة ---
# ملاحظة: تم إزالة حرف f لتجنب أي SyntaxError مع أقواس JavaScript
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
            backdrop-filter: blur(15px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
        }
        .product-card:hover { 
            border-color: rgba(234, 179, 8, 0.4); 
            transform: translateY(-8px); 
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        }
        .gradient-text {
            background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade { animation: fade-in 0.5s ease-out forwards; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

        const Icon = ({ name, size = 24, className = "" }) => {
            const LucideIcon = lucide[name];
            return LucideIcon ? <i data-lucide={name} className={className} style={{ width: size, height: size }}></i> : null;
        };

        const App = () => {
            // --- حالات النظام (System States) ---
            const [currentView, setCurrentView] = useState('market'); // market | wishlist | checkout
            const [searchTerm, setSearchTerm] = useState('');
            const [selectedCountry, setSelectedCountry] = useState('الكل');
            const [selectedCategory, setSelectedCategory] = useState('الكل');
            const [balance, setBalance] = useState(LEADER_BALANCE_PLACEHOLDER);
            const [cart, setCart] = useState([]);
            const [wishlist, setWishlist] = useState([]);
            const [isCartOpen, setIsCartOpen] = useState(false);
            const [isGifting, setIsGifting] = useState(false);

            const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "استشارات تريليونية", "أصول فاخرة"];
            const COUNTRIES = ["الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "قطر", "المغرب", "تركيا", "عالمي"];

            // --- قاعدة البيانات المبدئية الضخمة (Expanded Mock Data) ---
            const products = [
                { id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت العقارية', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600', rating: 5.0, sales: 12 },
                { id: 'p2', name: 'منظومة الطاقة X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=600', rating: 4.8, sales: 85 },
                { id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'MR7 Academy', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600', rating: 4.9, sales: 1240 },
                { id: 'p4', name: 'وكيل الذكاء الاصطناعي السيادي', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'مختبرات السيادة', img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600', rating: 5.0, sales: 320 },
                { id: 'p5', name: 'يخت الامتياز الملكي', price: 850000, country: 'الإمارات', category: 'أصول فاخرة', vendor: 'مارين نبت', img: 'https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=600', rating: 4.9, sales: 3 },
                { id: 'p6', name: 'مزرعة الذهب الأخضر', price: 450000, country: 'السودان', category: 'عقارات سيادية', vendor: 'سودان فيجن', img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600', rating: 4.7, sales: 15 },
                { id: 'p7', name: 'استشارة المليار السنوية', price: 5000, country: 'عالمي', category: 'استشارات تريليونية', vendor: 'القائد المؤسس', img: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600', rating: 5.0, sales: 45 },
                { id: 'p8', name: 'سيارة السيادة الكهربائية V1', price: 65000, country: 'مصر', category: 'تقنيات المستقبل', vendor: 'EV Egypt', img: 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600', rating: 4.9, sales: 220 },
                { id: 'p9', name: 'فيلا واجهة البحر بنغازي', price: 280000, country: 'ليبيا', category: 'عقارات سيادية', vendor: 'عقارات ليبيا', img: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600', rating: 4.6, sales: 8 },
                { id: 'p10', name: 'نظام التحكم الكمومي', price: 8500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'كوانتم وورلد', img: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600', rating: 4.8, sales: 112 },
                { id: 'p11', name: 'ماستر كلاس "القيادة العابرة"', price: 150, country: 'عالمي', category: 'أكاديمية القيادة', vendor: 'أكاديمية النخبة', img: 'https://images.unsplash.com/photo-1524178232363-1fb280714553?w=600', rating: 4.9, sales: 3400 },
                { id: 'p12', name: 'ساعة السيادة المرصعة', price: 12000, country: 'عالمي', category: 'أصول فاخرة', vendor: 'رويال تايم', img: 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=600', rating: 5.0, sales: 12 }
            ];

            useEffect(() => {
                lucide.createIcons();
            }, [searchTerm, selectedCountry, selectedCategory, isCartOpen, currentView]);

            // --- فلاتر البحث والمنتجات ---
            const filtered = products.filter(p => {
                const matchSearch = p.name.includes(searchTerm) || p.vendor.includes(searchTerm);
                const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
                const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
                return matchSearch && matchCountry && matchCategory;
            });

            // --- العمليات (Operations) ---
            const addToCart = (product) => {
                if (!cart.find(i => i.id === product.id)) {
                    setCart([...cart, product]);
                    setIsCartOpen(true);
                }
            };

            const toggleWishlist = (product) => {
                if (wishlist.find(i => i.id === product.id)) {
                    setWishlist(wishlist.filter(i => i.id !== product.id));
                } else {
                    setWishlist([...wishlist, product]);
                }
            };

            const cartTotal = cart.reduce((s, i) => s + i.price, 0);

            // --- المكونات الفرعية (Sub-Components) ---
            
            const Header = () => (
                <nav className="flex flex-col md:flex-row justify-between items-center mb-10 gap-6 glass p-6 rounded-[2rem] sticky top-0 z-50">
                    <div className="flex items-center gap-4 cursor-pointer" onClick={() => setCurrentView('market')}>
                        <div className="bg-yellow-500 p-3 rounded-2xl shadow-xl text-black">
                            <Icon name="Store" size={28} />
                        </div>
                        <div>
                            <h1 className="text-2xl font-black text-yellow-500 tracking-tighter uppercase">MR7 GLOBAL</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Sovereign Marketplace</p>
                        </div>
                    </div>

                    <div className="flex-1 max-w-xl w-full relative text-black">
                        <input 
                            type="text" 
                            placeholder="ابحث عن أصول، أقسام، أو تجار سياديين..."
                            className="w-full bg-white border-none rounded-2xl py-4 px-6 focus:ring-2 focus:ring-yellow-500 outline-none transition-all font-bold text-sm"
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="flex flex-col items-end">
                            <span className="text-[10px] text-gray-500 font-black uppercase">خزنة السيولة</span>
                            <div className="flex items-center gap-2 text-[#00FF88] font-black text-xl">
                                <Icon name="Wallet" size={18} />
                                <span>${balance.toLocaleString()}</span>
                            </div>
                        </div>
                        <button onClick={() => setCurrentView('wishlist')} className="p-3 bg-white/5 rounded-2xl hover:bg-white/10 relative">
                            <Icon name="Heart" size={24} className={wishlist.length > 0 ? "text-red-500 fill-red-500" : ""} />
                            {wishlist.length > 0 && <span className="absolute -top-1 -left-1 bg-red-500 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full">{wishlist.length}</span>}
                        </button>
                        <button onClick={() => setIsCartOpen(true)} className="relative p-3 bg-white/5 rounded-2xl hover:bg-white/10 transition-all">
                            <Icon name="ShoppingBag" size={28} />
                            {cart.length > 0 && <span className="absolute -top-1 -left-1 bg-yellow-500 text-black text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-4 border-[#020202]">
                                {cart.length}
                            </span>}
                        </button>
                    </div>
                </nav>
            );

            // --- واجهة السوق الرئيسية ---
            const MarketView = () => (
                <div className="animate-fade">
                    <div className="flex gap-3 overflow-x-auto no-scrollbar mb-8 pb-2">
                        {CATEGORIES.map(cat => (
                            <button 
                                key={cat} 
                                onClick={() => setSelectedCategory(cat)}
                                className={`px-8 py-3 rounded-xl text-sm font-black whitespace-nowrap transition-all ${
                                    selectedCategory === cat ? 'bg-yellow-500 text-black shadow-lg' : 'bg-white/5 text-gray-500 hover:bg-white/10'
                                }`}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>

                    <div className="mb-10 flex flex-wrap items-center gap-4 bg-white/5 p-4 rounded-2xl border border-white/5">
                        <div className="flex items-center gap-2 text-gray-400 font-bold text-sm px-2">
                            <Icon name="Globe" size={18} className="text-yellow-500" />
                            تصفية حسب الدولة:
                        </div>
                        <div className="flex gap-2 overflow-x-auto no-scrollbar">
                            {COUNTRIES.map(c => (
                                <button 
                                    key={c} 
                                    onClick={() => setSelectedCountry(c)}
                                    className={`px-4 py-2 rounded-lg text-xs font-black transition-all ${
                                        selectedCountry === c ? 'bg-white text-black shadow-md' : 'bg-white/5 text-gray-500 hover:bg-white/10'
                                    }`}
                                >
                                    {c}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {filtered.map(p => (
                            <div key={p.id} className="group glass rounded-[2.5rem] overflow-hidden product-card flex flex-col">
                                <div className="relative h-64 overflow-hidden">
                                    <img src={p.img} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
                                    <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-xl flex items-center gap-2 border border-white/10 text-[10px] font-black uppercase">
                                        <Icon name="MapPin" size={12} className="text-yellow-500" /> {p.country}
                                    </div>
                                    <button 
                                        onClick={() => toggleWishlist(p)}
                                        className="absolute top-4 left-4 bg-black/50 p-2 rounded-full hover:bg-white transition-colors group/wish"
                                    >
                                        <Icon name="Heart" size={18} className={wishlist.find(i => i.id === p.id) ? "text-red-500 fill-red-500" : "text-white group-hover/wish:text-black"} />
                                    </button>
                                    <div className="absolute bottom-4 right-4 bg-yellow-500 text-black px-4 py-1.5 rounded-xl text-[10px] font-black shadow-lg">
                                        {p.category}
                                    </div>
                                </div>
                                <div className="p-8 flex-1 flex flex-col">
                                    <div className="flex justify-between items-center mb-4">
                                        <div className="flex items-center gap-1 text-yellow-500"><Icon name="Star" size={14} /><span className="text-xs font-black">{p.rating}</span></div>
                                        <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{p.sales} مبيعة</span>
                                    </div>
                                    <h3 className="text-xl font-black mb-2 line-clamp-1 group-hover:text-yellow-500 transition-colors">{p.name}</h3>
                                    <p className="text-gray-500 text-xs font-bold mb-6 italic">التاجر: {p.vendor}</p>
                                    <div className="mt-auto flex items-center justify-between border-t border-white/5 pt-6">
                                        <div className="flex flex-col">
                                            <span className="text-[10px] text-gray-500 font-bold uppercase">قيمة الأصل</span>
                                            <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                        </div>
                                        <button 
                                            onClick={() => addToCart(p)} 
                                            className="bg-white text-black h-14 w-14 rounded-2xl flex items-center justify-center hover:bg-yellow-500 transition-all active:scale-90 shadow-lg"
                                        >
                                            <Icon name="ChevronRight" size={28} strokeWidth={3} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );

            // --- واجهة حائط الأمنيات (Wish Wall) ---
            const WishlistView = () => (
                <div className="animate-fade">
                    <div className="flex items-center gap-4 mb-8">
                        <button onClick={() => setCurrentView('market')} className="bg-white/5 p-3 rounded-xl hover:bg-yellow-500 hover:text-black transition-all">
                            <Icon name="ArrowRight" size={24} />
                        </button>
                        <h2 className="text-3xl font-black">حائط الأمنيات الاستراتيجي</h2>
                    </div>
                    {wishlist.length === 0 ? (
                        <div className="text-center py-20 opacity-20">
                            <Icon name="Heart" size={80} className="mx-auto mb-4" />
                            <p className="text-2xl font-black">حائطك خالٍ.. اختر الأصول التي تطمح لسيادتها</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {wishlist.map(p => (
                                <div key={p.id} className="glass p-6 rounded-3xl relative">
                                    <img src={p.img} className="w-full h-40 object-cover rounded-2xl mb-4" />
                                    <h4 className="font-black mb-2">{p.name}</h4>
                                    <span className="text-[#00FF88] font-black block mb-4">${p.price.toLocaleString()}</span>
                                    <div className="flex gap-2">
                                        <button onClick={() => addToCart(p)} className="flex-1 bg-yellow-500 text-black py-2 rounded-xl font-bold text-sm">نقل للسلة</button>
                                        <button onClick={() => toggleWishlist(p)} className="p-2 bg-red-500/20 text-red-500 rounded-xl hover:bg-red-500 hover:text-white transition-all">
                                            <Icon name="X" size={18} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            );

            // --- واجهة إتمام الدفع (Checkout Screen) ---
            const CheckoutView = () => (
                <div className="animate-fade max-w-4xl mx-auto">
                    <div className="flex items-center gap-4 mb-10">
                        <button onClick={() => setCurrentView('market')} className="bg-white/5 p-3 rounded-xl hover:bg-yellow-500 hover:text-black transition-all">
                            <Icon name="ArrowRight" size={24} />
                        </button>
                        <h2 className="text-3xl font-black">إتمام عملية الضخ السيادي</h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                        {/* ملخص الطلب */}
                        <div className="glass p-8 rounded-[2.5rem]">
                            <h3 className="text-xl font-black mb-6 border-b border-white/10 pb-4">ملخص الأصول</h3>
                            <div className="space-y-4 mb-8 max-h-80 overflow-y-auto no-scrollbar">
                                {cart.map(item => (
                                    <div key={item.id} className="flex justify-between items-center bg-white/5 p-4 rounded-2xl">
                                        <div className="flex items-center gap-3">
                                            <img src={item.img} className="w-12 h-12 rounded-lg object-cover" />
                                            <div>
                                                <p className="font-bold text-sm">{item.name}</p>
                                                <small className="text-gray-500">{item.vendor}</small>
                                            </div>
                                        </div>
                                        <span className="text-yellow-500 font-black">${item.price.toLocaleString()}</span>
                                    </div>
                                ))}
                            </div>
                            <div className="flex justify-between items-center text-2xl font-black">
                                <span>الإجمالي:</span>
                                <span className="text-[#00FF88]">${cartTotal.toLocaleString()}</span>
                            </div>
                        </div>

                        {/* خيارات الدفع والسيادة */}
                        <div className="space-y-6">
                            <div className="glass p-8 rounded-[2.5rem]">
                                <h3 className="text-xl font-black mb-6">خيارات العملية</h3>
                                
                                <div className="space-y-4">
                                    <label className="flex items-center gap-4 bg-white/5 p-4 rounded-2xl cursor-pointer hover:bg-white/10 transition-all">
                                        <input type="checkbox" checked={!isGifting} onChange={() => setIsGifting(false)} className="w-6 h-6 accent-yellow-500" />
                                        <div className="flex-1">
                                            <p className="font-black text-sm">اقتناء شخصي</p>
                                            <small className="text-gray-500">ترحيل الأصل لمحفظة سيادتي</small>
                                        </div>
                                        <Icon name="ShieldCheck" />
                                    </label>

                                    <label className="flex items-center gap-4 bg-white/5 p-4 rounded-2xl cursor-pointer hover:bg-white/10 transition-all">
                                        <input type="checkbox" checked={isGifting} onChange={() => setIsGifting(true)} className="w-6 h-6 accent-yellow-500" />
                                        <div className="flex-1">
                                            <p className="font-black text-sm">إرسال كهدية إمبراطورية</p>
                                            <small className="text-gray-500">إرسال الأصل لقائد آخر في الفريق</small>
                                        </div>
                                        <Icon name="Gift" />
                                    </label>

                                    {isGifting && (
                                        <div className="animate-fade mt-4">
                                            <input 
                                                type="text" 
                                                placeholder="أدخل المعرف (UUID) للقائد المستلم..."
                                                className="w-full bg-white border-none rounded-xl py-4 px-6 text-black font-bold text-sm outline-none"
                                            />
                                        </div>
                                    )}
                                </div>
                            </div>

                            <button 
                                onClick={() => {
                                    if(balance >= cartTotal) {
                                        alert("تم تأكيد الضخ المالي! سيتم ترحيل الأصول فوراً.");
                                        setBalance(b => b - cartTotal);
                                        setCart([]);
                                        setCurrentView('market');
                                    } else {
                                        alert("عذراً، السيولة الحالية لا تغطي قيمة الضخ.");
                                    }
                                }}
                                className="w-full py-6 rounded-[2rem] font-black text-xl bg-gradient-to-r from-yellow-600 to-yellow-400 text-black hover:scale-105 transition-all shadow-2xl flex items-center justify-center gap-3"
                            >
                                <Icon name="CreditCard" />
                                تأكيد الضخ المالي 🚀
                            </button>
                        </div>
                    </div>
                </div>
            );

            return (
                <div className="min-h-screen p-4 md:p-8">
                    <Header />

                    <main className="max-w-7xl mx-auto">
                        {currentView === 'market' && <MarketView />}
                        {currentView === 'wishlist' && <WishlistView />}
                        {currentView === 'checkout' && <CheckoutView />}
                    </main>

                    {/* --- السلة الجانبية (Cart Sidebar) --- */}
                    {isCartOpen && (
                        <div className="fixed inset-0 z-[100] flex justify-end">
                            <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={() => setIsCartOpen(false)} />
                            <div className="relative w-full max-w-md bg-[#050505] border-l border-yellow-500/20 shadow-2xl h-full flex flex-col p-10 animate-in slide-in-from-left duration-500">
                                <div className="flex items-center justify-between mb-10">
                                    <div className="flex items-center gap-4">
                                        <Icon name="ShoppingBag" size={32} className="text-yellow-500" />
                                        <h2 className="text-2xl font-black">سلة الضخ</h2>
                                    </div>
                                    <button onClick={() => setIsCartOpen(false)} className="p-3 hover:bg-white/5 rounded-2xl transition-colors"><Icon name="X" size={28} /></button>
                                </div>
                                <div className="flex-1 overflow-y-auto space-y-4 no-scrollbar">
                                    {cart.length === 0 ? <div className="text-center opacity-20 mt-20 text-xl font-black">السلة فارغة</div> : 
                                      cart.map(item => (
                                        <div key={item.id} className="bg-white/5 p-5 rounded-[2rem] border border-white/5 flex gap-5">
                                            <img src={item.img} className="w-16 h-16 rounded-xl object-cover" />
                                            <div className="flex-1">
                                                <h4 className="font-black text-sm line-clamp-1">{item.name}</h4>
                                                <span className="text-[#00FF88] font-black">${item.price.toLocaleString()}</span>
                                            </div>
                                            <button onClick={() => setCart(cart.filter(i => i.id !== item.id))} className="text-gray-500 hover:text-red-500 self-start p-1"><Icon name="X" size={18} /></button>
                                        </div>
                                      ))}
                                </div>
                                {cart.length > 0 && (
                                    <div className="mt-10 pt-10 border-t border-white/5">
                                        <div className="flex justify-between items-center mb-8">
                                            <span className="text-gray-500 font-bold">الإجمالي</span>
                                            <span className="text-3xl font-black text-[#00FF88]">${cartTotal.toLocaleString()}</span>
                                        </div>
                                        <button 
                                            onClick={() => { setIsCartOpen(false); setCurrentView('checkout'); }}
                                            className="w-full py-6 rounded-2xl font-black text-xl bg-yellow-500 text-black hover:scale-105 transition-all shadow-2xl"
                                        >
                                            التوجه لإتمام العملية ⚡
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <footer className="mt-20 py-12 border-t border-white/5 text-center opacity-30 text-xs font-bold uppercase tracking-[0.4em]">
                        © 2026 MR7 EMPIRE | GLOBAL SOVEREIGN COMMERCE
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
# نستخرج الرصيد من الـ session_state أو نضع قيمة افتراضية
current_balance = st.session_state.get('cash_balance', 1250000)
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. تشغيل المكون داخل ستريمليت ---
components.html(final_html, height=1600, scrolling=True)

# --- 6. منطق العودة (بايثون Core) ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي (Python Core)"):
    st.switch_page("app.py")
