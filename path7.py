<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Path7 – Riyadh</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --cyan:#00c6ff;--navy:#0a1628;--mid:#0d3b6e;--glass:rgba(255,255,255,0.12);
  --glass2:rgba(255,255,255,0.08);--card:#fff;--shadow:0 8px 32px rgba(10,22,40,0.18);
  --radius:18px;--accent:#00c6ff;--gold:#f5c518;
}
body{min-height:100vh;background:linear-gradient(135deg,#0a1628 0%,#0d3b6e 50%,#0a2a4a 100%);font-family:'Inter',sans-serif;color:#fff;overflow-x:hidden}
body.ar{font-family:'IBM Plex Sans Arabic',sans-serif;direction:rtl}

/* BG particles */
.bg-orb{position:fixed;border-radius:50%;filter:blur(80px);opacity:.18;pointer-events:none;z-index:0}
.orb1{width:500px;height:500px;background:radial-gradient(circle,#00c6ff,transparent);top:-100px;left:-100px}
.orb2{width:400px;height:400px;background:radial-gradient(circle,#0052d4,transparent);bottom:-100px;right:-100px}
.orb3{width:300px;height:300px;background:radial-gradient(circle,#00c6ff,transparent);top:50%;left:50%;transform:translate(-50%,-50%)}

/* HEADER */
header{position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:20px 40px;backdrop-filter:blur(20px);background:rgba(255,255,255,0.06);border-bottom:1px solid rgba(255,255,255,0.1)}
.logo{display:flex;align-items:center;gap:12px}
.logo-icon{width:44px;height:44px;background:linear-gradient(135deg,#00c6ff,#0052d4);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#fff;box-shadow:0 4px 15px rgba(0,198,255,.4)}
.logo-text{font-size:24px;font-weight:700;background:linear-gradient(90deg,#00c6ff,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-right{display:flex;align-items:center;gap:16px}
.lang-btn{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:8px 18px;border-radius:50px;cursor:pointer;font-size:14px;font-weight:500;transition:.3s;backdrop-filter:blur(10px)}
.lang-btn:hover{background:rgba(0,198,255,0.2);border-color:#00c6ff}
.weather-chip{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);padding:8px 16px;border-radius:50px;font-size:13px}
.weather-icon{font-size:18px}

/* MAIN */
main{position:relative;z-index:5;max-width:1100px;margin:0 auto;padding:30px 20px 60px}

/* WELCOME */
.welcome-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,0.15);border-radius:24px;padding:40px;margin-bottom:30px;text-align:center;position:relative;overflow:hidden}
.welcome-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#00c6ff,#0052d4,#00c6ff)}
.welcome-title{font-size:clamp(22px,4vw,36px);font-weight:700;margin-bottom:8px;background:linear-gradient(90deg,#00c6ff,#fff,#00c6ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.welcome-sub{color:rgba(255,255,255,0.65);font-size:16px;margin-bottom:30px}

/* SETUP PANEL */
.setup-panel{display:flex;flex-wrap:wrap;gap:20px;justify-content:center;margin-bottom:10px}
.setup-group{display:flex;flex-direction:column;gap:8px;min-width:200px}
.setup-label{font-size:13px;font-weight:600;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:.5px}
.mode-btns{display:flex;gap:8px}
.mode-btn{flex:1;padding:12px 20px;border-radius:12px;border:1.5px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.8);cursor:pointer;font-size:14px;font-weight:500;transition:.3s;text-align:center}
.mode-btn.active{background:linear-gradient(135deg,rgba(0,198,255,.3),rgba(0,82,212,.3));border-color:#00c6ff;color:#fff;box-shadow:0 0 20px rgba(0,198,255,.2)}
.mode-btn:hover:not(.active){background:rgba(255,255,255,0.12)}
.start-btn{background:linear-gradient(135deg,#00c6ff,#0052d4);border:none;color:#fff;padding:14px 40px;border-radius(50px;font-size:16px;font-weight:600;cursor:pointer;border-radius:50px;box-shadow:0 6px 25px rgba(0,198,255,.35);transition:.3s;margin-top:10px}
.start-btn:hover{transform:translateY(-2px);box-shadow:0 10px 35px rgba(0,198,255,.45)}
.start-btn:active{transform:translateY(0)}

/* PROGRESS */
.progress-bar{display:flex;align-items:center;justify-content:center;gap:0;margin-bottom:32px}
.prog-step{display:flex;align-items:center;gap:0}
.prog-dot{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.06);color:rgba(255,255,255,.5);transition:.5s;position:relative}
.prog-dot.done{background:linear-gradient(135deg,#00c6ff,#0052d4);border-color:#00c6ff;color:#fff;box-shadow:0 0 20px rgba(0,198,255,.4)}
.prog-dot.active{background:rgba(0,198,255,.2);border-color:#00c6ff;color:#00c6ff;box-shadow:0 0 15px rgba(0,198,255,.3)}
.prog-line{width:60px;height:2px;background:rgba(255,255,255,0.15);transition:.5s}
.prog-line.done{background:linear-gradient(90deg,#00c6ff,#0052d4)}
.prog-label{font-size:11px;color:rgba(255,255,255,.5);text-align:center;margin-top:4px}
.prog-step-wrap{display:flex;flex-direction:column;align-items:center}

/* DAY CARD */
.day-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,0.15);border-radius:24px;padding:30px;margin-bottom:24px;transition:.5s}
.day-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.day-title{font-size:22px;font-weight:700;display:flex;align-items:center;gap:10px}
.day-badge{background:linear-gradient(135deg,#00c6ff,#0052d4);padding:4px 14px;border-radius:50px;font-size:13px;font-weight:600}
.budget-tag{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,.2);padding:5px 14px;border-radius:50px;font-size:12px;font-weight:500}

/* PLACES GRID */
.places-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-bottom:24px}
.place-card{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:20px;transition:.3s;position:relative;overflow:hidden}
.place-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,rgba(0,198,255,.6),transparent);opacity:0;transition:.3s}
.place-card:hover{background:rgba(255,255,255,0.1);transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,.3)}
.place-card:hover::before{opacity:1}
.place-emoji{font-size:32px;margin-bottom:10px}
.place-name{font-size:16px;font-weight:600;margin-bottom:6px;color:#fff}
.place-desc{font-size:13px;color:rgba(255,255,255,.6);line-height:1.5;margin-bottom:12px}
.place-meta{display:flex;flex-wrap:wrap;gap:6px}
.meta-chip{font-size:11px;padding:3px 10px;border-radius:50px;font-weight:500}
.chip-time{background:rgba(0,198,255,.15);color:#00c6ff;border:1px solid rgba(0,198,255,.3)}
.chip-price{background:rgba(245,197,24,.12);color:#f5c518;border:1px solid rgba(245,197,24,.3)}
.chip-metro{background:rgba(80,200,120,.12);color:#50c878;border:1px solid rgba(80,200,120,.3)}
.chip-nometro{background:rgba(255,100,100,.12);color:#ff8080;border:1px solid rgba(255,100,100,.3)}

/* TRANSPORT */
.transport-section{margin-bottom:24px}
.section-title{font-size:14px;font-weight:600;color:rgba(255,255,255,.7);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.transport-btns{display:flex;flex-wrap:wrap;gap:10px}
.transport-btn{display:flex;align-items:center;gap:8px;padding:10px 20px;border-radius:50px;border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);color:#fff;cursor:pointer;font-size:14px;font-weight:500;transition:.3s;position:relative}
.transport-btn:hover:not(:disabled){background:rgba(0,198,255,.15);border-color:#00c6ff}
.transport-btn.selected{background:rgba(0,198,255,.2);border-color:#00c6ff;color:#00c6ff}
.transport-btn:disabled{opacity:.4;cursor:not-allowed}
.tooltip{position:relative}
.tooltip .tip{display:none;position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#0a1628;border:1px solid rgba(255,255,255,.2);color:#fff;font-size:12px;padding:6px 12px;border-radius:8px;white-space:nowrap;z-index:100}
.tooltip:hover .tip{display:block}

/* RATING */
.rating-section{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:20px;margin-bottom:20px;text-align:center}
.rating-title{font-size:15px;font-weight:600;margin-bottom:14px;color:rgba(255,255,255,.9)}
.stars{display:flex;justify-content:center;gap:10px;margin-bottom:8px}
.star{font-size:32px;cursor:pointer;transition:.2s;filter:grayscale(1) opacity(.4)}
.star.active{filter:none;transform:scale(1.15)}
.star:hover{filter:none;transform:scale(1.2)}
.rating-msg{font-size:13px;color:rgba(255,255,255,.5);min-height:20px}

/* ACTION BTNS */
.action-row{display:flex;gap:12px;flex-wrap:wrap}
.btn-next{background:linear-gradient(135deg,#00c6ff,#0052d4);border:none;color:#fff;padding:13px 32px;border-radius(50px;font-size:15px;font-weight:600;cursor:pointer;border-radius:50px;box-shadow:0 6px 20px rgba(0,198,255,.3);transition:.3s}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,198,255,.45)}
.btn-next:disabled{opacity:.4;cursor:not-allowed;transform:none}
.btn-reset{background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.2);color:rgba(255,255,255,.8);padding:13px 24px;border-radius:50px;font-size:14px;font-weight:500;cursor:pointer;transition:.3s}
.btn-reset:hover{background:rgba(255,100,100,.15);border-color:rgba(255,100,100,.4);color:#ff8080}

/* SUMMARY */
.summary-card{background:rgba(255,255,255,.08);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:36px;text-align:center}
.summary-icon{font-size:60px;margin-bottom:16px}
.summary-title{font-size:28px;font-weight:700;margin-bottom:10px;background:linear-gradient(90deg,#00c6ff,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.summary-sub{color:rgba(255,255,255,.65);font-size:16px;margin-bottom:28px}
.ratings-recap{display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin-bottom:28px}
.recap-item{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:16px 24px;text-align:center}
.recap-day{font-size:12px;color:rgba(255,255,255,.5);margin-bottom:6px;font-weight:500}
.recap-stars{font-size:20px}

/* HIDDEN */
.hidden{display:none!important}
.fade-in{animation:fadeIn .5s ease forwards}
@keyframes fadeIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

@media(max-width:600px){
  header{padding:14px 18px}
  main{padding:16px 12px 50px}
  .places-grid{grid-template-columns:1fr}
  .prog-line{width:30px}
}
</style>
</head>
<body>
<div class="bg-orb orb1"></div>
<div class="bg-orb orb2"></div>
<div class="bg-orb orb3"></div>

<header>
  <div class="logo">
    <div class="logo-icon">P7</div>
    <div class="logo-text">Path7</div>
  </div>
  <div class="header-right">
    <div class="weather-chip">
      <span class="weather-icon" id="weatherIcon">☀️</span>
      <span id="weatherText">38°C · Riyadh</span>
      <span style="color:rgba(255,255,255,.4);margin-left:4px;font-size:12px" id="clockText"></span>
    </div>
    <button class="lang-btn" onclick="toggleLang()" id="langBtn">العربية</button>
  </div>
</header>

<main>
  <!-- WELCOME / SETUP -->
  <div class="welcome-card fade-in" id="setupSection">
    <div class="welcome-title" id="welcomeTitle">Welcome to Path7, Jomanah! 👋</div>
    <div class="welcome-sub" id="welcomeSub">Your smart 3-day Riyadh journey starts here. Let's personalize your experience.</div>
    <div class="setup-panel">
      <div class="setup-group">
        <div class="setup-label" id="budgetLabel">Budget Mode</div>
        <div class="mode-btns">
          <button class="mode-btn active" id="btnEconomy" onclick="setBudget('economy')">💰 <span id="econText">Economy</span></button>
          <button class="mode-btn" id="btnLuxury" onclick="setBudget('luxury')">💎 <span id="luxText">Luxury</span></button>
        </div>
      </div>
    </div>
    <button class="start-btn" onclick="startJourney()" id="startBtn">✨ Start My Journey</button>
  </div>

  <!-- PROGRESS -->
  <div id="progressSection" class="hidden fade-in" style="margin-bottom:28px">
    <div class="progress-bar">
      <div class="prog-step-wrap">
        <div class="prog-dot active" id="dot1">1</div>
        <div class="prog-label" id="pl1">Day 1</div>
      </div>
      <div class="prog-step">
        <div class="prog-line" id="line1"></div>
      </div>
      <div class="prog-step-wrap">
        <div class="prog-dot" id="dot2">2</div>
        <div class="prog-label" id="pl2">Day 2</div>
      </div>
      <div class="prog-step">
        <div class="prog-line" id="line2"></div>
      </div>
      <div class="prog-step-wrap">
        <div class="prog-dot" id="dot3">3</div>
        <div class="prog-label" id="pl3">Day 3</div>
      </div>
    </div>
  </div>

  <!-- DAY CONTENT -->
  <div id="daySection" class="hidden fade-in"></div>

  <!-- SUMMARY -->
  <div id="summarySection" class="hidden fade-in"></div>
</main>

<script>
// ── State ──────────────────────────────────────────────────────────────────
const state = {
  lang: 'en',
  budget: 'economy',
  currentDay: 0,
  ratings: {1: 0, 2: 0, 3: 0},
  transport: {1: '', 2: '', 3: ''},
  started: false
};

// ── Data ──────────────────────────────────────────────────────────────────
const DATA = {
  economy: [
    {
      day: 1,
      places: [
        {emoji:'🕌', name:{en:'Al-Masmak Fortress',ar:'قصر المصمك'}, desc:{en:'Historic mud-brick fortress at the heart of old Riyadh.',ar:'قلعة تاريخية في قلب الرياض القديمة.'}, time:'9AM–12PM', price:{en:'Free',ar:'مجاناً'}, metro:true},
        {emoji:'🛍️', name:{en:'Deira Souq',ar:'سوق ضيرة'}, desc:{en:'Vibrant traditional market with spices, textiles & antiques.',ar:'سوق شعبي نابض بالحياة يضم التوابل والمنسوجات والتحف.'}, time:'2–6PM', price:{en:'Free entry',ar:'دخول مجاني'}, metro:true},
        {emoji:'🌿', name:{en:'King Abdullah Park',ar:'حديقة الملك عبدالله'}, desc:{en:'Lush urban park with fountains, perfect for an evening stroll.',ar:'حديقة حضرية رائعة بنوافيرها المميزة.'}, time:'6–9PM', price:{en:'10 SAR',ar:'١٠ ريال'}, metro:false}
      ]
    },
    {
      day: 2,
      places: [
        {emoji:'📚', name:{en:'King Abdulaziz Public Library',ar:'مكتبة الملك عبدالعزيز العامة'}, desc:{en:'Grand library with reading halls and cultural exhibitions.',ar:'مكتبة ضخمة بقاعات قراءة ومعارض ثقافية.'}, time:'9AM–1PM', price:{en:'Free',ar:'مجاناً'}, metro:true},
        {emoji:'🦁', name:{en:'Riyadh Zoo',ar:'حديقة الحيوان بالرياض'}, desc:{en:'One of the largest zoos in the Gulf with diverse animal species.',ar:'من أكبر حدائق الحيوان في الخليج.'}, time:'2–6PM', price:{en:'15 SAR',ar:'١٥ ريال'}, metro:false},
        {emoji:'🍽️', name:{en:'Al-Nakheel Food Court',ar:'فود كورت النخيل'}, desc:{en:'Affordable local dining with authentic Saudi dishes.',ar:'طعام محلي بأسعار مناسبة وأطباق سعودية أصيلة.'}, time:'7–10PM', price:{en:'25–50 SAR',ar:'٢٥–٥٠ ريال'}, metro:true}
      ]
    },
    {
      day: 3,
      places: [
        {emoji:'🏟️', name:{en:'Diriyah Historic District',ar:'حي الدرعية التاريخي'}, desc:{en:'UNESCO-listed ancient capital with mud-brick ruins.',ar:'العاصمة القديمة المدرجة على قائمة اليونسكو.'}, time:'8AM–12PM', price:{en:'Free',ar:'مجاناً'}, metro:false},
        {emoji:'☕', name:{en:'Al-Murooj Café Row',ar:'مقاهي المروج'}, desc:{en:'Cozy local cafés for a relaxed afternoon coffee experience.',ar:'مقاهي محلية دافئة لقضاء وقت ممتع.'}, time:'2–4PM', price:{en:'15–30 SAR',ar:'١٥–٣٠ ريال'}, metro:true},
        {emoji:'🛒', name:{en:'Panorama Mall',ar:'بانوراما مول'}, desc:{en:'Budget-friendly shopping with local and regional brands.',ar:'تسوق بأسعار معقولة مع علامات تجارية محلية وإقليمية.'}, time:'5–9PM', price:{en:'Free entry',ar:'دخول مجاني'}, metro:true}
      ]
    }
  ],
  luxury: [
    {
      day: 1,
      places: [
        {emoji:'🗼', name:{en:'Kingdom Tower Observation Deck',ar:'مرصد برج المملكة'}, desc:{en:'Breathtaking 360° views of Riyadh from the iconic Sky Bridge.',ar:'إطلالات بانورامية خلابة من الجسر السماوي الشهير.'}, time:'10AM–1PM', price:{en:'87 SAR',ar:'٨٧ ريال'}, metro:true},
        {emoji:'🎨', name:{en:'Riyadh Art Gallery',ar:'غاليري الرياض للفنون'}, desc:{en:'Premier gallery showcasing contemporary Saudi fine art.',ar:'معرض رائد يعرض أعمال الفن السعودي المعاصر.'}, time:'2–5PM', price:{en:'50 SAR',ar:'٥٠ ريال'}, metro:true},
        {emoji:'🍷', name:{en:'Nobu Riyadh',ar:'مطعم نوبو الرياض'}, desc:{en:'World-class Japanese-Peruvian fusion dining experience.',ar:'تجربة طعام عالمية فاخرة باندماج ياباني–بيروفي.'}, time:'7–10PM', price:{en:'350+ SAR',ar:'٣٥٠+ ريال'}, metro:false}
      ]
    },
    {
      day: 2,
      places: [
        {emoji:'🏇', name:{en:'King Abdulaziz Racetrack',ar:'ميدان الملك عبدالعزيز'}, desc:{en:'Premium horse racing experience with VIP viewing areas.',ar:'تجربة سباق خيل فاخرة مع مناطق مشاهدة VIP.'}, time:'9AM–12PM', price:{en:'200 SAR',ar:'٢٠٠ ريال'}, metro:false},
        {emoji:'🏊', name:{en:'Four Seasons Spa & Pool',ar:'سبا وحمام فور سيزونز'}, desc:{en:'Luxurious full-day spa retreat in the heart of Riyadh.',ar:'استجمام سبا فاخر ليوم كامل في قلب الرياض.'}, time:'1–6PM', price:{en:'600 SAR',ar:'٦٠٠ ريال'}, metro:false},
        {emoji:'🌃', name:{en:'Tatel Riyadh Rooftop',ar:'مطعم تاتيل سطح المبنى'}, desc:{en:'Exclusive rooftop dining with glittering city panoramas.',ar:'عشاء حصري على السطح بإطلالات على المدينة المضيئة.'}, time:'7–11PM', price:{en:'400+ SAR',ar:'٤٠٠+ ريال'}, metro:false}
      ]
    },
    {
      day: 3,
      places: [
        {emoji:'✈️', name:{en:'Private Desert Safari',ar:'رحلة صحراوية خاصة'}, desc:{en:'VIP dune bashing and falcon show in the Riyadh desert.',ar:'تجربة صحراوية VIP مع عروض الصقور وتحدي الكثبان.'}, time:'7AM–12PM', price:{en:'1500 SAR',ar:'١٥٠٠ ريال'}, metro:false},
        {emoji:'💆', name:{en:'Boudl Al Qasr Hotel Spa',ar:'سبا بودل القصر'}, desc:{en:'Post-adventure premium relaxation and wellness session.',ar:'جلسة استرخاء وعافية فاخرة بعد المغامرة.'}, time:'2–5PM', price:{en:'500 SAR',ar:'٥٠٠ ريال'}, metro:false},
        {emoji:'🛍️', name:{en:'Avenue Mall – Luxury Wing',ar:'أفينيو مول – الجناح الفاخر'}, desc:{en:'Final shopping spree with Chanel, Dior & Rolex boutiques.',ar:'جولة تسوق نهائية في بوتيكات شانيل ودير وروليكس.'}, time:'6–10PM', price:{en:'Free entry',ar:'دخول مجاني'}, metro:true}
      ]
    }
  ]
};

const T = {
  en: {
    welcome: 'Welcome to Path7, Jomanah! 👋',
    welcomeSub: 'Your smart 3-day Riyadh journey starts here. Let\'s personalize your experience.',
    budget: 'Budget Mode', economy: 'Economy', luxury: 'Luxury',
    start: '✨ Start My Journey',
    day: 'Day', places: 'Today\'s Destinations',
    transport: 'Choose Transport', metro: '🚇 Metro', taxi: '🚕 Taxi', uber: '🚘 Uber',
    metroTip: 'Metro unavailable for these destinations',
    rateDay: 'Rate your day', rateMsg: ['Awful 😞','Poor 😐','OK 🙂','Good 😊','Amazing! 🌟'],
    next: 'Next Day →', finish: 'Complete Journey ✅', reset: 'New Journey 🔄',
    summaryTitle: 'Journey Complete! 🎉', summarySub: 'You\'ve explored the best of Riyadh, Jomanah!',
    dayLabel: ['Day 1','Day 2','Day 3'],
    weatherHot: '☀️', weatherWarm: '🌤️', weatherEvening: '🌙',
    ratingNeeded: 'Please rate your day to continue!',
    prog: ['Day 1','Day 2','Day 3']
  },
  ar: {
    welcome: 'أهلاً بكِ في Path7، جمانة! 👋',
    welcomeSub: 'رحلتكِ الذكية لـ ٣ أيام في الرياض تبدأ من هنا. لنُخصّص تجربتكِ.',
    budget: 'نوع الميزانية', economy: 'اقتصادي', luxury: 'فاخر',
    start: '✨ ابدئي رحلتي',
    day: 'اليوم', places: 'وجهات اليوم',
    transport: 'اختاري وسيلة التنقل', metro: '🚇 مترو', taxi: '🚕 تاكسي', uber: '🚘 أوبر',
    metroTip: 'المترو غير متاح لهذه الوجهات',
    rateDay: 'قيّمي يومكِ', rateMsg: ['سيء 😞','ضعيف 😐','مقبول 🙂','جيد 😊','رائع! 🌟'],
    next: 'اليوم التالي ←', finish: 'إتمام الرحلة ✅', reset: 'رحلة جديدة 🔄',
    summaryTitle: 'اكتملت الرحلة! 🎉', summarySub: 'استكشفتِ أجمل ما في الرياض، جمانة!',
    dayLabel: ['اليوم الأول','اليوم الثاني','اليوم الثالث'],
    weatherHot: '☀️', weatherWarm: '🌤️', weatherEvening: '🌙',
    ratingNeeded: 'يُرجى تقييم يومكِ للمتابعة!',
    prog: ['اليوم ١','اليوم ٢','اليوم ٣']
  }
};

// ── Clock & Weather ────────────────────────────────────────────────────────
function updateClock() {
  const now = new Date(new Date().toLocaleString('en-US',{timeZone:'Asia/Riyadh'}));
  const h = now.getHours(), m = String(now.getMinutes()).padStart(2,'0');
  const ampm = h >= 12 ? 'PM' : 'AM';
  const h12 = h % 12 || 12;
  document.getElementById('clockText').textContent = `${h12}:${m} ${ampm}`;

  let icon, temp;
  if(h >= 6 && h < 11){ icon = '🌤️'; temp = 32; }
  else if(h >= 11 && h < 16){ icon = '☀️'; temp = 42; }
  else if(h >= 16 && h < 20){ icon = '🌅'; temp = 36; }
  else { icon = '🌙'; temp = 28; }
  document.getElementById('weatherIcon').textContent = icon;
  document.getElementById('weatherText').textContent = `${temp}°C · Riyadh`;
}
setInterval(updateClock, 1000);
updateClock();

// ── Language ───────────────────────────────────────────────────────────────
function toggleLang() {
  state.lang = state.lang === 'en' ? 'ar' : 'en';
  document.body.classList.toggle('ar', state.lang === 'ar');
  document.documentElement.dir = state.lang === 'ar' ? 'rtl' : 'ltr';
  document.getElementById('langBtn').textContent = state.lang === 'en' ? 'العربية' : 'English';
  render();
}

function t(key) { return T[state.lang][key] || key; }

// ── Budget ─────────────────────────────────────────────────────────────────
function setBudget(mode) {
  state.budget = mode;
  document.getElementById('btnEconomy').classList.toggle('active', mode === 'economy');
  document.getElementById('btnLuxury').classList.toggle('active', mode === 'luxury');
}

// ── Journey Control ────────────────────────────────────────────────────────
function startJourney() {
  state.started = true;
  state.currentDay = 1;
  document.getElementById('setupSection').classList.add('hidden');
  document.getElementById('progressSection').classList.remove('hidden');
  document.getElementById('daySection').classList.remove('hidden');
  renderDay();
  updateProgress();
}

function nextDay() {
  if(!state.ratings[state.currentDay]) {
    showRatingAlert();
    return;
  }
  if(state.currentDay < 3) {
    state.currentDay++;
    updateProgress();
    renderDay();
  } else {
    showSummary();
  }
}

function resetJourney() {
  state.started = false;
  state.currentDay = 0;
  state.ratings = {1:0,2:0,3:0};
  state.transport = {1:'',2:'',3:''};
  document.getElementById('setupSection').classList.remove('hidden');
  document.getElementById('progressSection').classList.add('hidden');
  document.getElementById('daySection').classList.add('hidden');
  document.getElementById('summarySection').classList.add('hidden');
  document.getElementById('summarySection').innerHTML = '';
  render();
}

// ── Check Metro ────────────────────────────────────────────────────────────
function hasMetro(day) {
  const places = DATA[state.budget][day - 1].places;
  return places.every(p => p.metro);
}

// ── Rating ─────────────────────────────────────────────────────────────────
function setRating(day, stars) {
  state.ratings[day] = stars;
  document.querySelectorAll('.star').forEach((s, i) => {
    s.classList.toggle('active', i < stars);
  });
  const msgs = t('rateMsg');
  document.getElementById('ratingMsg').textContent = msgs[stars - 1] || '';
  document.getElementById('nextDayBtn').disabled = false;
}

function showRatingAlert() {
  const msg = document.getElementById('ratingMsg');
  msg.textContent = t('ratingNeeded');
  msg.style.color = '#ff8080';
  setTimeout(() => { msg.style.color = ''; renderRatingMsg(); }, 2000);
}

function renderRatingMsg() {
  const r = state.ratings[state.currentDay];
  const msgs = t('rateMsg');
  const el = document.getElementById('ratingMsg');
  if(el) el.textContent = r ? msgs[r-1] : '';
}

// ── Render Day ─────────────────────────────────────────────────────────────
function renderDay() {
  const d = state.currentDay;
  const dayData = DATA[state.budget][d - 1];
  const metro = hasMetro(d);
  const lang = state.lang;
  const isLast = d === 3;

  const placesHTML = dayData.places.map(p => `
    <div class="place-card">
      <div class="place-emoji">${p.emoji}</div>
      <div class="place-name">${p.name[lang]}</div>
      <div class="place-desc">${p.desc[lang]}</div>
      <div class="place-meta">
        <span class="meta-chip chip-time">🕐 ${p.time}</span>
        <span class="meta-chip chip-price">${p.price[lang]}</span>
        <span class="meta-chip ${p.metro ? 'chip-metro' : 'chip-nometro'}">${p.metro ? '🚇 Metro' : '🚫 No Metro'}</span>
      </div>
    </div>
  `).join('');

  const transports = [
    {id:'metro', label: t('metro'), disabled: !metro, tip: t('metroTip')},
    {id:'taxi',  label: t('taxi'),  disabled: false, tip: ''},
    {id:'uber',  label: t('uber'),  disabled: false, tip: ''}
  ];

  const transportHTML = transports.map(tr => `
    <div class="tooltip">
      <button class="transport-btn ${state.transport[d] === tr.id ? 'selected' : ''}" 
        ${tr.disabled ? 'disabled' : ''}
        onclick="selectTransport(${d},'${tr.id}')">
        ${tr.label}
      </button>
      ${tr.disabled ? `<div class="tip">${tr.tip}</div>` : ''}
    </div>
  `).join('');

  const currentRating = state.ratings[d];
  const starsHTML = [1,2,3,4,5].map(i => `
    <span class="star ${currentRating >= i ? 'active' : ''}" onclick="setRating(${d},${i})">⭐</span>
  `).join('');

  const dayNames = t('dayLabel');

  document.getElementById('daySection').innerHTML = `
    <div class="day-card fade-in">
      <div class="day-header">
        <div class="day-title">
          <span>${dayNames[d-1]}</span>
          <span class="day-badge">${t('day')} ${d}/3</span>
        </div>
        <span class="budget-tag">${state.budget === 'economy' ? '💰 '+t('economy') : '💎 '+t('luxury')}</span>
      </div>

      <div class="section-title">📍 ${t('places')}</div>
      <div class="places-grid">${placesHTML}</div>

      <div class="transport-section">
        <div class="section-title">🚌 ${t('transport')}</div>
        <div class="transport-btns">${transportHTML}</div>
      </div>

      <div class="rating-section">
        <div class="rating-title">⭐ ${t('rateDay')}</div>
        <div class="stars">${starsHTML}</div>
        <div class="rating-msg" id="ratingMsg">${currentRating ? t('rateMsg')[currentRating-1] : ''}</div>
      </div>

      <div class="action-row">
        <button class="btn-next" id="nextDayBtn" ${currentRating ? '' : 'disabled'} onclick="nextDay()">
          ${isLast ? t('finish') : t('next')}
        </button>
        <button class="btn-reset" onclick="resetJourney()">🔄 ${t('reset')}</button>
      </div>
    </div>
  `;
}

// ── Select Transport ───────────────────────────────────────────────────────
function selectTransport(day, mode) {
  state.transport[day] = mode;
  renderDay();
}

// ── Progress ───────────────────────────────────────────────────────────────
function updateProgress() {
  const prog = t('prog');
  [1,2,3].forEach(i => {
    const dot = document.getElementById(`dot${i}`);
    document.querySelector(`#pl${i}`) && (document.getElementById(`pl${i}`).textContent = prog[i-1]);
    dot.classList.remove('active','done');
    if(i < state.currentDay) dot.classList.add('done');
    else if(i === state.currentDay) dot.classList.add('active');
    if(i < 3) {
      const line = document.getElementById(`line${i}`);
      line.classList.toggle('done', i < state.currentDay);
    }
  });
}

// ── Summary ────────────────────────────────────────────────────────────────
function showSummary() {
  document.getElementById('daySection').classList.add('hidden');
  const sum = document.getElementById('summarySection');
  sum.classList.remove('hidden');
  const dayNames = t('dayLabel');
  const recapHTML = [1,2,3].map(d => `
    <div class="recap-item">
      <div class="recap-day">${dayNames[d-1]}</div>
      <div class="recap-stars">${'⭐'.repeat(state.ratings[d])}</div>
    </div>
  `).join('');

  sum.innerHTML = `
    <div class="summary-card fade-in">
      <div class="summary-icon">🎉</div>
      <div class="summary-title">${t('summaryTitle')}</div>
      <div class="summary-sub">${t('summarySub')}</div>
      <div class="ratings-recap">${recapHTML}</div>
      <button class="btn-reset" onclick="resetJourney()" style="font-size:15px;padding:14px 32px">🔄 ${t('reset')}</button>
    </div>
  `;
}

// ── Render (refresh text) ──────────────────────────────────────────────────
function render() {
  const lang = state.lang;
  document.getElementById('welcomeTitle').textContent = t('welcome');
  document.getElementById('welcomeSub').textContent = t('welcomeSub');
  document.getElementById('budgetLabel').textContent = t('budget');
  document.getElementById('econText').textContent = t('economy');
  document.getElementById('luxText').textContent = t('luxury');
  document.getElementById('startBtn').textContent = t('start');
  if(state.started && state.currentDay > 0 && state.currentDay <= 3) {
    updateProgress();
    renderDay();
  }
}

// Init
render();
</script>
</body>
</html>
