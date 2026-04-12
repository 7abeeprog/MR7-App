import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Merchant Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. جلب إعدادات السحابة والنمط ---
fb_config_str = st.secrets.get("__firebase_config", "{}")
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
current_theme = st.session_state.get('app_theme', "أسود قيادي 🖤")
current_balance = st.session_state.get('cash_balance', 1250000)

# --- 3. واجهة React للوحة التاجر (نظام العمولات المتعدد وتحديث الهوية اللفظية) ---
react_html = r"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <!-- السيرفرات السحابية الأسرع والأكثر استقراراً (JSDelivr) -->
    <script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.23.5/babel.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lucide@0.292.0/dist/umd/lucide.min.js"></script>
    
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
        ::-webkit-scrollbar-thumb:hover { background: #888; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        .glass-panel { 
            backdrop-filter: blur(24px); 
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            transition: all 0.5s;
        }

        .premium-input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            color: white;
        }
        .premium-input:focus {
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
            outline: none;
            background: rgba(255, 255, 255, 0.05);
        }

        .btn-hover-dynamic { transition: all 0.3s ease; }
        .btn-hover-dynamic:hover {
            transform: scale(1.03);
            filter: brightness(1.1);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .animate-view { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        @keyframes toastEnter {
            0% { opacity: 0; transform: translateY(100%) scale(0.9); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .toast-animate { animation: toastEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }

        html[dir="ltr"] .dir-invert { flex-direction: row-reverse; }
        html[dir="ltr"] .text-dir { text-align: left; }
        html[dir="rtl"] .text-dir { text-align: right; }

        #loading-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            background: #000; color: #FFD700; display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 99999;
            font-family: 'Tajawal', sans-serif;
            transition: opacity 0.5s ease;
        }
        .loader-spinner {
            border: 4px solid rgba(255,215,0,0.3); border-top: 4px solid #FFD700;
            border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .sparkline { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: drawLine 2s ease-out forwards; }
        @keyframes drawLine { to { stroke-dashoffset: 0; } }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div class="loader-spinner"></div>
        <h2 style="margin:0;">جاري تهيئة مركز العمليات الاستراتيجي...</h2>
        <p style="color:#888; font-size:14px; margin-top:10px;">MR7 Ecosystem Initialization</p>
    </div>

    <div id="root"></div>

    <script>
        window.onerror = function(msg, url, line, col, error) {
            var loader = document.getElementById('loading-screen');
            if (loader) loader.style.display = 'none';
            document.body.innerHTML += `
                <div style="padding:40px; background:#220000; color:#FF5555; text-align:left; direction:ltr; position:absolute; top:0; width:100%; min-height:100vh; z-index:999999;">
                    <h2 style="font-family:sans-serif;">⚠️ نظام الحماية: تم رصد خطأ تقني</h2>
                    <p style="font-size:1.2rem;">${msg}</p>
                </div>
            `;
        };
    </script>

    <script type="text/babel">
        const { useState, useEffect, useCallback, useRef, useMemo } = React;

        class ErrorBoundary extends React.Component {
            constructor(props) { super(props); this.state = { hasError: false, errorInfo: null }; }
            static getDerivedStateFromError(error) { return { hasError: true }; }
            componentDidCatch(error, errorInfo) {
                this.setState({ errorInfo: error.toString() + "\n" + errorInfo.componentStack });
                const loader = document.getElementById('loading-screen');
                if (loader) loader.style.display = 'none';
            }
            render() {
                if (this.state.hasError) return <div style={{padding: '30px', background: '#330000', color: 'white', direction: 'ltr', borderRadius: '20px', margin: '20px'}}><h2>React UI Crash</h2><pre style={{whiteSpace: 'pre-wrap', fontSize: '12px'}}>{this.state.errorInfo}</pre></div>;
                return this.props.children;
            }
        }

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

        const Sparkline = ({ color }) => (
            <svg width="100%" height="40" viewBox="0 0 200 40" preserveAspectRatio="none" className="mt-4">
                <path d="M0,40 L20,30 L40,35 L60,20 L80,25 L100,10 L120,15 L140,5 L160,10 L180,0 L200,5" fill="none" stroke={color} strokeWidth="3" className="sparkline" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M0,40 L20,30 L40,35 L60,20 L80,25 L100,10 L120,15 L140,5 L160,10 L180,0 L200,5 L200,40 L0,40 Z" fill={`${color}33`} stroke="none"/>
            </svg>
        );

        // قاموس الترجمة الشامل (بمصطلحات ريادية واحترافية)
        const translations = {
            ar: {
                dashboardTitle: "لوحة التاجر", dashboardSub: "Elite Merchant Hub", searchPlaceholder: "البحث عن الأصول الريادية...",
                liquidity: "المحفظة الاستثمارية", overview: "نظرة عامة", assets: "إدارة الأصول", team: "شركاء النجاح", services: "الخدمات الذكية",
                affiliate: "نظام الشراكات والعمولات", certified: "رائد أعمال معتمد", gen: "الجيل المتقدم", kpiTitle: "مؤشرات الأداء 📊", sales: "إجمالي المبيعات",
                activeAssets: "الأصول النشطة", views: "المشاهدات", teamMembers: "شركاء الشبكة", newProduct: "طرح أصل جديد", addAsset: "اعتماد الأصل",
                inventory: "مخزون الأصول", edit: "تعديل", delete: "حذف", active: "نشط", inactive: "مخفي", targetProgress: "نسبة الهدف", bonus: "مكافأة",
                affTitle: "هندسة العمولات والمكتبة التسويقية 🔗", affSub1: "نظام العمولات متعدد المستويات", affSub2: "المكتبة التسويقية (Assets Vault)",
                uploadAd: "إضافة مادة إعلانية", saveRate: "تحديث النظام المالي", successAdded: "تم رفع الأصل للمراجعة بنجاح! 🚀"
            },
            en: {
                dashboardTitle: "Merchant Hub", dashboardSub: "Elite Merchant Hub", searchPlaceholder: "Search Elite Assets...",
                liquidity: "Investment Wallet", overview: "Overview", assets: "Asset Mgmt", team: "Success Partners", services: "Smart Services",
                affiliate: "Partnerships & Commissions", certified: "Certified Entrepreneur", gen: "Advanced Gen", kpiTitle: "Performance KPIs 📊", sales: "Total Sales",
                activeAssets: "Active Assets", views: "Total Views", teamMembers: "Network Partners", newProduct: "List New Asset", addAsset: "Submit Asset",
                inventory: "Inventory", edit: "Edit", delete: "Delete", active: "Active", inactive: "Hidden", targetProgress: "Target Progress", bonus: "Bonus",
                affTitle: "Commission Engineering & Marketing Vault 🔗", affSub1: "Multi-Level Commission Settings", affSub2: "Marketing Assets Vault",
                uploadAd: "Upload Creative", saveRate: "Update Financial Engine", successAdded: "Asset successfully submitted for review! 🚀"
            },
            fr: {
                dashboardTitle: "Hub Marchand", dashboardSub: "Hub Marchand d'Élite", searchPlaceholder: "Rechercher des Actifs...",
                liquidity: "Portefeuille d'Investissement", overview: "Aperçu", assets: "Gestion des Actifs", team: "Partenaires de Succès", services: "Services Intelligents",
                affiliate: "Partenariats et Commissions", certified: "Entrepreneur Certifié", gen: "Génération Avancée", kpiTitle: "KPI de Performance 📊", sales: "Ventes Totales",
                activeAssets: "Actifs Actifs", views: "Vues Totales", teamMembers: "Partenaires du Réseau", newProduct: "Lister Nouvel Actif", addAsset: "Soumettre pour Examen",
                inventory: "Inventaire", edit: "Modifier", delete: "Supprimer", active: "Actif", inactive: "Masqué", targetProgress: "Progression Cible", bonus: "Bonus",
                affTitle: "Ingénierie des Commissions 🔗", affSub1: "Paramètres de Commission Multi-Niveaux", affSub2: "Coffre de Ressources Marketing",
                uploadAd: "Télécharger une Création", saveRate: "Mettre à jour le Moteur Financier", successAdded: "Actif soumis avec succès ! 🚀"
            },
            es: {
                dashboardTitle: "Centro Comercial", dashboardSub: "Centro Comercial de Élite", searchPlaceholder: "Buscar Activos...",
                liquidity: "Billetera de Inversión", overview: "Visión General", assets: "Gestión de Activos", team: "Socios de Éxito", services: "Servicios Inteligentes",
                affiliate: "Asociaciones y Comisiones", certified: "Emprendedor Certificado", gen: "Generación Avanzada", kpiTitle: "KPI de Rendimiento 📊", sales: "Ventas Totales",
                activeAssets: "Activos Activos", views: "Vistas Totales", teamMembers: "Socios de Red", newProduct: "Listar Nuevo Activo", addAsset: "Enviar para Revisión",
                inventory: "Inventario", edit: "Editar", delete: "Eliminar", active: "Activo", inactive: "Oculto", targetProgress: "Progreso Objetivo", bonus: "Bono",
                affTitle: "Ingeniería de Comisiones 🔗", affSub1: "Configuración de Comisiones Multinivel", affSub2: "Bóveda de Recursos de Marketing",
                uploadAd: "Subir Creatividad", saveRate: "Actualizar Motor Financiero", successAdded: "¡Activo enviado con éxito! 🚀"
            },
            zh: {
                dashboardTitle: "商家中心", dashboardSub: "精英商家中心", searchPlaceholder: "搜索优质资产...",
                liquidity: "投资钱包", overview: "概览", assets: "资产与库存管理", team: "成功合作伙伴", services: "智能辅助服务",
                affiliate: "合伙与佣金系统", certified: "认证企业家", gen: "高级一代", kpiTitle: "绩效指标 📊", sales: "总销售额",
                activeAssets: "活跃资产", views: "总浏览量", teamMembers: "网络合伙人", newProduct: "发布新资产", addAsset: "提交审核",
                inventory: "库存", edit: "编辑", delete: "删除", active: "活跃", inactive: "隐藏", targetProgress: "目标进度", bonus: "奖金",
                affTitle: "佣金工程与营销资源库 🔗", affSub1: "多级佣金设置", affSub2: "营销资源库",
                uploadAd: "上传广告素材", saveRate: "更新财务引擎", successAdded: "资产已成功提交审核！ 🚀"
            },
            fa: {
                dashboardTitle: "داشبورد تاجر", dashboardSub: "مرکز تجارت نخبگان", searchPlaceholder: "جستجوی دارایی‌های برتر...",
                liquidity: "کیف پول سرمایه‌گذاری", overview: "نمای کلی", assets: "مدیریت دارایی", team: "شرکای موفقیت", services: "خدمات هوشمند",
                affiliate: "سیستم مشارکت و پورسانت", certified: "کارآفرین تایید شده", gen: "نسل پیشرفته", kpiTitle: "شاخص‌های عملکرد 📊", sales: "کل فروش",
                activeAssets: "دارایی‌های فعال", views: "کل بازدیدها", teamMembers: "شرکای شبکه", newProduct: "عرضه دارایی جدید", addAsset: "تایید و ارسال",
                inventory: "موجودی", edit: "ویرایش", delete: "حذف", active: "فعال", inactive: "پنهان", targetProgress: "پیشرفت هدف", bonus: "پاداش",
                affTitle: "مهندسی پورسانت و کتابخانه بازاریابی 🔗", affSub1: "تنظیمات پورسانت چند سطحی", affSub2: "کتابخانه بازاریابی",
                uploadAd: "بارگذاری محتوای تبلیغاتی", saveRate: "بروزرسانی سیستم مالی", successAdded: "دارایی با موفقیت برای بررسی ارسال شد! 🚀"
            },
            sw: {
                dashboardTitle: "Kituo cha Mfanyabiashara", dashboardSub: "Kituo cha Biashara cha Wasomi", searchPlaceholder: "Tafuta Mali za Wasomi...",
                liquidity: "Mkoba wa Uwekezaji", overview: "Muhtasari", assets: "Usimamizi wa Mali", team: "Washirika wa Mafanikio", services: "Huduma za Kisasa",
                affiliate: "Ushirikiano na Kamisheni", certified: "Mjasiriamali Aliyeidhinishwa", gen: "Kizazi cha Juu", kpiTitle: "Viashiria vya Utendaji 📊", sales: "Mauzo ya Jumla",
                activeAssets: "Mali Zinazofanya Kazi", views: "Mionekano ya Jumla", teamMembers: "Washirika wa Mtandao", newProduct: "Zindua Mali Mpya", addAsset: "Wasilisha kwa Ukaguzi",
                inventory: "Orodha", edit: "Hariri", delete: "Futa", active: "Inayofanya Kazi", inactive: "Iliyofichwa", targetProgress: "Maendeleo ya Lengo", bonus: "Bonasi",
                affTitle: "Uhandisi wa Kamisheni 🔗", affSub1: "Mipangilio ya Kamisheni ya Ngazi Nyingi", affSub2: "Maktaba ya Masoko",
                uploadAd: "Pakia Tangazo", saveRate: "Sasisha Mfumo wa Kifedha", successAdded: "Mali imewasilishwa kwa ukaguzi kikamilifu! 🚀"
            }
        };

        const App = () => {
            useEffect(() => {
                const loader = document.getElementById('loading-screen');
                if (loader) { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 500); }
            }, []);

            const themes = {
                "فاتح ملكي ✨": { bg: "bg-[#F5F5F5]", text: "text-[#1A1A1A]", card: "bg-white/90", border: "border-[#B8860B]", borderLight: "border-[#B8860B]/20", accent: "text-[#B8860B]", btn: "bg-[#B8860B]", btnText: "text-white", hex: "#FFFFFF" },
                "أسود قيادي 🖤": { bg: "bg-[#030303]", text: "text-white", card: "bg-[rgba(15,15,15,0.8)]", border: "border-[#FFD700]", borderLight: "border-[#FFD700]/20", accent: "text-[#FFD700]", btn: "bg-[#FFD700]", btnText: "text-black", hex: "#000000" },
                "أزرق القيادة 💙": { bg: "bg-[#000814]", text: "text-white", card: "bg-[#00122B]/80", border: "border-[#0074D9]", borderLight: "border-[#0074D9]/20", accent: "text-[#0074D9]", btn: "bg-[#0074D9]", btnText: "text-white", hex: "#0074D9" },
                "أخضر الاستدامة 💚": { bg: "bg-[#00140A]", text: "text-white", card: "bg-[#002B1B]/80", border: "border-[#00FF88]", borderLight: "border-[#00FF88]/20", accent: "text-[#00FF88]", btn: "bg-[#00FF88]", btnText: "text-black", hex: "#00FF88" },
                "أحمر القوة 🔴": { bg: "bg-[#140000]", text: "text-white", card: "bg-[#2B0000]/80", border: "border-[#FF4136]", borderLight: "border-[#FF4136]/20", accent: "text-[#FF4136]", btn: "bg-[#FF4136]", btnText: "text-white", hex: "#FF4136" },
                "أصفر الريادة 🟡": { bg: "bg-[#141400]", text: "text-white", card: "bg-[#2B2B00]/80", border: "border-[#FFDC00]", borderLight: "border-[#FFDC00]/20", accent: "text-[#FFDC00]", btn: "bg-[#FFDC00]", btnText: "text-black", hex: "#FFDC00" },
                "روز الفخامة 🌸": { bg: "bg-[#14000A]", text: "text-white", card: "bg-[#2B0015]/80", border: "border-[#F012BE]", borderLight: "border-[#F012BE]/20", accent: "text-[#F012BE]", btn: "bg-[#F012BE]", btnText: "text-white", hex: "#F012BE" }
            };
            
            const [activeThemeName, setActiveThemeName] = useState("CURRENT_THEME_PLACEHOLDER" || "أسود قيادي 🖤");
            const activeTheme = themes[activeThemeName] || themes["أسود قيادي 🖤"];
            const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);

            const [lang, setLang] = useState('ar');
            const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
            const t = translations[lang] || translations['ar'];

            useEffect(() => { document.documentElement.dir = (lang === 'ar' || lang === 'fa') ? 'rtl' : 'ltr'; }, [lang]);

            // --- States ---
            const [activeTab, setActiveTab] = useState('overview'); 
            const [productSubTab, setProductSubTab] = useState('inventory');
            const [toasts, setToasts] = useState([]);
            
            const [products, setProducts] = useState([
                { id: 'p1', name: 'أكاديمية الريادة المتقدمة', price: 1500000, category: 'عقارات نخبوية', sales: 12, views: 1500, status: 'نشط', commRate: 10 },
                { id: 'p2', name: 'دبلوم هندسة الأرباح', price: 499, category: 'تعليم', sales: 1240, views: 5600, status: 'مخفي', commRate: 15 }
            ]);
            
            const [team, setTeam] = useState([
                { id: 1, name: 'أحمد المصري', role: 'مدير المبيعات', sales: 124000, target: 150000, status: 'نشط 🟢' },
                { id: 2, name: 'سارة خالد', role: 'استشاري استثمار', sales: 45000, target: 50000, status: 'نشط 🟢' }
            ]);

            // Affiliate State (Multi-Level)
            const [commRates, setCommRates] = useState({ l1: 10, l2: 5, l3: 2 });
            const [marketingAssets, setMarketingAssets] = useState([
                { id: 1, title: 'فيديو ترويجي للمنصة (TikTok)', type: 'Video', views: 4500, url: '#' },
                { id: 2, title: 'تصميم جرافيك للحملات', type: 'Image', views: 1200, url: '#' }
            ]);

            const [newProd, setNewProd] = useState({ name: '', price: '', category: 'عقارات نخبوية', desc: '' });

            const showToast = useCallback((msg, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, msg, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            }, []);

            // Functions
            const handleAddProduct = (e) => {
                e.preventDefault();
                if(!newProd.name || !newProd.price) { showToast('يرجى استكمال البيانات', 'warning'); return; }
                const p_price = parseFloat(newProd.price);
                setProducts([{...newProd, price: p_price, id: Date.now().toString(), sales: 0, views: 0, status: 'نشط', commRate: commRates.l1}, ...products]);
                setNewProd({ name: '', price: '', category: 'عقارات نخبوية', desc: '' });
                showToast(t.successAdded);
                setProductSubTab('inventory');
            };

            const ToastContainer = () => (
                <div className="fixed bottom-8 right-8 z-[999] flex flex-col gap-3 pointer-events-none">
                    {toasts.map(toast => (
                        <div key={toast.id} className={`toast-animate flex items-center gap-3 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl border ${toast.type === 'success' ? 'bg-black/90 border-[#00FF88]/40 text-[#00FF88]' : `bg-black/90 ${activeTheme.borderLight} ${activeTheme.accent}`}`}>
                            <Icon name={toast.type === 'success' ? 'CheckCircle2' : 'AlertCircle'} size={20} />
                            <span className="font-bold text-sm text-white text-dir">{toast.msg}</span>
                        </div>
                    ))}
                </div>
            );

            const isRTL = lang === 'ar' || lang === 'fa';
            const themeHex = activeTheme.hex;

            return (
                <div className={`min-h-screen ${activeTheme.bg} ${activeTheme.text} flex flex-col md:flex-row overflow-hidden transition-colors duration-500`}>
                    
                    {/* --- Sidebar --- */}
                    <div className={`w-full md:w-72 md:min-h-screen ${activeTheme.card} border-b md:border-b-0 md:border-l ${activeTheme.borderLight} flex flex-col transition-colors duration-500 z-10 shadow-[0_0_30px_rgba(0,0,0,0.5)]`}>
                        
                        <div className="p-6 pb-2 flex justify-between items-center dir-invert">
                            <div className="relative z-[200]">
                                <button onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)} className={`w-10 h-10 rounded-full border-2 border-white/20 shadow-lg hover:scale-110 transition-transform`} style={{backgroundColor: themeHex}} title="تغيير النمط"></button>
                                {isThemeMenuOpen && (
                                    <div className={`absolute top-12 ${isRTL ? 'right-0' : 'left-0'} glass-panel p-2 rounded-2xl flex flex-col gap-2 shadow-2xl animate-view`}>
                                        {Object.entries(themes).map(([key, theme]) => (
                                            <button key={key} onClick={() => { setActiveThemeName(key); setIsThemeMenuOpen(false); }} title={key} className={`w-8 h-8 rounded-full border-2 transition-all ${activeThemeName === key ? 'border-white scale-110' : 'border-transparent hover:scale-110 opacity-70 hover:opacity-100'}`} style={{ backgroundColor: theme.hex }} />
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div className="relative z-[200]">
                                <button onClick={() => setIsLangMenuOpen(!isLangMenuOpen)} className={`flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border ${activeTheme.borderLight} hover:bg-white/10 transition-all font-bold text-sm`}>
                                    <Icon name="Globe" size={16} className={activeTheme.accent} /> {lang.toUpperCase()}
                                </button>
                                {isLangMenuOpen && (
                                    <div className={`absolute top-10 ${isRTL ? 'left-0' : 'right-0'} glass-panel p-2 rounded-xl flex flex-col gap-1 shadow-2xl animate-view min-w-[100px]`}>
                                        {['ar', 'en', 'fr', 'es', 'zh', 'fa', 'sw'].map(l => (
                                            <button key={l} onClick={() => {setLang(l); setIsLangMenuOpen(false);}} className={`px-4 py-2 rounded-lg text-sm font-bold text-dir hover:bg-white/10 ${lang === l ? activeTheme.accent : 'text-white'}`}>{l.toUpperCase()}</button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="px-8 pb-6 pt-4 text-dir">
                            <div className={`${activeTheme.btn} ${activeTheme.btnText} p-3.5 rounded-2xl inline-block mb-4 shadow-lg`}>
                                <Icon name="Briefcase" size={30} />
                            </div>
                            <h1 className={`text-2xl font-black uppercase tracking-widest ${activeTheme.accent} mb-1`}>{t.dashboardTitle}</h1>
                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{t.dashboardSub}</p>
                        </div>

                        <div className="flex flex-row md:flex-col gap-3 p-4 md:p-6 overflow-x-auto no-scrollbar md:flex-1">
                            {[
                                {id: 'overview', icon: 'LayoutDashboard', label: t.overview},
                                {id: 'products', icon: 'Package', label: t.assets},
                                {id: 'affiliate', icon: 'Share2', label: t.affiliate},
                                {id: 'team', icon: 'Users', label: t.team},
                                {id: 'services', icon: 'Zap', label: t.services}
                            ].map(tab => (
                                <button 
                                    key={tab.id} onClick={() => setActiveTab(tab.id)} 
                                    className={`flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all text-dir whitespace-nowrap ${activeTab === tab.id ? `bg-white/10 ${isRTL?'border-r-4':'border-l-4'} ${activeTheme.border} ${activeTheme.accent} shadow-md` : 'text-gray-400 hover:bg-white/5 hover:text-white'}`}
                                >
                                    <Icon name={tab.icon} size={20} /> {tab.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* --- Main Content Area --- */}
                    <div className="flex-1 p-4 md:p-10 h-screen overflow-y-auto no-scrollbar text-dir relative">
                        
                        {/* Top Bar */}
                        <div className="flex flex-col md:flex-row gap-6 mb-10 items-center">
                            <div className="flex-1 relative w-full">
                                <Icon name="Search" size={18} className={`absolute ${isRTL?'right-5':'left-5'} top-1/2 -translate-y-1/2 text-gray-400`} />
                                <input type="text" placeholder={t.searchPlaceholder} className={`w-full premium-input rounded-2xl py-4 ${isRTL?'pr-14 pl-6':'pl-14 pr-6'} text-sm font-bold text-dir shadow-sm`} />
                            </div>
                            <div className={`glass-panel px-8 py-3 rounded-2xl border ${activeTheme.borderLight} flex items-center gap-4 hover:border-white/20 transition-colors`}>
                                <div className="flex flex-col">
                                    <span className="text-[10px] text-gray-500 font-black uppercase tracking-widest">{t.liquidity}</span>
                                    <span className="text-[#00FF88] font-black text-xl">${Number(LEADER_BALANCE_PLACEHOLDER).toLocaleString()}</span>
                                </div>
                                <div className={`p-2 rounded-xl bg-white/5 ${activeTheme.accent}`}><Icon name="Wallet" size={24} /></div>
                            </div>
                        </div>

                        {/* --- Tab: Overview --- */}
                        {activeTab === 'overview' && (
                            <div className="animate-view space-y-8 max-w-[1600px] mx-auto">
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors shadow-lg`}>
                                        <p className="text-gray-400 font-bold mb-1 text-xs uppercase tracking-widest">{t.sales}</p>
                                        <h4 className="text-3xl font-black text-[#00FF88]">$1,036,000</h4>
                                        <Sparkline color="#00FF88" />
                                        <div className={`absolute ${isRTL?'-left-4':'-right-4'} -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="TrendingUp" size={120} /></div>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors shadow-lg`}>
                                        <p className="text-gray-400 font-bold mb-1 text-xs uppercase tracking-widest">{t.activeAssets}</p>
                                        <h4 className="text-3xl font-black text-white">{products.length}</h4>
                                        <Sparkline color={themeHex} />
                                        <div className={`absolute ${isRTL?'-left-4':'-right-4'} -top-4 opacity-5 text-white group-hover:scale-110 transition-transform`}><Icon name="Package" size={120} /></div>
                                    </div>
                                    <div className={`${activeTheme.card} p-6 rounded-[2rem] border ${activeTheme.borderLight} relative overflow-hidden group transition-colors shadow-lg`}>
                                        <p className="text-gray-400 font-bold mb-1 text-xs uppercase tracking-widest">{t.teamMembers}</p>
                                        <h4 className="text-3xl font-black text-white">450</h4>
                                        <Sparkline color="#0074D9" />
                                        <div className={`absolute ${isRTL?'-left-4':'-right-4'} -top-4 opacity-5 ${activeTheme.accent} group-hover:scale-110 transition-transform`}><Icon name="Share2" size={120} /></div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* --- Tab: Affiliate & Marketing (Multi-Level) --- */}
                        {activeTab === 'affiliate' && (
                            <div className="animate-view space-y-8 max-w-[1600px] mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="Share2" className={activeTheme.accent} size={32} /> {t.affTitle}
                                </h2>
                                
                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                    {/* 1. إعدادات العمولات متعددة المستويات */}
                                    <div className={`lg:col-span-1 ${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} shadow-xl`}>
                                        <h3 className="text-xl font-black mb-6">{t.affSub1}</h3>
                                        <div className="space-y-5">
                                            <div>
                                                <label className="text-[10px] font-black text-gray-400 uppercase block mb-2">عمولة المستوى الأول (%)</label>
                                                <div className="flex items-center gap-4">
                                                    <input type="range" min="1" max="50" value={commRates.l1} onChange={(e) => setCommRates({...commRates, l1: e.target.value})} className="flex-1 accent-yellow-500" />
                                                    <span className={`text-xl font-black ${activeTheme.accent}`}>{commRates.l1}%</span>
                                                </div>
                                            </div>
                                            <div>
                                                <label className="text-[10px] font-black text-gray-400 uppercase block mb-2">عمولة المستوى الثاني (%)</label>
                                                <div className="flex items-center gap-4">
                                                    <input type="range" min="0" max="30" value={commRates.l2} onChange={(e) => setCommRates({...commRates, l2: e.target.value})} className="flex-1 accent-yellow-500" />
                                                    <span className={`text-xl font-black ${activeTheme.accent}`}>{commRates.l2}%</span>
                                                </div>
                                            </div>
                                            <div>
                                                <label className="text-[10px] font-black text-gray-400 uppercase block mb-2">عمولة المستوى الثالث (%)</label>
                                                <div className="flex items-center gap-4">
                                                    <input type="range" min="0" max="15" value={commRates.l3} onChange={(e) => setCommRates({...commRates, l3: e.target.value})} className="flex-1 accent-yellow-500" />
                                                    <span className={`text-xl font-black ${activeTheme.accent}`}>{commRates.l3}%</span>
                                                </div>
                                            </div>
                                            <button onClick={()=>showToast('تم تحديث نظام العمولات بنجاح')} className={`w-full py-4 mt-2 rounded-xl font-black text-lg ${activeTheme.btn} ${activeTheme.btnText} btn-hover-dynamic`}>
                                                {t.saveRate}
                                            </button>
                                        </div>
                                    </div>

                                    {/* 2. تخصيص عمولات المنتجات */}
                                    <div className={`lg:col-span-2 ${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} shadow-xl overflow-x-auto no-scrollbar`}>
                                        <h3 className="text-xl font-black mb-6">تخصيص عمولات الأصول الفردية</h3>
                                        <table className="w-full text-dir border-collapse">
                                            <thead>
                                                <tr className="text-gray-400 text-xs uppercase tracking-widest border-b border-white/10">
                                                    <th className="pb-4 font-black text-right pl-4">اسم الأصل</th>
                                                    <th className="pb-4 font-black">القيمة</th>
                                                    <th className="pb-4 font-black text-center">عمولة الشراكة (م1)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {products.map(p => (
                                                    <tr key={p.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                        <td className="py-4 font-bold">{p.name}</td>
                                                        <td className="py-4 font-black text-[#00FF88]">${Number(p.price).toLocaleString()}</td>
                                                        <td className="py-4 text-center">
                                                            <div className="flex items-center justify-center gap-2">
                                                                <input type="number" defaultValue={p.commRate || commRates.l1} className="premium-input w-20 text-center rounded-lg py-1 font-bold text-sm" /> %
                                                            </div>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>

                                    {/* 3. المكتبة التسويقية */}
                                    <div className={`lg:col-span-3 ${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} shadow-xl mt-4`}>
                                        <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
                                            <h3 className="text-xl font-black">{t.affSub2}</h3>
                                            <button onClick={()=>showToast('سيتم تفعيل رفع المواد الإعلانية قريباً', 'warning')} className={`px-5 py-2 rounded-xl font-bold text-sm bg-white/10 hover:bg-white/20 transition-all flex items-center gap-2`}>
                                                <Icon name="Upload" size={16} /> {t.uploadAd}
                                            </button>
                                        </div>
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                            {marketingAssets.map(asset => (
                                                <div key={asset.id} className="bg-black/50 border border-white/10 p-5 rounded-2xl group hover:border-[#00FF88] transition-all">
                                                    <div className="h-32 bg-white/5 rounded-xl mb-4 flex items-center justify-center border border-white/5 group-hover:bg-[#00FF88]/5">
                                                        <Icon name={asset.type === 'Video' ? 'Video' : 'Image'} size={40} className="text-gray-500 group-hover:text-[#00FF88] transition-colors" />
                                                    </div>
                                                    <h4 className="font-bold text-sm mb-2">{asset.title}</h4>
                                                    <div className="flex justify-between items-center text-xs text-gray-400">
                                                        <span className="bg-white/10 px-2 py-1 rounded-md">{asset.type}</span>
                                                        <span><Icon name="Eye" size={12} className="inline mr-1"/> {asset.views}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* --- Tab: Products --- */}
                        {activeTab === 'products' && (
                            <div className="animate-view space-y-6 max-w-[1600px] mx-auto">
                                <div className="flex gap-4 border-b border-white/10 pb-4">
                                    <button onClick={()=>setProductSubTab('inventory')} className={`pb-2 px-2 font-black text-lg transition-colors ${productSubTab==='inventory'?`border-b-2 ${activeTheme.border} ${activeTheme.accent}`:'text-gray-500 hover:text-white'}`}>{t.inventory}</button>
                                    <button onClick={()=>setProductSubTab('add')} className={`pb-2 px-2 font-black text-lg transition-colors ${productSubTab==='add'?`border-b-2 ${activeTheme.border} ${activeTheme.accent}`:'text-gray-500 hover:text-white'}`}>{t.newProduct}</button>
                                </div>

                                {productSubTab === 'inventory' && (
                                    <div className={`${activeTheme.card} p-6 md:p-8 rounded-[2.5rem] border ${activeTheme.borderLight} shadow-xl animate-fade-in`}>
                                        <div className="overflow-x-auto">
                                            <table className="w-full text-dir border-collapse">
                                                <thead>
                                                    <tr className="text-gray-400 text-xs uppercase tracking-widest border-b border-white/10">
                                                        <th className="pb-4 font-black text-right pl-4">اسم الأصل</th>
                                                        <th className="pb-4 font-black">القيمة</th>
                                                        <th className="pb-4 font-black text-center">الحالة</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {products.map(p => (
                                                        <tr key={p.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                            <td className="py-5 font-bold flex items-center gap-3">
                                                                <div className="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center text-lg">🏢</div>
                                                                <div>
                                                                    <div className="text-sm">{p.name}</div>
                                                                    <div className="text-[10px] text-gray-500">{p.category}</div>
                                                                </div>
                                                            </td>
                                                            <td className="py-5 font-black text-[#00FF88]">${Number(p.price).toLocaleString()}</td>
                                                            <td className="py-5 text-center">
                                                                <span className={`px-3 py-1 rounded-lg text-xs font-black ${p.status === 'نشط' ? 'bg-[#00FF88]/20 text-[#00FF88] border border-[#00FF88]/30 hover:bg-[#00FF88]/40' : 'bg-gray-800 text-gray-400 border border-gray-600 hover:bg-gray-700'}`}>
                                                                    {p.status}
                                                                </span>
                                                            </td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                )}

                                {productSubTab === 'add' && (
                                    <form onSubmit={handleAddProduct} className={`${activeTheme.card} p-8 md:p-10 rounded-[3rem] border ${activeTheme.borderLight} shadow-2xl transition-colors animate-fade-in max-w-4xl mx-auto`}>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                                            <div className="space-y-3">
                                                <input type="text" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border} text-dir`} value={newProd.name} onChange={e => setNewProd({...newProd, name: e.target.value})} placeholder={lang === 'ar' || lang === 'fa' ? 'اسم الأصل...' : 'Asset Name...'} required />
                                            </div>
                                            <div className="space-y-3">
                                                <input type="number" className={`w-full premium-input rounded-2xl py-4 px-5 font-bold focus:${activeTheme.border} text-dir`} value={newProd.price} onChange={e => setNewProd({...newProd, price: e.target.value})} placeholder={lang === 'ar' || lang === 'fa' ? 'السعر ($)' : 'Price ($)'} required />
                                            </div>
                                        </div>
                                        <button type="submit" className={`w-full py-6 rounded-[2rem] font-black text-xl ${activeTheme.btn} ${activeTheme.btnText} btn-hover-dynamic flex items-center justify-center gap-3 shadow-[0_10px_30px_rgba(0,0,0,0.3)]`}>
                                            <Icon name="UploadCloud" /> {t.addAsset}
                                        </button>
                                    </form>
                                )}
                            </div>
                        )}

                        {/* --- Tab: Team --- */}
                        {activeTab === 'team' && (
                            <div className="animate-view space-y-8 max-w-6xl mx-auto">
                                <h2 className="text-3xl font-black mb-8 border-b border-white/10 pb-6 flex items-center gap-4">
                                    <Icon name="Users" className={activeTheme.accent} size={32} /> {t.teamMembers}
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {team.map(member => (
                                        <div key={member.id} className={`${activeTheme.card} p-8 rounded-[2.5rem] border ${activeTheme.borderLight} relative overflow-hidden transition-colors`}>
                                            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mb-4 text-2xl">👤</div>
                                            <h4 className="text-xl font-black mb-1">{member.name}</h4>
                                            <p className={`text-sm font-bold mb-6 ${activeTheme.accent}`}>{member.role}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                    </div>
                    <ToastContainer />
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ErrorBoundary><App /></ErrorBoundary>);
    </script>
</body>
</html>
"""

# --- 4. حقن المتغيرات (آمن بدون Syntax Error) ---
final_html = react_html.replace("CURRENT_THEME_PLACEHOLDER", current_theme)
final_html = final_html.replace("LEADER_BALANCE_PLACEHOLDER", str(current_balance))

# --- 5. تشغيل واجهة React ---
components.html(final_html, height=1050, scrolling=True)

# --- 6. أزرار التحكم والرجوع ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🛒 العودة للمتجر (Marketplace)"):
        st.switch_page("pages/4_Marketplace.py")
with c2:
    if st.button("🏠 العودة للرئيسية"):
        st.switch_page("app.py")
