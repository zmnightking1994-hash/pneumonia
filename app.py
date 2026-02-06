import streamlit as st
import pandas as pd

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Pneumonia Expert System", page_icon="🩺", layout="wide")

# -----------------------------------------------------------------------------
# قاعدة البيانات الشاملة (البيانات مستخرجة من Red Book و CSV المرفق)
# -----------------------------------------------------------------------------
pneumonia_data = [
    {
        "Cause": "Actinomycosis",
        "Age": "Adults / Adolescents",
        "Season": "Year-round",
        "CXR": "Abscess, Empyema, Pleurodermal sinuses",
        "Risk_Factors": "Poor dental hygiene, Aspiration",
        "Treatment": "Initial: IV Penicillin G or Ampicillin (4-6 weeks). Follow-up: High-dose oral Penicillin (6-12 months).",
        "Clinical_Note": "Slow progression, often crosses anatomical boundaries (mass-like)."
    },
    {
        "Cause": "Adenovirus",
        "Age": "Infants, Young children",
        "Season": "Winter, Spring, Summer",
        "CXR": "Hyperinflation, Interstitial infiltrates, Patchy consolidation",
        "Risk_Factors": "Daycare, Immunocompromised",
        "Treatment": "Primarily Supportive. Cidofovir may be considered for severe disease in immunocompromised patients.",
        "Clinical_Note": "Often associated with conjunctivitis, pharyngitis, and high fever."
    },
    {
        "Cause": "Anaerobic Bacteria (AGNB)",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Abscess, Necrotizing pneumonia, Aspiration pattern (Right Middle/Lower Lobe)",
        "Risk_Factors": "Aspiration, Poor dental hygiene, Mucosal damage",
        "Treatment": "Clindamycin, or Ampicillin-Sulbactam (Unasyn). Penicillin G is no longer recommended for empiric treatment of severe cases.",
        "Clinical_Note": "Putid (foul-smelling) sputum or empyema fluid is a classic sign."
    },
    {
        "Cause": "Bartonella henselae (Cat-Scratch Disease)",
        "Age": "Children, Adolescents",
        "Season": "Fall, Winter",
        "CXR": "Hilar lymphadenopathy, Nodular infiltrates",
        "Risk_Factors": "Cat/Kitten exposure (scratches/bites)",
        "Treatment": "Azithromycin (5 days). For severe/systemic: Rifampin, Trimethoprim-Sulfamethoxazole, or Ciprofloxacin.",
        "Clinical_Note": "Pulmonary involvement is rare but occurs in systemic forms."
    },
    {
        "Cause": "Blastomycosis",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Mass-like lesions (mimics tumor), Cavitation, Lobar consolidation",
        "Risk_Factors": "Exposure to soil/decaying wood (Great Lakes, Mississippi River basins)",
        "Treatment": "Mild/Moderate: Itraconazole (6-12 months). Severe: Amphotericin B followed by Itraconazole.",
        "Clinical_Note": "Often involves skin, bones, and genitourinary tract."
    },
    {
        "Cause": "Chlamydia pneumoniae",
        "Age": "School age (5-15y), Adolescents",
        "Season": "Year-round",
        "CXR": "Subsegmental patchy infiltrates (often unilateral)",
        "Risk_Factors": "Close contact, Schools/Dormitories",
        "Treatment": "Azithromycin (5 days), Clarithromycin (7-10 days), or Doxycycline (>8y).",
        "Clinical_Note": "Gradual onset, 'hoarseness' is a common early symptom."
    },
    {
        "Cause": "Chlamydia trachomatis",
        "Age": "Young infants (2-19 weeks old)",
        "Season": "Year-round",
        "CXR": "Hyperinflation, Diffuse interstitial infiltrates",
        "Risk_Factors": "Vaginal delivery from infected mother",
        "Treatment": "Erythromycin (14 days) or Azithromycin (3 days). Monitor for infantile hypertrophic pyloric stenosis.",
        "Clinical_Note": "Classic 'staccato cough', tachypnea, and absence of fever."
    },
    {
        "Cause": "Coccidioidomycosis (Valley Fever)",
        "Age": "Any age",
        "Season": "Year-round (peaks after dust storms)",
        "CXR": "Ipsilateral Hilar adenopathy, Thin-walled cavities, Effusion",
        "Risk_Factors": "Southwestern US (Desert), Dust exposure",
        "Treatment": "Fluconazole or Itraconazole (3-6 months). Amphotericin B for disseminated disease.",
        "Clinical_Note": "Associated with Erythema Nodosum or Erythema Multiforme."
    },
    {
        "Cause": "Cryptococcosis",
        "Age": "Immunocompromised",
        "Season": "Year-round",
        "CXR": "Solitary or multiple masses, Nodular pattern, Ground-glass (in ARDS)",
        "Risk_Factors": "HIV/AIDS, Transplant, Pigeon droppings",
        "Treatment": "Amphotericin B + Flucytosine (induction), followed by Fluconazole.",
        "Clinical_Note": "Always check for Meningitis (CSF Cryptococcal Antigen)."
    },
    {
        "Cause": "Cytomegalovirus (CMV)",
        "Age": "Immunocompromised, Neonates",
        "Season": "Year-round",
        "CXR": "Diffuse Interstitial, Ground-glass opacities",
        "Risk_Factors": "Transplant recipients, HIV",
        "Treatment": "IV Ganciclovir. Valganciclovir (oral) for maintenance.",
        "Clinical_Note": "CMV pneumonia in transplant patients has high mortality."
    },
    {
        "Cause": "Histoplasmosis",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Miliary pattern (diffuse small nodules), Hilar lymphadenopathy",
        "Risk_Factors": "Bird/Bat droppings, Ohio/Mississippi River valleys",
        "Treatment": "Mild: Observation or Itraconazole. Severe: Amphotericin B (1-2 weeks) then Itraconazole (12 weeks).",
        "Clinical_Note": "Can cause mediastinal fibrosis in rare cases."
    },
    {
        "Cause": "Influenza (A & B)",
        "Age": "Any age",
        "Season": "Winter",
        "CXR": "Bilateral diffuse infiltrates, can lead to secondary bacterial consolidation",
        "Risk_Factors": "Seasonal outbreaks, Crowded areas",
        "Treatment": "Oseltamivir (Tamiflu), Baloxavir (>12y), or IV Peramivir for severe cases.",
        "Clinical_Note": "Rapid onset of high fever, myalgia, and dry cough."
    },
    {
        "Cause": "Legionella pneumophila",
        "Age": "Adults, Rare in children",
        "Season": "Summer, Fall",
        "CXR": "Rapidly progressive patchy consolidation, Effusion",
        "Risk_Factors": "Contaminated water systems, Cooling towers, Hot tubs",
        "Treatment": "Azithromycin or Levofloxacin (7-14 days).",
        "Clinical_Note": "Often accompanied by GI symptoms (diarrhea) and hyponatremia."
    },
    {
        "Cause": "Mycoplasma pneumoniae",
        "Age": "School age, Adolescents",
        "Season": "Year-round (peaks in Fall)",
        "CXR": "Reticulonodular infiltrates, 'Worse than clinical exam'",
        "Risk_Factors": "Schools, Military barracks",
        "Treatment": "Azithromycin, Clarithromycin, or Doxycycline/Levofloxacin (if resistant).",
        "Clinical_Note": "Walking pneumonia; extra-pulmonary: Stevens-Johnson syndrome, Hemolytic anemia."
    },
    {
        "Cause": "Pneumocystis jirovecii (PCP)",
        "Age": "Infants (HIV+), Immunocompromised",
        "Season": "Year-round",
        "CXR": "Diffuse Bilateral Ground-glass opacities, 'Bat-wing' appearance",
        "Risk_Factors": "HIV (CD4 < 200), Cancer, Steroid use",
        "Treatment": "High-dose Trimethoprim-Sulfamethoxazole (TMP-SMX) + Prednisone (if PaO2 < 70).",
        "Clinical_Note": "Hypoxemia out of proportion to CXR findings."
    },
    {
        "Cause": "Pneumococcus (Streptococcus pneumoniae)",
        "Age": "Any age (very common in all)",
        "Season": "Winter, Spring",
        "CXR": "Lobar consolidation, Round pneumonia (in children), Pleural effusion",
        "Risk_Factors": "Post-viral (Flu), Asplenia, Sickle cell",
        "Treatment": "Amoxicillin (high dose), Ceftriaxone, or Vancomycin (if highly resistant).",
        "Clinical_Note": "The most common cause of bacterial pneumonia. Sudden chill/fever."
    },
    {
        "Cause": "Respiratory Syncytial Virus (RSV)",
        "Age": "Infants (<2 years)",
        "Season": "Winter, Spring",
        "CXR": "Hyperinflation, Atelectasis, Peribronchial thickening",
        "Risk_Factors": "Prematurity, CHD, Daycare",
        "Treatment": "Supportive (Oxygen, Fluids). Ribavirin (aerosol) only for extremely high-risk patients.",
        "Clinical_Note": "Significant wheezing and respiratory distress in infants."
    },
    {
        "Cause": "SARS-CoV-2 (COVID-19)",
        "Age": "Any age",
        "Season": "Year-round/Endemic",
        "CXR": "Peripheral ground-glass opacities, Bilateral consolidation",
        "Risk_Factors": "Obesity, Diabetes, Cardiac disease",
        "Treatment": "Supportive, Remdesivir, Dexamethasone (if requiring oxygen).",
        "Clinical_Note": "Risk of MIS-C in children weeks after infection."
    },
    {
        "Cause": "Staphylococcus aureus (MRSA/MSSA)",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Pneumatoceles, Cavitation, Rapidly changing infiltrates, Empyema",
        "Risk_Factors": "Post-influenza, Skin infections, PICU",
        "Treatment": "MSSA: Nafcillin/Cefazolin. MRSA: Vancomycin or Linezolid.",
        "Clinical_Note": "Very aggressive; can cause necrotizing pneumonia."
    },
    {
        "Cause": "Tuberculosis (Mycobacterium)",
        "Age": "Any age",
        "Season": "Year-round",
        "CXR": "Hilar adenopathy (primary), Cavitation (reactivation), Miliary",
        "Risk_Factors": "Travel to endemic area, Contact with active case",
        "Treatment": "RIPE (Rifampin, INH, PZA, EMB) for 2 months, then RI for 4-7 months.",
        "Clinical_Note": "Weight loss, night sweats, chronic cough."
    },
    {
        "Cause": "Tularemia (Francisella tularensis)",
        "Age": "Any age",
        "Season": "Summer (ticks), Winter (hunting)",
        "CXR": "Patchy infiltrates, Hilar adenopathy, Pleural effusion",
        "Risk_Factors": "Rabbit exposure, Tick/Deer fly bites, Laboratory exposure",
        "Treatment": "Gentamicin or Streptomycin. Alternative: Ciprofloxacin or Doxycycline.",
        "Clinical_Note": "Potential bioterrorism agent; very low infectious dose."
    }
]

