import streamlit as st
import json
import os

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="Pneumonia Etiology Guide",
    page_icon="🫁",
    layout="wide"
)

# --- دالة تحميل البيانات ---
@st.cache_data
def load_data():
    # تأكد من أن ملف pneumonia.json موجود في نفس المجلد
    file_path = 'pneumonia.json'
    if not os.path.exists(file_path):
        st.error("ملف البيانات (pneumonia.json) غير موجود! يرجى وضعه في نفس مجلد الكود.")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            st.error("هناك خطأ في تنسيق ملف JSON.")
            return []

data = load_data()

# --- الشريط الجانبي (Filters) ---
st.sidebar.title("🔍 أدوات التشخيص (Filters)")
st.sidebar.markdown("---")

# 1. فلتر البحث العام
search_query = st.sidebar.text_input("بحث سريع (Keywords)", placeholder="مثال: Birds, HIV, fever...")

# 2. فلتر العمر (Age Group)
# بما أن البيانات نصية، سنقوم بربط الاختيار بكلمات مفتاحية للبحث
age_mapping = {
    "الكل (All)": [],
    "حديثي الولادة (Neonates < 1m)": ["neonate", "birth", "0-28", "vertical", "early-onset"],
    "الرضع (Infants 1m-1y)": ["infant", "young children", "weeks", "months"],
    "الأطفال (Children)": ["child", "school", "5 and 15", "years"],
    "البالغين/الكبار (Adults/Elderly)": ["adult", "elderly", "65"]
}
selected_age_group = st.sidebar.selectbox("الفئة العمرية (Age Group)", list(age_mapping.keys()))

# 3. فلتر علامات الأشعة (CXR Findings)
cxr_keywords = [
    "Consolidation", "Lobar", "Patchy", "Interstitial", 
    "Ground glass", "Effusion", "Abscess", "Cavity", 
    "Hyperinflation", "Nodular", "Mass"
]
selected_cxr = st.sidebar.multiselect("علامات صورة الصدر (CXR Findings)", cxr_keywords)

# 4. فلتر عوامل الخطر (Risk Factors)
risk_keywords = [
    "Immunocompromised", "HIV", "Cystic Fibrosis", "Asthma", 
    "Sickle Cell", "Aspiration", "Birds", "Animals"
]
selected_risks = st.sidebar.multiselect("عوامل الخطر (Risk Factors)", risk_keywords)

# --- منطق الفلترة (Filtering Logic) ---
filtered_data = []

for entry in data:
    match = True
    
    # دمج كل النصوص في المدخل للبحث العام
    all_text = " ".join([str(v) for v in entry.values() if v]).lower()
    
    # 1. تطبيق البحث العام
    if search_query and search_query.lower() not in all_text:
        match = False
    
    # 2. تطبيق فلتر العمر
    if match and selected_age_group != "الكل (All)":
        age_text = str(entry.get('best_age', '') or '').lower()
        # التحقق مما إذا كانت أي من الكلمات المفتاحية للفئة العمرية موجودة
        age_keywords = age_mapping[selected_age_group]
        if not any(k in age_text or k in str(entry.get('CLINICAL MANIFESTATIONS', '')).lower() for k in age_keywords):
            match = False

    # 3. تطبيق فلتر CXR
    if match and selected_cxr:
        cxr_text = str(entry.get('cxr_findings', '') or '').lower()
        # يجب أن يحتوي النص على *واحد على الأقل* من الخيارات المحددة
        if not any(k.lower() in cxr_text for k in selected_cxr):
            match = False
            
    # 4. تطبيق فلتر عوامل الخطر
    if match and selected_risks:
        risk_text = str(entry.get('risk_factors', '') or '').lower()
        if not any(k.lower() in risk_text for k in selected_risks):
            match = False

    if match:
        filtered_data.append(entry)

# --- الواجهة الرئيسية ---
st.title("🫁 دليل مسببات ذات الرئة (Pneumonia Etiology)")
st.markdown(f"**عدد النتائج المطابقة:** {len(filtered_data)}")

if len(filtered_data) == 0:
    st.warning("لا توجد نتائج تطابق الفلاتر الحالية. حاول تخفيف شروط البحث.")
else:
    for item in filtered_data:
        # تحديد اللون بناءً على نوع المسبب (اختياري لتحسين الشكل)
        cause_name = item.get('pneumonia_cause', 'Unknown')
        
        with st.expander(f"🦠 {cause_name}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📋 Clinical Manifestations")
                st.write(item.get('CLINICAL MANIFESTATIONS') or "Non specific")
                
                st.markdown("### 💊 Treatment")
                # دمج حقول العلاج إذا وجدت
                tx = item.get('treatment_pneumonia') or item.get('treatment')
                st.info(tx or "Supportive / Refer to guidelines")

            with col2:
                # عرض البيانات الوصفية في جدول صغير
                st.markdown("### 🔍 Key Features")
                
                if item.get('cxr_findings'):
                    st.markdown(f"**🩻 CXR:** {item.get('cxr_findings')}")
                
                if item.get('risk_factors'):
                    st.markdown(f"**⚠️ Risk Factors:** {item.get('risk_factors')}")
                
                if item.get('best_age'):
                    st.markdown(f"**👶 Age:** {item.get('best_age')}")
                
                if item.get('diagnosis'):
                    st.markdown(f"**🧪 Diagnosis:** {item.get('diagnosis')}")

                if item.get('regions'):
                    st.markdown(f"**🌍 Region:** {item.get('regions')}")

# --- تذييل الصفحة ---
st.markdown("---")
st.caption("Developed for Clinical Decision Support. Based on Red Book Data.")
