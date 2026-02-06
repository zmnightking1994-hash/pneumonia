import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# -----------------------------------------------------------------------------
# 1. إعدادات النظام وتحميل الذكاء الاصطناعي
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Pneumonia Expert System Pro", page_icon="🧬", layout="wide")

@st.cache_resource
def load_ai_model():
    return MobileNetV2(weights='imagenet')

ai_brain = load_ai_model()

# -----------------------------------------------------------------------------
# 2. قاعدة البيانات العملاقة (Master Database) - مستخرجة من Red Book
# -----------------------------------------------------------------------------
master_db = [
    # --- البكتيريا النمطية وغير النمطية ---
    {"Cause": "Streptococcus pneumoniae", "Type": "Bacterial", "Age": "All ages", "Season": "Winter/Spring", "CXR": "Lobar consolidation, Round pneumonia", "Risk": "Most common bacterial cause", "Treatment": "High-dose Amoxicillin (90 mg/kg) or IV Ceftriaxone."},
    {"Cause": "Mycoplasma pneumoniae", "Type": "Atypical", "Age": "School age/Adolescents", "Season": "Year-round", "CXR": "Reticulonodular, Peribronchial cuffing", "Risk": "Walking pneumonia", "Treatment": "Azithromycin or Doxycycline (if >8 years)."},
    {"Cause": "Staphylococcus aureus (MRSA)", "Type": "Bacterial", "Age": "Any age", "Season": "Year-round", "CXR": "Pneumatoceles, Abscess, Empyema", "Risk": "Post-influenza, Rapidly ill", "Treatment": "Vancomycin or Linezolid."},
    {"Cause": "Chlamydia trachomatis", "Type": "Bacterial", "Age": "Infants (2-19 weeks)", "Season": "Year-round", "CXR": "Hyperinflation, Interstitial", "Risk": "Birth canal exposure", "Treatment": "Erythromycin (14 days) or Azithromycin (3 days)."},
    {"Cause": "Bordetella pertussis", "Type": "Bacterial", "Age": "Infants", "Season": "Year-round", "CXR": "Shaggy heart border", "Risk": "Unvaccinated", "Treatment": "Azithromycin (5 days)."},
    {"Cause": "Haemophilus influenzae type b", "Type": "Bacterial", "Age": "<5 years", "Season": "Year-round", "CXR": "Lobar consolidation", "Risk": "Unvaccinated", "Treatment": "Ceftriaxone or Cefotaxime."},
    {"Cause": "Legionella pneumophila", "Type": "Bacterial", "Age": "Adults/Immunocompromised", "Season": "Summer/Fall", "CXR": "Patchy or Lobar consolidation", "Risk": "Water systems, Air con", "Treatment": "Azithromycin or Levofloxacin."},
    {"Cause": "Mycobacterium tuberculosis", "Type": "Bacterial", "Age": "Any age", "Season": "Year-round", "CXR": "Hilar adenopathy, Ghon complex", "Risk": "Endemic travel", "Treatment": "RIPE (INH, RIF, PZA, EMB)."},
    {"Cause": "Pseudomonas aeruginosa", "Type": "Bacterial", "Age": "Any age", "Season": "Year-round", "CXR": "Necrotizing infiltrates", "Risk": "Cystic Fibrosis, Tracheostomy", "Treatment": "Cefepime or Piperacillin-Tazobactam + Tobramycin."},
    
    # --- الفيروسات ---
    {"Cause": "RSV", "Type": "Viral", "Age": "Infants (<2 years)", "Season": "Winter", "CXR": "Hyperinflation, Atelectasis", "Risk": "Prematurity", "Treatment": "Supportive (Oxygen/Fluids)."},
    {"Cause": "Influenza A & B", "Type": "Viral", "Age": "Any age", "Season": "Winter", "CXR": "Bilateral diffuse infiltrates", "Risk": "Seasonal epidemics", "Treatment": "Oseltamivir (within 48h)."},
    {"Cause": "Adenovirus", "Type": "Viral", "Age": "Young children", "Season": "Year-round", "CXR": "Patchy infiltrates, Pleural effusion", "Risk": "Daycare", "Treatment": "Supportive. Cidofovir in severe cases."},
    {"Cause": "Cytomegalovirus (CMV)", "Type": "Viral", "Age": "Immunocompromised", "Season": "Year-round", "CXR": "Ground-glass opacities", "Risk": "Transplant/HIV", "Treatment": "Ganciclovir or Valganciclovir."},
    {"Cause": "Human Metapneumovirus", "Type": "Viral", "Age": "Children", "Season": "Winter/Spring", "CXR": "Peribronchial thickening", "Risk": "Asthma exacerbation", "Treatment": "Supportive."},
    {"Cause": "SARS-CoV-2", "Type": "Viral", "Age": "Any age", "Season": "Year-round", "CXR": "Peripheral ground-glass", "Risk": "Pandemic", "Treatment": "Supportive, Remdesivir/Dexamethasone if severe."},

    # --- الفطريات وغيرها ---
    {"Cause": "Pneumocystis jirovecii (PCP)", "Type": "Fungal", "Age": "Immunocompromised", "Season": "Year-round", "CXR": "Bilateral ground-glass", "Risk": "HIV/AIDS", "Treatment": "High-dose TMP-SMX + Steroids."},
    {"Cause": "Histoplasmosis", "Type": "Fungal", "Age": "Any age", "Season": "Year-round", "CXR": "Miliary, Hilar adenopathy", "Risk": "Bird/Bat droppings", "Treatment": "Itraconazole or Amphotericin B."},
    {"Cause": "Cryptococcosis", "Type": "Fungal", "Age": "Immunocompromised", "Season": "Year-round", "CXR": "Nodular or masses", "Risk": "Pigeon droppings", "Treatment": "Amphotericin B + Flucytosine."},
]

