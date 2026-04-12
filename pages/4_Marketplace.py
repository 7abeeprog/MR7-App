import React, { useState, useEffect, useMemo } from 'react';
import { 
  ShoppingBag, 
  Search, 
  MapPin, 
  TrendingUp, 
  ShieldCheck, 
  Star, 
  Wallet, 
  X, 
  ChevronRight, 
  Package,
  CheckCircle2,
  AlertCircle,
  LayoutGrid,
  Store,
  Globe,
  Filter
} from 'lucide-react';
import { initializeApp } from 'firebase/app';
import { 
  getFirestore, 
  collection, 
  onSnapshot, 
  addDoc,
  query 
} from 'firebase/firestore';
import { 
  getAuth, 
  signInAnonymously, 
  signInWithCustomToken, 
  onAuthStateChanged 
} from 'firebase/auth';

// --- إعدادات الإمبراطورية ---
const firebaseConfig = JSON.parse(window.__firebase_config || '{}');
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof window.__app_id !== 'undefined' ? window.__app_id : 'mr7-empire-v1';

// --- القوائم العالمية ---
const CATEGORIES = ["الكل", "عقارات سيادية", "أكاديمية القيادة", "تقنيات المستقبل", "طاقة مستدامة", "استشارات تريليونية", "أصول رقمية"];

const COUNTRIES = [
  "الكل", "مصر", "ليبيا", "السودان", "السعودية", "الإمارات", "قطر", "الكويت", "سلطنة عمان", "البحرين", 
  "الأردن", "لبنان", "سوريا", "العراق", "فلسطين", "المغرب", "تونس", "الجزائر", "موريتانيا", "اليمن", 
  "تركيا", "الولايات المتحدة", "الصين", "ألمانيا", "بريطانيا", "فرنسا", "اليابان", "كندا", "أستراليا", "البرازيل"
  // يمكن إضافة باقي الدول برمجياً هنا
];