df = pd.DataFrame(pneumonia_data)

# -----------------------------------------------------------------------------
# الواجهة البرمجية (The UI)
# -----------------------------------------------------------------------------
st.title("🛡️ نظام الخبير لتشخيص التهاب الرئة (Red Book Edition)")
st.write("أدخل المتغيرات السريرية التي لاحظتها على المريض للحصول على التشخيص التفريقي:")

# --- الفلاتر الجانبية ---
with st.sidebar:
    st.header("⚙️ الفلاتر الذكية")
    
    age_filter = st.selectbox("الفئة العمرية:", 
                              ["الكل", "Young infants", "Infants", "Children", "School age", "Adolescents", "Adults", "Immunocompromised"])
    
    season_filter = st.selectbox("الموسم الحالي:", 
                                 ["الكل", "Winter", "Spring", "Summer", "Fall", "Year-round"])
    
    cxr_options = ["Interstitial", "Lobar consolidation", "Hyperinflation", "Abscess", "Cavitation", "Pneumatoceles", "Hilar adenopathy", "Ground-glass", "Miliary", "Atelectasis"]
    cxr_filter = st.multiselect("موجودات الأشعة (CXR):", cxr_options)

# --- محرك البحث (The Filtering Engine) ---
def filter_logic(age, season, cxr_list):
    results = df.copy()
    
    if age != "الكل":
        results = results[results['Age'].str.contains(age, case=False, na=False) | (results['Age'].str.contains("Any", case=False))]
    
    if season != "الكل":
        results = results[results['Season'].str.contains(season, case=False, na=False) | (results['Season'].str.contains("Year-round", case=False))]
        
    if cxr_list:
        # البحث عن أي كلمة مفتاحية من المختار في عمود CXR
        pattern = '|'.join(cxr_list)
        results = results[results['CXR'].str.contains(pattern, case=False, na=False)]
        
    return results