df = pd.DataFrame(master_db)

# -----------------------------------------------------------------------------
# 3. واجهة التطبيق
# -----------------------------------------------------------------------------
st.title("🫁 تطبيق خبير التهاب الرئة الشامل (Red Book 2024)")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 محرك التشخيص السريري", "📸 تحليل الأشعة (AI)", "📚 الموسوعة الكاملة"])

# --- Tab 1: Clinical Assistant ---
with tab1:
    st.subheader("تحليل الحالة بناءً على المعطيات")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_filter = st.selectbox("العمر:", ["الكل"] + sorted(list(set(df['Age']))))
    with col2:
        season_filter = st.selectbox("الموسم:", ["الكل", "Winter", "Spring", "Summer", "Fall", "Year-round"])
    with col3:
        cxr_filter = st.multiselect("الموجودات في الأشعة:", ["Lobar consolidation", "Interstitial", "Hyperinflation", "Abscess", "Pneumatoceles", "Ground-glass", "Hilar adenopathy"])

    # منطق البحث العكسي
    filtered = df.copy()
    if age_filter != "الكل": filtered = filtered[filtered['Age'].str.contains(age_filter, case=False)]
    if season_filter != "الكل": filtered = filtered[filtered['Season'].str.contains(season_filter, case=False) | (filtered['Season'] == "Year-round")]
    if cxr_filter:
        pattern = '|'.join(cxr_filter)
        filtered = filtered[filtered['CXR'].str.contains(pattern, case=False)]

    st.write(f"### النتائج المحتملة: ({len(filtered)})")
    for _, row in filtered.iterrows():
        with st.expander(f"📍 {row['Cause']}"):
            st.warning(f"💊 **بروتوكول العلاج:** {row['Treatment']}")
            st.info(f"🔍 **عوامل الخطر:** {row['Risk']}")
            st.write(f"🩻 **الأشعة:** {row['CXR']}")

# --- Tab 2: AI Analysis (The code you provided) ---
with tab2:
    st.subheader("تحليل صورة الأشعة بالذكاء الاصطناعي")
    uploaded_file = st.file_uploader("ارفع صورة الأشعة...", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        c_img, c_res = st.columns(2)
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        with c_img:
            # معالجة متقدمة: Equalization + Heatmap
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(gray)
            heatmap = cv2.applyColorMap(equ, cv2.COLORMAP_JET)
            blended = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
            st.image(blended, caption="التحليل البصري للعتامات", use_container_width=True)

        with c_res:
            # AI Inference
            img_resized = cv2.resize(img, (224, 224))
            x = preprocess_input(np.expand_dims(img_resized, axis=0))
            preds = ai_brain.predict(x)
            results = decode_predictions(preds, top=3)[0]
            
            st.write(f"**النمط المكتشف:** {results[0][1]} (الثقة: {results[0][2]*100:.1f}%)")
            st.success("**💊 القاعدة العامة للعلاج (Empiric Therapy):**\n\nAmoxicillin هو الخيار الأول للأطفال غير الملقحين أو الحالات النموذجية.")

# --- Tab 3: Full Encyclopedia ---
with tab3:
    st.subheader("قاعدة بيانات المسببات الكاملة")
    st.dataframe(df, use_container_width=True)
    # خيار التحميل
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل البيانات كاملة (Excel/CSV)", data=csv, file_name="RedBook_Full_Database.csv")

st.sidebar.markdown("""
### حول التطبيق:
هذا النظام يدمج بين **رؤية الحاسوب** و **قواعد البيانات السريرية**.
تم استخراج البيانات من:
- **AAP Red Book 32nd Edition**
- **Nelson Textbook of Pediatrics**
""")
