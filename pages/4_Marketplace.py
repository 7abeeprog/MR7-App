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
# يتم سحب هذه البيانات من st.secrets لضمان الربط بقاعدة بياناتك الحالية
fb_config_str = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
auth_token = st.secrets.get("__initial_auth_token", "")

# --- 3. بناء واجهة React داخل حاوية HTML مدمجة ---
# نستخدم f-string لتمرير المتغيرات من بايثون إلى جافا سكريبت
# ونستخدم {{ }} في كود الجافا سكريبت لمنع تعارض بايثون مع الأقواس المجعدة
react_html = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    
    <!-- تحميل مكتبات React و Babel للأكواد المدمجة -->
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        body {{ 
            font-family: 'Tajawal', sans-serif; 
            background-color: #020202; 
            margin: 0; 
            overflow-x: hidden; 
            color: white; 
        }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .glass {{ 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(15px); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
        }}
        .product-card:hover {{ 
            border-color: rgba(234, 179, 8, 0.4); 
            transform: translateY(-5px); 
            transition: 0.4s; 
        }}
        /* تحسين مظهر التمرير */
        .custom-scroll::-webkit-scrollbar {{
            width: 6px;
        }}
        .custom-scroll::-webkit-scrollbar-thumb {{
            background: #FFD700;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState, useEffect, useMemo }} = React;

        // مكون الأيقونات
        const Icon = ({{ name, size = 24, className = "" }}) => {{
            const LucideIcon = lucide[name];
            return LucideIcon ? <i data-lucide="{{name}}" className="{{className}}" style={{{{ width: size, height: size }}}}></i> : null;
        }};

        const App = () => {{
            const [searchTerm, setSearchTerm] = useState('');
            const [selectedCountry, setSelectedCountry] = useState('الكل');
            const [selectedCategory, setSelectedCategory] = useState('الكل');
            const [balance, setBalance] = useState(1250000);
            const [cart, setCart] = useState([]);
            const [isCartOpen, setIsCartOpen] = useState(false);

            const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "استشارات تريليونية", "أصول رقمية"];
            const COUNTRIES = [
                "الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "قطر", "الكويت", 
                "سلطنة عمان", "البحرين", "الأردن", "فلسطين", "المغرب", "تونس", "الجزائر", 
                "تركيا", "الولايات المتحدة", "الصين", "ألمانيا", "بريطانيا", "اليابان"
            ];

            // المنتجات المدمجة (بيانات تجريبية راقية)
            const products = [
                {{ id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت العقارية', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600', rating: 5.0, sales: 12 }},
                {{ id: 'p2', name: 'منظومة الطاقة X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=600', rating: 4.8, sales: 85 }},
                {{ id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'أكاديمية MR7', img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600', rating: 4.9, sales: 1240 }},
                {{ id: 'p4', name: 'وكيل الذكاء الاصطناعي السيادي', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'مختبرات السيادة', img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600', rating: 5.0, sales: 320 }}
            ];

            useEffect(() => {{
                lucide.createIcons();
            }}, [searchTerm, selectedCountry, selectedCategory, isCartOpen]);

            const filtered = products.filter(p => {{
                const matchSearch = p.name.includes(searchTerm) || p.vendor.includes(searchTerm);
                const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
                const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
                return matchSearch && matchCountry && matchCategory;
            }});

            const addToCart = (product) => {{
                if (!cart.find(i => i.id === product.id)) {{
                    setCart([...cart, product]);
                    setIsCartOpen(true);
                }}
            }};

            return (
                <div className="min-h-screen p-4 md:p-8">
                    {/* Header */}
                    <nav className="flex flex-col md:flex-row justify-between items-center mb-10 gap-6 glass p-6 rounded-[2rem] sticky top-0 z-50">
                        <div className="flex items-center gap-4">
                            <div className="bg-yellow-500 p-3 rounded-2xl shadow-xl text-black">
                                <Icon name="Store" size={{28}} />
                            </div>
                            <div>
                                <h1 className="text-2xl font-black text-yellow-500 tracking-tighter uppercase">MR7 GLOBAL</h1>
                                <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Sovereign Marketplace</p>
                            </div>
                        </div>

                        <div className="flex-1 max-w-xl w-full relative">
                            <input 
                                type="text" 
                                placeholder="ابحث عن أصول، أقسام، أو تجار سياديين..."
                                className="w-full bg-white border border-white/10 rounded-2xl py-4 px-6 focus:border-yellow-500 outline-none transition-all font-bold text-sm text-black"
                                onChange={{e => setSearchTerm(e.target.value)}}
                            />
                        </div>

                        <div className="flex items-center gap-8">
                            <div className="flex flex-col items-end">
                                <span className="text-[10px] text-gray-500 font-black uppercase">خزنة السيولة</span>
                                <div className="flex items-center gap-2 text-[#00FF88] font-black text-xl">
                                    <Icon name="Wallet" size={{18}} />
                                    <span>${{balance.toLocaleString()}}</span>
                                </div>
                            </div>
                            <button onClick={{() => setIsCartOpen(true)}} className="relative p-3 bg-white/5 rounded-2xl hover:bg-white/10 transition-all">
                                <Icon name="ShoppingBag" size={{28}} />
                                {{cart.length > 0 && <span className="absolute -top-1 -left-1 bg-yellow-500 text-black text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-4 border-[#020202]">
                                    {{cart.length}}
                                </span>}}
                            </button>
                        </div>
                    </nav>

                    {/* Categories Bar */}
                    <div className="flex gap-3 overflow-x-auto no-scrollbar mb-8 pb-2">
                        {{CATEGORIES.map(cat => (
                            <button 
                                key={{cat}} 
                                onClick={{() => setSelectedCategory(cat)}}
                                className={{`px-8 py-3 rounded-xl text-sm font-black whitespace-nowrap transition-all ${{
                                    selectedCategory === cat ? 'bg-yellow-500 text-black shadow-lg shadow-yellow-500/20' : 'bg-white/5 text-gray-500 hover:bg-white/10'
                                }}`}}
                            >
                                {{cat}}
                            </button>
                        ))}}
                    </div>

                    {/* Countries Filter */}
                    <div className="mb-10 flex flex-wrap items-center gap-4 bg-white/5 p-4 rounded-2xl border border-white/5">
                        <div className="flex items-center gap-2 text-gray-400 font-bold text-sm px-2">
                            <Icon name="Globe" size={{18}} className="text-yellow-500" />
                            تصفية حسب الدولة:
                        </div>
                        <div className="flex gap-2 overflow-x-auto no-scrollbar custom-scroll">
                            {{COUNTRIES.map(c => (
                                <button 
                                    key={{c}} 
                                    onClick={{() => setSelectedCountry(c)}}
                                    className={{`px-4 py-2 rounded-lg text-xs font-black transition-all ${{
                                        selectedCountry === c ? 'bg-white text-black shadow-md' : 'bg-white/5 text-gray-500 hover:bg-white/10'
                                    }}`}}
                                >
                                    {{c}}
                                </button>
                            ))}}
                        </div>
                    </div>

                    {/* Product Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {{filtered.map(p => (
                            <div key={{p.id}} className="group glass rounded-[2.5rem] overflow-hidden product-card transition-all duration-500">
                                <div className="relative h-64 overflow-hidden">
                                    <img src={{p.img}} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
                                    <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-xl flex items-center gap-2 border border-white/10 text-[10px] font-black">
                                        <Icon name="MapPin" size={{12}} className="text-yellow-500" /> {{p.country}}
                                    </div>
                                    <div className="absolute bottom-4 left-4 bg-yellow-500 text-black px-4 py-1.5 rounded-xl text-[10px] font-black shadow-lg">{{p.category}}</div>
                                </div>
                                <div className="p-8">
                                    <div className="flex justify-between items-center mb-4">
                                        <div className="flex items-center gap-1 text-yellow-500"><Icon name="Star" size={{14}} /><span className="text-xs font-black">{{p.rating}}</span></div>
                                        <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{{p.sales}} مبيعة</span>
                                    </div>
                                    <h3 className="text-xl font-black mb-2 line-clamp-1 group-hover:text-yellow-500 transition-colors">{{p.name}}</h3>
                                    <p className="text-gray-500 text-xs font-bold mb-6 italic text-left">التاجر: {{p.vendor}}</p>
                                    <div className="flex items-center justify-between border-t border-white/5 pt-6">
                                        <div className="flex flex-col">
                                            <span className="text-[10px] text-gray-500 font-bold uppercase">قيمة الأصل</span>
                                            <span className="text-2xl font-black text-[#00FF88]">${{p.price.toLocaleString()}}</span>
                                        </div>
                                        <button onClick={{() => addToCart(p)}} className="bg-white text-black h-14 w-14 rounded-2xl flex items-center justify-center hover:bg-yellow-500 transition-all active:scale-90 shadow-lg">
                                            <Icon name="ChevronRight" size={{28}} strokeWidth={{3}} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}}
                    </div>

                    {/* Cart Modal */}
                    {{isCartOpen && (
                        <div className="fixed inset-0 z-[100] flex justify-end">
                            <div className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300" onClick={{() => setIsCartOpen(false)}} />
                            <div className="relative w-full max-w-md bg-[#050505] border-l border-yellow-500/20 shadow-2xl h-full flex flex-col p-10 animate-in slide-in-from-left duration-500">
                                <div className="flex items-center justify-between mb-10">
                                    <div className="flex items-center gap-4"><Icon name="ShoppingBag" size={{32}} className="text-yellow-500" /><h2 className="text-2xl font-black">عربة الضخ</h2></div>
                                    <button onClick={{() => setIsCartOpen(false)}} className="p-3 hover:bg-white/5 rounded-2xl transition-colors"><Icon name="X" size={{28}} /></button>
                                </div>
                                <div className="flex-1 overflow-y-auto space-y-4 custom-scroll">
                                    {{cart.length === 0 ? <div className="text-center opacity-20 mt-20 text-xl font-black">العربة فارغة</div> : 
                                      cart.map(item => (
                                        <div key={{item.id}} className="bg-white/5 p-5 rounded-[2rem] border border-white/5 flex gap-5">
                                            <img src={{item.img}} className="w-16 h-16 rounded-xl object-cover" />
                                            <div className="flex-1">
                                                <h4 className="font-black text-sm">{{item.name}}</h4>
                                                <span className="text-[#00FF88] font-black">${{item.price.toLocaleString()}}</span>
                                            </div>
                                            <button onClick={{() => setCart(cart.filter(i => i.id !== item.id))}} className="text-gray-500 hover:text-red-500 self-start p-1 transition-colors"><Icon name="X" size={{18}} /></button>
                                        </div>
                                      ))}}
                                </div>
                                {{cart.length > 0 && (
                                    <div className="mt-10 pt-10 border-t border-white/5">
                                        <div className="flex justify-between items-center mb-8"><span className="text-gray-500 font-bold text-lg text-white">إجمالي الضخ</span><span className="text-3xl font-black text-[#00FF88]">${{cart.reduce((s,i)=>s+i.price,0).toLocaleString()}}</span></div>
                                        <button className="w-full py-6 rounded-2xl font-black text-xl bg-yellow-500 text-black hover:scale-105 transition-all shadow-2xl">تأكيد العملية السيادية 🚀</button>
                                    </div>
                                )}}
                            </div>
                        </div>
                    )}}

                    <footer className="mt-20 py-12 border-t border-white/5 text-center opacity-30 text-xs font-bold uppercase tracking-[0.4em]">
                        © 2026 MR7 EMPIRE | GLOBAL SOVEREIGN COMMERCE
                    </footer>
                </div>
            );
        }};

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- 4. تشغيل المكون داخل ستريمليت (Render Bridge) ---
# هذا الأمر يقوم بحقن الـ HTML والـ React داخل الصفحة دون التسبب في SyntaxError
components.html(react_html, height=1500, scrolling=True)

# --- 5. منطق العودة (بايثون Core) ---
st.markdown("---")
if st.button("🏠 العودة لمركز القيادة الرئيسي (Python Core)"):
    st.switch_page("app.py")