final_results = filter_logic(age_filter, season_filter, cxr_filter)

# --- عرض النتائج ---
st.subheader(f"🔍 التشخيصات التفريقية المحتملة: ({len(final_results)})")

if not final_results.empty:
    for idx, row in final_results.iterrows():
        with st.expander(f"📌 {row['Cause']}"):
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                st.markdown(f"**👤 العمر:** {row['Age']}")
                st.markdown(f"**📅 الموسم:** {row['Season']}")
                st.markdown(f"**🩻 الأشعة:** {row['CXR']}")
                st.markdown(f"**⚠️ عوامل الخطر:** {row['Risk_Factors']}")
            
            with col_b:
                st.warning(f"**💡 ملحوظة سريرية:** {row['Clinical_Note']}")
                st.success(f"**💊 بروتوكول العلاج الموصى به:**\n\n{row['Treatment']}")
else:
    st.error("❌ لم يتم العثور على تطابق. حاول توسيع خيارات البحث (مثلاً اختر 'الكل' في العمر أو الموسم).")

# --- ميزات إضافية ---
st.divider()
st.info("""
**دليل الاستخدام:**
1. إذا كانت الأشعة تظهر **Cavitation**، جرب اختيارها من القائمة لرؤية المسببات مثل (Staph aureus, TB, Actinomycosis).
2. إذا كان المريض **Infant** في الشتاء، ستظهر لك فيروسات مثل RSV و Adenovirus.
3. اضغط على اسم المرض لمشاهدة بروتوكول العلاج التفصيلي المستخرج من Red Book.
""")
