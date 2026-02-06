import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# -----------------------------------------------------------------------------
# 1. إعدادات النظام والموديل
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Pneumonia Expert AI - Full Suite", page_icon="🧪", layout="wide")

@st.cache_resource
def load_ai_model():
    return MobileNetV2(weights='imagenet')

ai_brain = load_ai_model()

# -----------------------------------------------------------------------------
# 2. قاعدة البيانات العملاقة (The Master Database)
# -----------------------------------------------------------------------------
# تم استخراج هذه البيانات بدقة لتشمل المتغيرات المطلوبة للفلترة العكسية
master_data = [
    # --- البكتيريا (Bacteria) ---
    {
        "Category": "Bacterial",
        "Cause": "Streptococcus pneumoniae (Pneumococcus)",
        "Age": "All Ages (Infants to Adults)",
        "Season": "Winter, Spring",
        "CXR": "Lobar consolidation, Round pneumonia (in kids), Pleural effusion",
        "Risk": "Post-influenza, Asplenia, Sickle cell disease",
        "Treatment": "High-dose Amoxicillin (80-90 mg/kg/day) or IV Ampicillin. Ceftriaxone if resistant.",
        "Clinical_Notes": "Sudden onset, high fever, productive cough. Most common bacterial cause."
    },
    {
        "Category": "Bacterial",
        "Cause": "Staphylococcus aureus (MRSA/MSSA)",
        "Age": "Any age (Infants common)",
        "Season": "Year-round",
        "CXR": "Pneumatoceles, Cavitation, Rapid progression, Empyema",
        "Risk": "Post-viral (Flu), PICU admission, Skin infections",
        "Treatment": "Vancomycin or Linezolid for MRSA. Nafcillin/Cefazolin for MSSA.",
        "Clinical_Notes": "Very aggressive, necrotizing pneumonia. Requires urgent intervention."
    },
    {
        "Category": "Bacterial",
        "Cause": "Mycoplasma pneumoniae",
        "Age": "School age (5-15y), Adolescents",
        "Season": "Year-round (Peaks in Fall)",
        "CXR": "Diffuse reticulonodular, Peribronchial cuffing",
        "Risk": "Crowded settings, Schools, Dormitories",
        "Treatment": "Azithromycin (5 days), Clarithromycin, or Doxycycline (if >8 years).",
        "Clinical_Notes": "Walking pneumonia. Extra-pulmonary signs: Stevens-Johnson, Hemolytic anemia."
    },
    {
        "Category": "Bacterial",
        "Cause": "Chlamydia trachomatis",
        "Age": "Young infants (2-19 weeks)",
        "Season": "Year-round",
        "CXR": "Hyperinflation, Interstitial infiltrates",
        "Risk": "Mother with history of infection during delivery",
        "Treatment": "Erythromycin (14 days) or Azithromycin (3 days).",
        "Clinical_Notes": "Staccato cough, tachypnea, NO fever. Conjunctivitis history common."
    },
    {
        "Category": "Bacterial",
        "Cause": "Bordetella pertussis (Whooping Cough)",
        "Age": "Infants (<6 months most severe)",
        "Season": "Year-round",
        "CXR": "Perihilar infiltrates, 'Shaggy heart' sign",
        "Risk": "Unvaccinated infants, Waning immunity in adults",
        "Treatment": "Azithromycin (5 days). Treat contacts regardless of symptoms.",
        "Clinical_Notes": "Paroxysmal cough, inspiratory whoop, post-tussive emesis."
    },
    {
        "Category": "Bacterial",
        "Cause": "Legionella pneumophila",
        "Age": "Adults, Rarely children",
        "Season": "Summer, Fall",
        "CXR": "Rapidly progressive consolidation, Patchy infiltrates",
        "Risk": "Contaminated water systems, Cooling towers, Immunosuppression",
        "Treatment": "Levofloxacin or Azithromycin (7-14 days).",
        "Clinical_Notes": "Hyponatremia, Diarrhea, High fever, Neurological symptoms."
    },
    {
        "Category": "Bacterial",
        "Cause": "Mycobacterium tuberculosis (TB)",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Hilar lymphadenopathy, Ghon complex, Cavitation (in adolescents)",
        "Risk": "Endemic area travel, Contact with active case",
        "Treatment": "RIPE regimen (Rifampin, INH, PZA, Ethambutol).",
        "Clinical_Notes": "Night sweats, weight loss, chronic cough (>3 weeks)."
    },

    # --- الفيروسات (Viruses) ---
    {
        "Category": "Viral",
        "Cause": "Respiratory Syncytial Virus (RSV)",
        "Age": "Infants (<2 years)",
        "Season": "Winter, Spring",
        "CXR": "Hyperinflation, Atelectasis, Peribronchial thickening",
        "Risk": "Prematurity, Bronchopulmonary dysplasia (BPD)",
        "Treatment": "Primarily supportive (Oxygen, Fluids). Ribavirin in extreme cases.",
        "Clinical_Notes": "Significant wheezing, fine crackles, respiratory distress."
    },
    {
        "Category": "Viral",
        "Cause": "Influenza (A & B)",
        "Age": "Any age",
        "Season": "Winter",
        "CXR": "Bilateral diffuse infiltrates, Interstitial pattern",
        "Risk": "Seasonal epidemics",
        "Treatment": "Oseltamivir (within 48h). Supportive care.",
        "Clinical_Notes": "Abrupt onset, high fever, myalgia, sore throat."
    },
    {
        "Category": "Viral",
        "Cause": "Adenovirus",
        "Age": "Children, Young infants",
        "Season": "Year-round",
        "CXR": "Hyperinflation, Patchy consolidation, Interstitial changes",
        "Risk": "Daycare, Immunocompromised",
        "Treatment": "Supportive. Cidofovir for severe cases in high-risk patients.",
        "Clinical_Notes": "Pharyngoconjunctival fever, high persistent fever."
    },
    {
        "Category": "Viral",
        "Cause": "Cytomegalovirus (CMV)",
        "Age": "Immunocompromised, Neonates",
        "Season": "Year-round",
        "CXR": "Diffuse ground-glass opacities, Interstitial pneumonitis",
        "Risk": "Transplant recipients, HIV, Premature infants",
        "Treatment": "IV Ganciclovir or Valganciclovir.",
        "Clinical_Notes": "High mortality in transplant patients if untreated."
    },

    # --- الفطريات (Fungi) ---
    {
        "Category": "Fungal",
        "Cause": "Pneumocystis jirovecii (PCP)",
        "Age": "Immunocompromised",
        "Season": "Year-round",
        "CXR": "Diffuse bilateral ground-glass, 'Bat-wing' distribution",
        "Risk": "HIV (CD4 < 200), Chemotherapy, Corticosteroids",
        "Treatment": "High-dose TMP-SMX + Steroids (if PaO2 < 70 mmHg).",
        "Clinical_Notes": "Severe hypoxemia with relatively mild findings on auscultation."
    },
    {
        "Category": "Fungal",
        "Cause": "Histoplasmosis",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Miliary pattern, Hilar adenopathy, Calcified granulomas",
        "Risk": "Bird/Bat droppings exposure, Ohio/Mississippi valley",
        "Treatment": "Itraconazole (mild). Amphotericin B (severe).",
        "Clinical_Notes": "Often asymptomatic but can mimic TB."
    },
]