const App = () => {
  const [user, setUser] = useState(null);
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('الكل');
  const [selectedCategory, setSelectedCategory] = useState('الكل');
  const [balance, setBalance] = useState(1250000);
  const [purchaseStatus, setPurchaseStatus] = useState(null);

  // 1. المصادقة
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof window.__initial_auth_token !== 'undefined' && window.__initial_auth_token) {
          await signInWithCustomToken(auth, window.__initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) { console.error(err); }
    };
    initAuth();
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  // 2. جلب البيانات (Multi-Vendor & Multi-Category Logic)
  useEffect(() => {
    if (!user) return;
    const q = collection(db, 'artifacts', appId, 'public', 'data', 'marketplace_products');
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const prods = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      if (prods.length === 0) {
        // بيانات تجريبية بنظام الأقسام والتجار الجدد
        setProducts([
          { id: 'p1', name: 'برج السيادة الإداري', price: 1500000, country: 'مصر', category: 'عقارات سيادية', vendor: 'مجموعة النبت العقارية', rating: 5.0, sales: 12, img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500' },
          { id: 'p2', name: 'منظومة الطاقة الشمسية X10', price: 12500, country: 'ليبيا', category: 'طاقة مستدامة', vendor: 'تكنو-صحراء', rating: 4.8, sales: 85, img: 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?w=500' },
          { id: 'p3', name: 'دبلوم هندسة الأرباح', price: 499, country: 'السعودية', category: 'أكاديمية القيادة', vendor: 'أكاديمية MR7', rating: 4.9, sales: 1240, img: 'https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=500' },
          { id: 'p4', name: 'وكيل الذكاء الاصطناعي الخاص', price: 2500, country: 'عالمي', category: 'تقنيات المستقبل', vendor: 'سيادة-تك', rating: 5.0, sales: 320, img: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500' },
        ]);
      } else {
        setProducts(prods);
      }
    });
    return () => unsubscribe();
  }, [user]);

  // 3. فلترة متقدمة (Country + Category + Search)
  const filteredProducts = useMemo(() => {
    return products.filter(p => {
      const matchSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || p.vendor.toLowerCase().includes(searchTerm.toLowerCase());
      const matchCountry = selectedCountry === 'الكل' || p.country === selectedCountry;
      const matchCategory = selectedCategory === 'الكل' || p.category === selectedCategory;
      return matchSearch && matchCountry && matchCategory;
    });
  }, [products, searchTerm, selectedCountry, selectedCategory]);

  const addToCart = (product) => {
    if (!cart.find(i => i.id === product.id)) {
      setCart([...cart, product]);
      setIsCartOpen(true);
    }
  };

  const handleCheckout = async () => {
    const total = cart.reduce((s, i) => s + i.price, 0);
    if (balance < total) { setPurchaseStatus('error'); return; }
    
    setBalance(prev => prev - total);
    if (user) {
      await addDoc(collection(db, 'artifacts', appId, 'users', user.uid, 'transactions'), {
        type: 'global_purchase',
        amount: total,
        items: cart.map(i => i.name),
        timestamp: new Date().toISOString()
      });
    }
    setPurchaseStatus('success');
    setCart([]);
    setTimeout(() => { setPurchaseStatus(null); setIsCartOpen(false); }, 2000);
  };

  return (
    <div dir="rtl" className="min-h-screen bg-[#020202] text-white font-['Tajawal',sans-serif]">
      {/* --- الهيدر العالمي --- */}
      <nav className="sticky top-0 z-50 bg-black/90 backdrop-blur-2xl border-b border-yellow-500/10 px-6 py-4 shadow-2xl">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-4 min-w-max">
            <div className="bg-yellow-500 text-black p-2.5 rounded-2xl shadow-[0_0_20px_rgba(234,179,8,0.4)]">
              <Store size={28} strokeWidth={2.5} />
            </div>
            <div className="hidden lg:block">
              <h1 className="text-2xl font-black tracking-tighter text-yellow-500">MR7 GLOBAL</h1>
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-[0.2em]">Empire Marketplace</p>
            </div>
          </div>

          <div className="flex-1 max-w-2xl relative">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
            <input 
              type="text" 
              placeholder="ابحث عن منتج، قسم، أو تاجر سيادي..."
              className="w-full bg-[#111] border border-gray-800 rounded-2xl py-3.5 pr-12 pl-4 focus:border-yellow-500/50 outline-none transition-all font-bold text-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="flex items-center gap-4 sm:gap-8">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-[10px] text-gray-500 font-bold">الخزنة السيادية</span>
              <div className="flex items-center gap-2 text-[#00FF88] font-black text-xl">
                <Wallet size={18} />
                <span>${balance.toLocaleString()}</span>
              </div>
            </div>
            <button onClick={() => setIsCartOpen(true)} className="relative p-3 bg-white/5 hover:bg-white/10 rounded-2xl transition-all group">
              <ShoppingBag size={28} className="group-hover:text-yellow-500 transition-colors" />
              {cart.length > 0 && (
                <span className="absolute -top-1 -left-1 bg-yellow-500 text-black text-[11px] font-black w-6 h-6 flex items-center justify-center rounded-full border-4 border-[#020202]">
                  {cart.length}
                </span>
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* --- شريط الأقسام (Categories Bar) --- */}
      <div className="bg-[#080808] border-b border-gray-900 py-3 sticky top-[89px] z-40">
        <div className="max-w-[1600px] mx-auto px-6 flex items-center gap-3 overflow-x-auto no-scrollbar">
          <LayoutGrid size={20} className="text-yellow-500 ml-2" />
          {CATEGORIES.map(cat => (
            <button 
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-5 py-2 rounded-xl text-sm font-black whitespace-nowrap transition-all border ${
                selectedCategory === cat 
                ? 'bg-yellow-500/10 border-yellow-500 text-yellow-500' 
                : 'bg-transparent border-transparent text-gray-500 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <main className="max-w-[1600px] mx-auto px-6 py-10">
        {/* --- فلتر الدول المتقدم (Country Selector) --- */}
        <div className="mb-10 flex flex-wrap items-center gap-4 bg-[#0a0a0a] p-4 rounded-3xl border border-gray-900">
          <div className="flex items-center gap-2 text-gray-400 font-bold text-sm px-2">
            <Globe size={18} className="text-yellow-500" />
            تصفية حسب الدولة:
          </div>
          <div className="flex gap-2 overflow-x-auto no-scrollbar">
            {COUNTRIES.map(country => (
              <button 
                key={country}
                onClick={() => setSelectedCountry(country)}
                className={`px-4 py-2 rounded-xl text-xs font-black transition-all ${
                  selectedCountry === country 
                  ? 'bg-white text-black' 
                  : 'bg-[#111] text-gray-500 hover:bg-[#1a1a1a]'
                }`}
              >
                {country}
              </button>
            ))}
          </div>
        </div>

        {/* --- شبكة المنتجات العالمية --- */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-8">
          {filteredProducts.map(product => (
            <div 
              key={product.id}
              className="group bg-[#0a0a0a] border border-gray-900 rounded-[2.5rem] overflow-hidden hover:border-yellow-500/40 transition-all duration-500 shadow-xl"
            >
              <div className="relative h-64 overflow-hidden">
                <img src={product.img} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-xl flex items-center gap-2 border border-white/10">
                  <MapPin size={14} className="text-yellow-500" />
                  <span className="text-[11px] font-black">{product.country}</span>
                </div>
                <div className="absolute bottom-4 left-4 bg-yellow-500 text-black px-4 py-1.5 rounded-xl text-[11px] font-black shadow-lg">
                  {product.category}
                </div>
              </div>

              <div className="p-8">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-1.5 bg-yellow-500/10 text-yellow-500 px-2 py-1 rounded-lg">
                    <Star size={14} fill="currentColor" />
                    <span className="text-xs font-black">{product.rating}</span>
                  </div>
                  <div className="flex items-center gap-1 text-[11px] text-gray-500 font-bold uppercase">
                    <TrendingUp size={12} className="text-[#00FF88]" />
                    {product.sales} مبيعة
                  </div>
                </div>
                
                <h3 className="text-xl font-black mb-2 line-clamp-1 group-hover:text-yellow-500 transition-colors">{product.name}</h3>
                <div className="flex items-center gap-2 mb-6">
                  <div className="w-6 h-6 rounded-full bg-gray-800 flex items-center justify-center text-[10px]">🏢</div>
                  <span className="text-xs text-gray-400 font-medium">التاجر: <b className="text-gray-200">{product.vendor}</b></span>
                </div>
                
                <div className="flex items-center justify-between border-t border-gray-900 pt-6">
                  <div className="flex flex-col">
                    <span className="text-[10px] text-gray-500 font-bold uppercase mb-1">قيمة الأصل</span>
                    <span className="text-2xl font-black text-[#00FF88]">${product.price.toLocaleString()}</span>
                  </div>
                  <button 
                    onClick={() => addToCart(product)}
                    className="bg-white text-black h-14 w-14 rounded-2xl flex items-center justify-center hover:bg-yellow-500 transition-all shadow-lg active:scale-95"
                  >
                    <ChevronRight size={28} strokeWidth={3} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* --- سلة المشتريات المدمجة --- */}
      {isCartOpen && (
        <div className="fixed inset-0 z-[100] flex justify-end">
          <div className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300" onClick={() => setIsCartOpen(false)} />
          <div className="relative w-full max-w-md bg-[#050505] border-r border-yellow-500/20 shadow-2xl h-full flex flex-col p-10 animate-in slide-in-from-left duration-500">
            <div className="flex items-center justify-between mb-10">
              <div className="flex items-center gap-4">
                <ShoppingBag size={32} className="text-yellow-500" />
                <h2 className="text-2xl font-black">عربة الضخ</h2>
              </div>
              <button onClick={() => setIsCartOpen(false)} className="p-3 hover:bg-white/5 rounded-2xl transition-colors">
                <X size={28} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-6 no-scrollbar">
              {cart.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center opacity-20">
                  <Package size={80} className="mb-6 text-yellow-500" />
                  <p className="font-black text-xl">لا توجد أصول في العربة</p>
                </div>
              ) : (
                cart.map(item => (
                  <div key={item.id} className="bg-[#0a0a0a] p-5 rounded-[2rem] border border-gray-900 flex gap-5 group">
                    <img src={item.img} className="w-20 h-20 rounded-2xl object-cover" />
                    <div className="flex-1">
                      <h4 className="font-black text-sm mb-1">{item.name}</h4>
                      <p className="text-[10px] text-yellow-500 font-bold mb-2">📍 {item.country}</p>
                      <span className="text-[#00FF88] font-black text-lg">${item.price.toLocaleString()}</span>
                    </div>
                    <button onClick={() => setCart(cart.filter(i => i.id !== item.id))} className="text-gray-700 hover:text-red-500 self-start p-1 transition-colors">
                      <X size={20} />
                    </button>
                  </div>
                ))
              )}
            </div>

            {cart.length > 0 && (
              <div className="mt-10 pt-10 border-t border-gray-900">
                <div className="flex justify-between items-center mb-8">
                  <span className="text-gray-500 font-bold text-lg">الإجمالي الكلي</span>
                  <span className="text-4xl font-black text-[#00FF88]">${cart.reduce((s,i)=>s+i.price,0).toLocaleString()}</span>
                </div>
                
                <button 
                  onClick={handleCheckout}
                  disabled={purchaseStatus === 'success'}
                  className={`w-full py-6 rounded-2xl font-black text-xl transition-all shadow-2xl flex items-center justify-center gap-4 ${
                    purchaseStatus === 'success' ? 'bg-[#00FF88] text-black' : 
                    purchaseStatus === 'error' ? 'bg-red-600 text-white' : 
                    'bg-yellow-500 text-black hover:scale-[1.02]'
                  }`}
                >
                  {purchaseStatus === 'success' ? <><CheckCircle2 size={28} /> تم الضخ بنجاح</> : 
                   purchaseStatus === 'error' ? <><AlertCircle size={28} /> رصيد غير كافٍ</> : 
                   <>تأكيد العملية السيادية 🚀</>}
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      <footer className="mt-20 border-t border-gray-900 p-12 text-center bg-[#010101]">
        <div className="flex items-center justify-center gap-12 mb-8 opacity-20 hover:opacity-50 transition-opacity">
          <ShieldCheck size={40} /> <Globe size={40} /> <Store size={40} />
        </div>
        <p className="text-gray-600 text-sm font-bold tracking-widest uppercase">© 2026 MR7 EMPIRE - Global Sovereign Commerce</p>
      </footer>
    </div>
  );
};

export default App;
