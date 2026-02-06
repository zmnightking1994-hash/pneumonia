import streamlit as st
import pandas as pd
import io

# إعدادات الصفحة
st.set_page_config(page_title="Pediatric Pneumonia Expert System", layout="wide")

# تصميم الواجهة
st.title("🩺 النظام الخبير لتشخيص ذات الرئة عند الأطفال")
st.markdown("""
هذا التطبيق مبرمج بناءً على البيانات التفصيلية للملف المرفق، يهدف لمساعدة الأطباء في ترجيح المسببات بناءً على المعطيات السريرية.
""")

# وظيفة تحميل البيانات ومعالجتها
@st.cache_data
def load_and_clean_data():
    # هنا نقوم بمحاكاة قراءة الملف الذي رفعته مع التأكد من جلب كل الأعمدة
    data = {
        "المسبب (Cause)": [
            "Actinomycosis", "Adenovirus Infections", "AGNB (Anaerobic Gram-Negative Bacilli)", 
            "Bartonella henselae (Cat-Scratch)", "Histoplasmosis", "SARS-CoV-2", 
            "Human coronaviruses", "Cryptococcosis"
        ],
        "CXR_Findings": [
            "Abscesses, empyema, and rarely, pleurodermal sinuses.",
            "Severe lung involvement.",
            "Aspiration pneumonia, lung abscess, necrotizing pneumonia.",
            "Less common lung findings.",
            "Bilateral reticulonodular or miliary infiltrates.",
            "Unilateral or bilateral lung involvement, consolidation, ground glass opacities, ARDS.",
            "Less common findings.",
            "Solitary or multiple masses; patchy, segmental, or lobar consolidation; nodular pattern; ARDS."
        ],
        "Risk_Factors": [
            "Uncommon / Endogenous.",
            "Young infants and immunocompromised people.",
            "Neonatal (rare), Aspiration, Mucosal Surface Damage, Granulocytopenia, Chemotherapy.",
            "Immunocompromised people.",
            "Tumor necrosis factor [TNF] alpha antagonists, children younger than 1 year.",
            "Obesity and cardiac diseases.",
            "Young infants and immunocompromised people.",
            "Immunocompromised (Serious infections)."
        ],
        "Season": ["N/A", "N/A", "N/A", "Fall and Winter", "Endemic", "Endemic", "N/A", "N/A"],
        "Geography": ["Worldwide", "N/A", "N/A", "N/A", "Endemic areas", "N/A", "N/A", "N/A"],
        "Age_Group": ["N/A", "Any age / Young infants", "Neonatal (rare)", "N/A", "Children < 1 year", "N/A", "Young infants", "N/A"],
        "Sex": ["Male > Female", "N/A", "N/A", "N/A", "N/A", "Male > Female", "N/A", "N/A"],
        "Incubation": [
            "Varies (days to years)", "2 to 14 days", "1 to 5 days", "N/A", 
            "1 to 3 weeks", "5 to 14 days", "N/A", "N/A"
        ],
        "Diagnosis": [
            "Culture", "PCR", "Culture", "IgM and IgG serum antibodies", 
            "Serologic tests", "PCR", "N/A", "Cryptococcal antigen (CRAG) / Culture"
        ],
        "Treatment": [
            "IV Penicillin G/Ampicillin (4-6 weeks) then Oral Penicillin (6-12 months).",
            "Supportive care.",
            "Beta-lactamase inhibitor (Penicillin not for empirical), Cefoxitin, Linezolid. (Cefuroxime/Ceftriaxone not effective).",
            "Antimicrobial therapy (Azithromycin recommended for all immunocompromised).",
            "Amphotericin B or high-dose fluconazole. Total duration: 1 year.",
            "Supportive care.",
            "Supportive care.",
            "Amphotericin B (deoxycholate/liposomal) + oral flucytosine (25 mg/kg 4 times/day)."
        ]
    }
    return pd.DataFrame(data)

df = load_and_clean_data()

# --- القائمة الجانبية للفلاتر ---
st.sidebar.header("📥 إدخال البيانات السريرية")

# 1. البحث بالنص عن نتائج الأشعة أو عوامل الخطر
search_text = st.sidebar.text_input("ابحث عن علامة شعاعية (مثل: Abscess, ARDS):")

# 2. اختيار الجنس
gender_opt = st.sidebar.selectbox("الجنس:", ["الكل", "Male > Female"])

# 3. عوامل الخطر
risk_opt = st.sidebar.multiselect("عوامل الخطر الموجودة:", 
    ["Aspiration", "Immunocompromised", "Chemotherapy", "Obesity", "Infants", "Granulocytopenia"])

# --- منطق الفلترة ---
final_df = df.copy()

if search_text:
    final_df = final_df[
        final_df['CXR_Findings'].str.contains(search_text, case=False) | 
        final_df['Risk_Factors'].str.contains(search_text, case=False)
    ]

if gender_opt != "الكل":
    final_df = final_df[final_df['Sex'] == gender_opt]

if risk_opt:
    pattern = '|'.join(risk_opt)
    final_df = final_df[final_df['Risk_Factors'].str.contains(pattern, case=False)]

# --- عرض النتائج ---
st.subheader(f"🔍 المسببات المحتملة وفقاً للملف: ({len(final_df)})")

if not final_df.empty:
    for index, row in final_df.iterrows():
        with st.expander(f"📌 المسبب: {row['المسبب (Cause)']} "):
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown(f"**🖼️ نتائج الأشعة (CXR):**\n{row['CXR_Findings']}")
                st.markdown(f"**⚠️ عوامل الخطر:**\n{row['Risk_Factors']}")
                st.markdown(f"**🕒 فترة الحضانة:** {row['Incubation']}")
                st.markdown(f"**📅 الموسم:** {row['Season']}")

            with c2:
                st.markdown(f"**👶 العمر المستهدف:** {row['Age_Group']}")
                st.markdown(f"**🌍 التوزع الجغرافي:** {row['Geography']}")
                st.success(f"**🧪 التشخيص:**\n{row['Diagnosis']}")
                
            st.warning(f"**💊 بروتوكول العلاج:**\n{row['Treatment']}")
else:
    st.error("لم يتم العثور على نتائج تطابق هذه المعايير، يرجى توسيع نطاق البحث.")

# إضافة جدول كامل في النهاية للمراجعة
if st.checkbox("عرض الجدول الكامل للبيانات"):
    st.dataframe(df)