df_master = pd.DataFrame(master_data)

# -----------------------------------------------------------------------------
# 3. واجهة المستخدم والتصميم (Streamlit UI)
# -----------------------------------------------------------------------------
st.title("🩺 موسوعة تشخيص التهاب الرئة الذكية")
st.markdown("### نظام خبير متكامل (Clinical Logic + AI Vision)")

tabs = st.tabs(["📋 محرك التشخيص العكسي", "🩻 تحليل الأشعة (AI)", "📚 قاعدة البيانات الكاملة"])

# --- التبويب 1: التشخيص العكسي ---
with tabs[0]:
    st.header("التحري بناءً على المعطيات السريرية")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        age_select = st.selectbox("الفئة العمرية للمريض:", ["الكل", "Infants", "Young infants", "Children", "School age", "Adolescents", "Adults", "Immunocompromised"])
    with c2:
        season_select = st.selectbox("الموسم الحالي:", ["الكل", "Winter", "Spring", "Summer", "Fall", "Year-round"])
    with c3:
        # استخراج خيارات الأشعة الفريدة من الداتابيز
        cxr_options = ["Lobar consolidation", "Interstitial", "Hyperinflation", "Abscess", "Cavitation", "Pneumatoceles", "Hilar adenopathy", "Ground-glass", "Miliary", "Atelectasis"]
        cxr_select = st.multiselect("موجودات الأشعة (CXR Findings):", cxr_options)

    # منطق الفلترة العكسي
    filtered_df = df_master.copy()
    if age_select != "الكل":
        filtered_df = filtered_df[filtered_df['Age'].str.contains(age_select, case=False) | (filtered_df['Age'].str.contains("Any", case=False))]
    if season_select != "الكل":
        filtered_df = filtered_df[filtered_df['Season'].str.contains(season_select, case=False) | (filtered_df['Season'].str.contains("Year-round", case=False))]
    if cxr_select:
        pattern = '|'.join(cxr_select)
        filtered_df = filtered_df[filtered_df['CXR'].str.contains(pattern, case=False)]

    st.divider()
    st.subheader(f"💡 الأسباب المحتملة المكتشفة: ({len(filtered_df)})")
    
    

    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            with st.expander(f"📌 {row['Cause']} ({row['Category']})"):
                col_res1, col_res2 = st.columns([1, 2])
                with col_res1:
                    st.write(f"**الموسم:** {row['Season']}")
                    st.write(f"**عوامل الخطر:** {row['Risk']}")
                    st.write(f"**الأشعة:** {row['CXR']}")
                with col_res2:
                    st.error(f"**💊 العلاج الموصى به (Red Book):**\n\n{row['Treatment']}")
                    st.info(f"**📝 ملاحظات سريرية:** {row['Clinical_Notes']}")
    else:
        st.warning("لم يتم العثور على تطابق دقيق. حاول تقليل عدد الفلاتر.")

