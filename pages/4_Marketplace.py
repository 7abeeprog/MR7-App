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

# --- 3. بناء واجهة React المتكاملة 2.3 (إصلاح السلة، الألوان، الوصف) ---
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
        body { font-family: 'Tajawal', sans-serif; margin: 0; overflow-x: hidden; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .glass { backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .product-card { transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .product-card:hover { transform: translateY(-10px); }
        .animate-view { animation: fadeIn 0.4s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
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
            // --- إعدادات الأنماط (Themes) ---
            const themes = {
                "غامق إمبراطوري 🖤": { bg: "bg-[#000000]", text: "text-white", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", card: "bg-[#111111]", border: "border-[#FFD700]/20" },
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", card: "bg-white", border: "border-[#B8860B]/20" },
                "أزرق القيادة 💙": { bg: "bg-[#001F3F]", text: "text-white", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", card: "bg-[#001529]", border: "border-[#0074D9]/20" },
                "أخضر الاستدامة 💚": { bg: "bg-[#002B1B]", text: "text-white", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", card: "bg-[#001A10]", border: "border-[#00FF88]/20" }
            };

            const activeTheme = themes["CURRENT_THEME_PLACEHOLDER"] || themes["غامق إمبراطوري 🖤"];

            // --- حالات النظام ---
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

            const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "أصول فاخرة"];
            const COUNTRIES = ["الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "المغرب", "عالمي"];

            // --- قاعدة البيانات المتكاملة ---
            const products = [
                { 
                    id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت', 
                    img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600', rating: 5.0, sales: 12,
                    desc: 'تحفة معمارية في العاصمة الإدارية الجديدة، مصممة بأعلى معايير الاستدامة والذكاء الاصطناعي لإدارة المكاتب التنفيذية.'
                },
                { 
                    id: 'p2', name: 'منظومة الطاقة X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', 
                    img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=600', rating: 4.8, sales: 85,
                    desc: 'محطة طاقة شمسية متنقلة قادرة على تغذية مجمعات سكنية كاملة، مع نظام تخزين طاقة متطور وتقنيات تبريد مدمجة.'
                },
                { 
                    id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'MR7 Academy', 
                    img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600', rating: 4.9, sales: 1240,
                    desc: 'المنهج الدراسي الأكثر تأثيراً لبناء العقلية الاستثمارية السيادية وتحويل الأفكار إلى تدفقات نقدية عابرة للحدود.'
                },
                { 
                    id: 'p4', name: 'وكيل الذكاء الاصطناعي', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'سيادة تيك', 
                    img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600', rating: 5.0, sales: 320,
                    desc: 'عميل مستقل مبرمج بلغة بايثون المتطورة، يقوم بإدارة محفظتك المالية وتنبيهك بفرص الضخ المالي الأكثر ربحية.'
                },
                { 
                    id: 'p5', name: 'يخت الامتياز الملكي', price: 850000, country: 'الإمارات', category: 'أصول فاخرة', vendor: 'رويال مارين', 
                    img: 'https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=600', rating: 4.9, sales: 3,
                    desc: 'يخت ملكي مجهز بأحدث تقنيات الملاحة والرفاهية، مثالي لعقد صفقات القادة الكبرى في أعالي البحار.'
                }
            ];

            useEffect(() => { lucide.createIcons(); }, [searchTerm, selectedCountry, selectedCategory, isCartOpen, currentView, selectedProduct, cart, wishlist]);

            const filtered = products.filter(p => {
                const matchSearch = p.name.includes(searchTerm) || p.vendor.includes(searchTerm);
                const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
                const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
                return matchSearch && matchCountry && matchCategory;
            });

            // --- منطق العمليات السيادية ---
            const addToCart = (product) => {
                setCart(prev => {
                    if (prev.find(item => item.id === product.id)) return prev;
                    return [...prev, product];
                });
                setIsCartOpen(true);
            };

            const toggleWishlist = (product) => {
                setWishlist(prev => {
                    if (prev.find(i => i.id === product.id)) return prev.filter(i => i.id !== product.id);
                    return [...prev, product];
                });
            };

            const cartTotal = cart.reduce((s, i) => s + i.price, 0);

            // --- المكونات الفرعية ---
            const ProductModal = () => {
                if (!selectedProduct) return null;
                return (
                    <div className="fixed inset-0 z-[300] flex items-center justify-center p-4 bg-black/95 backdrop-blur-md animate-view">
                        <div className={`${activeTheme.card} w-full max-w-3xl rounded-[3rem] overflow-hidden relative border ${activeTheme.border}`}>
                            <button onClick={() => setSelectedProduct(null)} className="absolute top-8 left-8 p-3 bg-white/10 rounded-full hover:bg-white/20 z-10">
                                <Icon name="X" size={24} className={activeTheme.text} />
                            </button>
                            <div className="flex flex-col md:flex-row h-full">
                                <img src={selectedProduct.img} className="w-full md:w-1/2 h-80 md:h-auto object-cover" />
                                <div className="p-10 flex-1 flex flex-col justify-between">
                                    <div>
                                        <div className="flex justify-between items-center mb-6">
                                            <span className={`${activeTheme.btn} text-black px-4 py-1 rounded-full text-[10px] font-black uppercase`}>{selectedProduct.category}</span>
                                            <span className={`${activeTheme.accent} font-black`}>📍 {selectedProduct.country}</span>
                                        </div>
                                        <h2 className={`text-3xl font-black mb-6 ${activeTheme.text}`}>{selectedProduct.name}</h2>
                                        <p className="text-gray-400 leading-relaxed text-lg mb-8">{selectedProduct.desc}</p>
                                    </div>
                                    <div className="flex items-center justify-between border-t border-white/5 pt-8">
                                        <div className="flex flex-col">
                                            <span className="text-xs text-gray-500 uppercase font-bold">قيمة الضخ</span>
                                            <span className="text-3xl font-black text-[#00FF88]">${selectedProduct.price.toLocaleString()}</span>
                                        </div>
                                        <button 
                                            onClick={() => { addToCart(selectedProduct); setSelectedProduct(null); }}
                                            className={`${activeTheme.btn} text-black px-10 py-4 rounded-2xl font-black text-xl hover:scale-105 transition-all`}
                                        >
                                            إضافة للسلة ⚡
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            return (
                <div className={`min-h-screen ${activeTheme.bg} ${activeTheme.text} p-4 md:p-8 animate-view`}>
                    {/* Header */}
                    <nav className={`flex flex-col md:flex-row justify-between items-center mb-10 gap-6 glass p-6 rounded-[2.5rem] sticky top-0 z-[100] ${activeTheme.border}`}>
                        <div className="flex items-center gap-4 cursor-pointer" onClick={() => setCurrentView('market')}>
                            <div className={`${activeTheme.btn} p-3 rounded-2xl shadow-xl text-black`}>
                                <Icon name="Store" size={28} />
                            </div>
                            <div>
                                <h1 className={`text-2xl font-black tracking-tighter uppercase ${activeTheme.accent}`}>MR7 GLOBAL</h1>
                                <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Sovereign Marketplace</p>
                            </div>
                        </div>

                        <div className="flex-1 max-w-xl w-full relative text-black">
                            <input 
                                type="text" 
                                placeholder="ابحث عن أصل، قسم، أو تاجر سيادي..."
                                className="w-full bg-white border-none rounded-2xl py-4 px-6 focus:ring-2 focus:ring-yellow-500 outline-none transition-all font-bold text-sm"
                                value={searchTerm}
                                onChange={e => setSearchTerm(e.target.value)}
                            />
                        </div>

                        <div className="flex items-center gap-6">
                            <div className="flex flex-col items-end">
                                <span className="text-[10px] text-gray-500 font-black uppercase">الخزنة</span>
                                <div className="flex items-center gap-2 text-[#00FF88] font-black text-xl">
                                    <Icon name="Wallet" size={18} />
                                    <span>${balance.toLocaleString()}</span>
                                </div>
                            </div>
                            <button onClick={() => setCurrentView('wishlist')} className="p-3 bg-white/5 rounded-2xl hover:bg-white/10 relative">
                                <Icon name="Heart" size={24} className={wishlist.length > 0 ? "text-red-500" : ""} fill={wishlist.length > 0 ? "currentColor" : "none"} />
                                {wishlist.length > 0 && <span className="absolute -top-1 -left-1 bg-red-500 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full">{wishlist.length}</span>}
                            </button>
                            <button onClick={() => setIsCartOpen(true)} className="relative p-3 bg-white/5 rounded-2xl hover:bg-white/10 transition-all border border-white/10">
                                <Icon name="ShoppingBag" size={28} />
                                {cart.length > 0 && <span className="absolute -top-1 -left-1 bg-yellow-500 text-black text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-4 border-[#020202]">
                                    {cart.length}
                                </span>}
                            </button>
                        </div>
                    </nav>

                    <main className="max-w-[1600px] mx-auto pb-24">
                        {currentView === 'market' && (
                            <div className="animate-view">
                                <div className="flex gap-3 overflow-x-auto no-scrollbar mb-10 pb-2">
                                    {CATEGORIES.map(cat => (
                                        <button 
                                            key={cat} 
                                            onClick={() => setSelectedCategory(cat)}
                                            className={`px-10 py-4 rounded-2xl text-sm font-black whitespace-nowrap transition-all ${selectedCategory === cat ? `${activeTheme.btn} text-black shadow-xl` : `bg-white/5 text-gray-500 hover:bg-white/10`}`}
                                        >
                                            {cat}
                                        </button>
                                    ))}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
                                    {filtered.map(p => (
                                        <div key={p.id} className={`${activeTheme.card} rounded-[3rem] overflow-hidden product-card flex flex-col border ${activeTheme.border}`}>
                                            <div className="relative h-64 overflow-hidden cursor-pointer" onClick={() => setSelectedProduct(p)}>
                                                <img src={p.img} className="w-full h-full object-cover transition-transform duration-1000 hover:scale-110" />
                                                <div className="absolute top-6 right-6 bg-black/70 backdrop-blur-md px-4 py-2 rounded-xl flex items-center gap-2 border border-white/10 text-[10px] font-black uppercase">
                                                    <Icon name="MapPin" size={12} className={activeTheme.accent} /> {p.country}
                                                </div>
                                            </div>
                                            <div className="p-8 flex-1 flex flex-col">
                                                <div className="flex justify-between items-center mb-4">
                                                    <div className={`flex items-center gap-1.5 px-3 py-1 bg-white/5 rounded-lg font-black ${activeTheme.accent}`}>
                                                        <Icon name="Star" size={14} fill="currentColor" /> {p.rating}
                                                    </div>
                                                    <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{p.sales} مبيعة</span>
                                                </div>
                                                <h3 className="text-2xl font-black mb-4 line-clamp-1 group-hover:text-yellow-500">{p.name}</h3>
                                                <div className="mt-auto flex items-center justify-between border-t border-white/5 pt-6">
                                                    <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                                    <div className="flex gap-2">
                                                        <button onClick={() => toggleWishlist(p)} className={`p-3 glass rounded-xl ${wishlist.find(i=>i.id===p.id) ? 'text-red-500' : 'text-gray-400'}`}>
                                                            <Icon name="Heart" size={18} fill={wishlist.find(i=>i.id===p.id) ? "currentColor" : "none"} />
                                                        </button>
                                                        <button onClick={() => { addToCart(p); setIsGifting(true); setCurrentView('checkout'); }} className="p-3 glass rounded-xl text-gray-400 hover:text-yellow-500">
                                                            <Icon name="Gift" size={18} />
                                                        </button>
                                                        <button onClick={() => addToCart(p)} className={`${activeTheme.btn} text-black p-3 rounded-xl`}>
                                                            <Icon name="ShoppingBag" size={18} />
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {currentView === 'wishlist' && (
                            <div className="animate-view">
                                <div className="flex items-center gap-4 mb-12">
                                    <button onClick={() => setCurrentView('market')} className="p-4 glass rounded-2xl hover:bg-yellow-500 hover:text-black"><Icon name="ArrowRight" /></button>
                                    <h2 className="text-4xl font-black tracking-tighter italic">حائط الأمنيات الاستراتيجي 🏛️</h2>
                                </div>
                                {wishlist.length === 0 ? (
                                    <div className="text-center py-32 opacity-20 border-2 border-dashed border-white/10 rounded-[3rem]">
                                        <Icon name="Heart" size={100} className="mx-auto mb-6" />
                                        <p className="text-2xl font-black uppercase">حائطك خالٍ.. اختر أصول مستقبلك الآن</p>
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                                        {wishlist.map(p => (
                                            <div key={p.id} className={`${activeTheme.card} p-8 rounded-[3rem] border ${activeTheme.border} group`}>
                                                <img src={p.img} className="w-full h-48 object-cover rounded-3xl mb-6 group-hover:scale-105 transition-all" />
                                                <h4 className="text-2xl font-black mb-2">{p.name}</h4>
                                                <div className="flex justify-between items-center mt-6">
                                                    <span className="text-2xl font-black text-[#00FF88]">${p.price.toLocaleString()}</span>
                                                    <div className="flex gap-2">
                                                        <button onClick={() => toggleWishlist(p)} className="p-3 text-red-500 glass rounded-xl"><Icon name="X" size={18} /></button>
                                                        <button onClick={() => addToCart(p)} className={`${activeTheme.btn} text-black px-6 py-3 rounded-xl font-black`}>نقل للسلة</button>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {currentView === 'checkout' && (
                            <div className="animate-view max-w-6xl mx-auto">
                                <div className="flex items-center gap-4 mb-12">
                                    <button onClick={() => setCurrentView('market')} className="p-4 glass rounded-2xl hover:bg-yellow-500 hover:text-black"><Icon name="ArrowRight" /></button>
                                    <h2 className="text-4xl font-black tracking-tighter italic">إتمام الضخ المالي 🛡️</h2>
                                </div>
                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                                    <div className="lg:col-span-2 space-y-8">
                                        <div className={`${activeTheme.card} p-10 rounded-[3rem] border ${activeTheme.border}`}>
                                            <h3 className="text-xl font-black mb-8 flex items-center gap-3">📦 ملخص الأصول في السلة</h3>
                                            <div className="space-y-4">
                                                {cart.map(item => (
                                                    <div key={item.id} className="flex justify-between items-center bg-white/5 p-6 rounded-3xl border border-white/5">
                                                        <div className="flex items-center gap-6">
                                                            <img src={item.img} className="w-20 h-20 rounded-2xl object-cover" />
                                                            <div>
                                                                <p className="font-black text-xl">{item.name}</p>
                                                                <small className="text-gray-500 uppercase tracking-widest">{item.vendor} | {item.country}</small>
                                                            </div>
                                                        </div>
                                                        <span className="text-2xl font-black text-[#00FF88]">${item.price.toLocaleString()}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                        <div className={`${activeTheme.card} p-10 rounded-[3rem] border ${activeTheme.border}`}>
                                            <h3 className="text-xl font-black mb-8 italic">📍 بيانات الاستلام اللوجستية</h3>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-black">
                                                <input type="text" placeholder="عنوان الاستلام الدقيق..." className="w-full bg-white p-5 rounded-2xl font-bold outline-none" />
                                                <input type="date" className="w-full bg-white p-5 rounded-2xl font-bold outline-none" />
                                                <textarea placeholder="ملاحظات توثيق العملية..." className="md:col-span-2 w-full bg-white p-5 rounded-2xl font-bold outline-none h-32"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="space-y-8">
                                        <div className={`${activeTheme.card} p-10 rounded-[3rem] border ${activeTheme.border}`}>
                                            <h3 className="text-xl font-black mb-10 uppercase tracking-widest">تأكيد العملية</h3>
                                            <div className="space-y-6 mb-12">
                                                <button onClick={() => setIsGifting(false)} className={`w-full flex justify-between p-6 rounded-2xl transition-all ${!isGifting ? `${activeTheme.btn} text-black` : 'bg-white/5 text-gray-500'}`}>
                                                    <span>اقتناء شخصي</span> <Icon name="ShieldCheck" />
                                                </button>
                                                <button onClick={() => setIsGifting(true)} className={`w-full flex justify-between p-6 rounded-2xl transition-all ${isGifting ? `${activeTheme.btn} text-black` : 'bg-white/5 text-gray-500'}`}>
                                                    <span>إرسال كهدية</span> <Icon name="Gift" />
                                                </button>
                                                {isGifting && <input type="text" placeholder="معرف UUID للمستلم..." className="w-full bg-white p-5 rounded-2xl font-bold text-black outline-none animate-view" />}
                                            </div>
                                            <div className="flex justify-between items-center text-3xl font-black border-t border-white/10 pt-10">
                                                <span className="text-lg text-gray-500">الإجمالي:</span>
                                                <span className="text-[#00FF88]">${cartTotal.toLocaleString()}</span>
                                            </div>
                                        </div>
                                        <button onClick={() => { if(balance >= cartTotal) { setBalance(b => b - cartTotal); setCart([]); setCurrentView('market'); alert("تم الضخ المالي بنجاح!"); } else { alert("الرصيد غير كافٍ"); }}} className={`w-full py-10 rounded-[3rem] font-black text-2xl ${activeTheme.btn} text-black hover:scale-105 transition-all shadow-2xl`}>تأكيد الضخ المالي 🚀</button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </main>

                    <ProductModal />

                    {/* Cart Sidebar */}
                    {isCartOpen && (
                        <div className="fixed inset-0 z-[200] flex justify-end">
                            <div className="absolute inset-0 bg-black/80 backdrop-blur-md" onClick={() => setIsCartOpen(false)} />
                            <div className={`relative w-full max-w-md ${activeTheme.card} border-l ${activeTheme.border} shadow-2xl h-full flex flex-col p-10 animate-view`}>
                                <div className="flex items-center justify-between mb-12">
                                    <div className="flex items-center gap-4">
                                        <div className={`${activeTheme.btn} p-2 rounded-xl text-black`}><Icon name="ShoppingBag" /></div>
                                        <h2 className="text-2xl font-black uppercase tracking-widest">سلة الضخ المالي</h2>
                                    </div>
                                    <button onClick={() => setIsCartOpen(false)} className="p-3 bg-white/5 rounded-2xl"><Icon name="X" /></button>
                                </div>
                                <div className="flex-1 overflow-y-auto space-y-6 no-scrollbar">
                                    {cart.length === 0 ? <div className="text-center opacity-20 py-20 text-xl font-black">السلة فارغة</div> : 
                                      cart.map(item => (
                                        <div key={item.id} className="bg-white/5 p-6 rounded-[2.5rem] border border-white/5 flex gap-6 animate-view">
                                            <img src={item.img} className="w-20 h-20 rounded-2xl object-cover" />
                                            <div className="flex-1">
                                                <h4 className="font-black text-lg mb-1">{item.name}</h4>
                                                <span className="text-[#00FF88] font-black text-xl">${item.price.toLocaleString()}</span>
                                            </div>
                                            <button onClick={() => setCart(cart.filter(i=>i.id!==item.id))} className="text-gray-500 hover:text-red-500"><Icon name="Trash2" size={20} /></button>
                                        </div>
                                      ))}
                                </div>
                                {cart.length > 0 && (
                                    <div className="mt-10 pt-10 border-t border-white/10 space-y-8 animate-view">
                                        <div className="flex justify-between items-center"><span className="text-gray-500 font-bold">الإجمالي المستحق</span><span className="text-3xl font-black text-[#00FF88]">${cartTotal.toLocaleString()}</span></div>
                                        <button onClick={() => { setIsCartOpen(false); setCurrentView('checkout'); }} className={`w-full py-6 rounded-2xl font-black text-xl ${activeTheme.btn} text-black hover:scale-105 transition-all`}>التوجه لإتمام العملية ⚡</button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <footer className="mt-20 py-12 border-t border-white/5 text-center opacity-30 text-[10px] font-black uppercase tracking-[0.8em]">
                        © 2026 MR7 EMPIRE | GLOBAL MARKETPLACE | BY THE ORDER OF LEADERS
                        <div className="flex justify-center gap-10 mt-10">
                            <button onClick={() => setIsGifting(true) || setCurrentView('checkout')} className="hover:text-yellow-500 flex items-center gap-2"><Icon name="Gift" size={14} /> أرسل كهدية</button>
                            <button onClick={() => setCurrentView('wishlist')} className="hover:text-red-500 flex items-center gap-2"><Icon name="Heart" size={14} /> حائط الأمنيات</button>
                        </div>
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

# --- 4. حقن المتغيرات والأنماط بشكل آمن ---
current_balance = st.session_state.get('cash_balance', 1250000)
# استبدال الثوابت في كود الـ React
final_html = react_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))
final_html = final_html.replace("CURRENT_THEME_PLACEHOLDER", current_theme)

# --- 5. تشغيل المكون داخل ستريمليت ---
components.html(final_html, height=1800, scrolling=True)

# --- 6. منطق العودة (بايثون Core) ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي (Python Core)"):
    st.switch_page("app.py")