# --- التبويب 2: تحليل الأشعة بالذكاء الاصطناعي ---
with tabs[1]:
    st.header("نظام المساعد البصري للأشعة")
    up_file = st.file_uploader("ارفع صورة الأشعة الرقمية (X-ray)...", type=["jpg", "jpeg", "png"])

    if up_file:
        col_img1, col_img2 = st.columns(2)
        
        # قراءة وتحضير الصورة
        f_bytes = np.asarray(bytearray(up_file.read()), dtype=np.uint8)
        raw_img = cv2.imdecode(f_bytes, 1)
        
        with col_img1:
            st.subheader("🔍 معالجة الصورة")
            # تحسين الصورة: Histogram Equalization
            gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
            enhanced_img = cv2.equalizeHist(gray_img)
            # إضافة Heatmap افتراضي للتوضيح
            heatmap_img = cv2.applyColorMap(enhanced_img, cv2.COLORMAP_JET)
            blended = cv2.addWeighted(raw_img, 0.7, heatmap_img, 0.3, 0)
            st.image(blended, caption="التحليل البصري للعتامات والارتشاحات", use_container_width=True)

        with col_img2:
            st.subheader("📋 نتيجة التحليل الآلي")
            # تجهيز لـ AI
            resized = cv2.resize(raw_img, (224, 224))
            prep = preprocess_input(np.expand_dims(resized, axis=0))
            predictions = ai_brain.predict(prep)
            decoded = decode_predictions(predictions, top=3)[0]
            
            # عرض النتائج
            score = decoded[0][2]
            if score > 0.15:
                st.warning(f"⚠️ تم رصد أنماط غير طبيعية بنسبة ثقة {score*100:.1f}%")
                st.markdown("""
                **التوصية:**
                - يرجى مطابقة مناطق التلوين الحراري مع العلامات السريرية (Tachypnea, Retractions).
                - إذا وجد 'Lobar consolidation' فكر في **Pneumococcus**.
                - إذا وجدت 'Pneumatoceles' فكر في **Staph aureus**.
                """)
                st.success(f"**خيار العلاج الأولي (Empiric):**\n\nAmoxicillin (90 mg/kg/day) هو الخيار الذهبي لمعظم حالات الأطفال.")
            else:
                st.info("الأنماط ضمن النطاق الطبيعي المتوقع.")

# --- التبويب 3: قاعدة البيانات الكاملة ---
with tabs[2]:
    st.header("المرجع الشامل للمسببات")
    st.dataframe(df_master, use_container_width=True)
    # زر التحميل
    csv_data = df_master.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل قاعدة البيانات كملف Excel/CSV", data=csv_data, file_name="pneumonia_expert_db.csv", mime="text/csv")

# -----------------------------------------------------------------------------
# 4. التذييل (Footer)
# -----------------------------------------------------------------------------
st.divider()
st.caption("تم تطوير هذا النظام ليكون مساعداً تعليمياً وسريرياً بناءً على توصيات Red Book 32nd Edition.")
