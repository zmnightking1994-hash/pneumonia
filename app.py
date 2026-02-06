import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. إعداد الصفحة
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Red Book Pneumonia Guide",
    page_icon="📘",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. قاعدة البيانات الشاملة (القديمة + الجديدة من Red Book)
# -----------------------------------------------------------------------------
data = [
    # --- القسم الأول: البيانات السابقة ---
    {
        "Pneumonia Cause": "Actinomycosis",
        "Risk Factors": "Poor dental hygiene, aspiration, trauma",
        "CXR Findings": "Abscesses, empyema, rarely pleurodermal sinuses.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Adults > Children",
        "Sex": "Male > Female",
        "Incubation": "Days to years",
        "Diagnosis": "Culture",
        "Treatment": "Initial therapy: IV penicillin G or ampicillin (4-6 weeks). Followed by high-dose oral penicillin (up to 2 g/day adults) for 6-12 months total."
    },
    {
        "Pneumonia Cause": "Adenovirus",
        "Risk Factors": "Severe in young infants/immunocompromised.",
        "CXR Findings": "Diffuse interstitial infiltrates, hyperinflation.",
        "Season": "Year-round (peaks late winter/spring)",
        "Region": "Worldwide",
        "Age": "Children",
        "Sex": "Equal",
        "Incubation": "2-14 days",
        "Diagnosis": "PCR",
        "Treatment": "Supportive care. Cidofovir may be considered in severe immunocompromised cases (consult specialist)."
    },
    {
        "Pneumonia Cause": "Anaerobic Gram-Negative Bacilli",
        "Risk Factors": "Aspiration, poor dental hygiene",
        "CXR Findings": "Lung abscess, necrotizing pneumonia, empyema.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Any",
        "Sex": "Male > Female",
        "Incubation": "1-5 days",
        "Diagnosis": "Culture (requires anaerobic transport)",
        "Treatment": "Ampicillin-sulbactam, clindamycin, or carbapenems. Penicillin alone is not recommended due to beta-lactamase production."
    },
    {
        "Pneumonia Cause": "Bartonella henselae (Cat-Scratch)",
        "Risk Factors": "Cat exposure, immunocompromised",
        "CXR Findings": "Lymphadenopathy, rare nodules.",
        "Season": "Fall/Winter",
        "Region": "Worldwide",
        "Age": "Children/Young Adults",
        "Sex": "Equal",
        "Incubation": "1-3 weeks",
        "Diagnosis": "Serology (IgM/IgG)",
        "Treatment": "Azithromycin is drug of choice. Alternatives: Rifampin, Trimethoprim-Sulfamethoxazole, or Ciprofloxacin in adults."
    },
    {
        "Pneumonia Cause": "Chlamydia pneumoniae",
        "Risk Factors": "School-age children",
        "CXR Findings": "Patchy subsegmental infiltrates, pleural effusion rare.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "5-15 years",
        "Sex": "Equal",
        "Incubation": "3-4 weeks",
        "Diagnosis": "PCR",
        "Treatment": "Azithromycin (5 days), Clarithromycin (10 days), or Erythromycin. Doxycycline for older children/adolescents."
    },
     {
        "Pneumonia Cause": "Chlamydia trachomatis",
        "Risk Factors": "Infants of infected mothers",
        "CXR Findings": "Hyperinflation, interstitial infiltrates.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "2-19 weeks old",
        "Sex": "Equal",
        "Incubation": "1-3 weeks",
        "Diagnosis": "PCR / Culture",
        "Treatment": "Erythromycin (50 mg/kg/day) for 14 days OR Azithromycin (20 mg/kg/day) for 3 days. Monitor for pyloric stenosis in young infants."
    },
    {
        "Pneumonia Cause": "Cryptococcosis",
        "Risk Factors": "HIV, malignancy, organ transplant",
        "CXR Findings": "Single/multiple nodules, consolidation, interstitial.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Adults > Children",
        "Sex": "Male > Female",
        "Incubation": "Unknown",
        "Diagnosis": "Antigen (CrAg), Culture",
        "Treatment": "Severe/CNS disease: Amphotericin B + Flucytosine. Mild pulmonary: Fluconazole (6-12 months)."
    },

    # --- القسم الثاني: الإضافات الجديدة (من Red Book) ---
    {
        "Pneumonia Cause": "Cytomegalovirus (CMV)",
        "Risk Factors": "Post-transplant, HIV (CD4<50), Congenital",
        "CXR Findings": "Diffuse interstitial pneumonitis, ground-glass opacities.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Any (Immunocompromised)",
        "Sex": "Equal",
        "Incubation": "3-12 weeks (post-transfusion/transplant)",
        "Diagnosis": "PCR (Blood/BAL), Histopathology (Owl's eye)",
        "Treatment": "IV Ganciclovir is the drug of choice for severe pneumonia. Valganciclovir for step-down or less severe cases. Foscarnet or Cidofovir for resistant strains. Immune globulin (IVIG) sometimes added in pneumonitis."
    },
    {
        "Pneumonia Cause": "Enterovirus / Rhinovirus",
        "Risk Factors": "Asthma exacerbation, infants",
        "CXR Findings": "Peribronchial cuffing, hyperinflation, patchy infiltrates.",
        "Season": "Summer/Fall (Entero), Spring/Fall (Rhino)",
        "Region": "Worldwide",
        "Age": "Infants/Children",
        "Sex": "Equal",
        "Incubation": "3-6 days",
        "Diagnosis": "PCR (Respiratory panel)",
        "Treatment": "Supportive care (Oxygen, hydration). Pleconaril (investigational) for severe neonatal enteroviral sepsis but not routinely available."
    },
    {
        "Pneumonia Cause": "Epstein-Barr Virus (EBV)",
        "Risk Factors": "Adolescents (Mononucleosis)",
        "CXR Findings": "Interstitial infiltrates, hilar lymphadenopathy, splenomegaly.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Adolescents/Young Adults",
        "Sex": "Equal",
        "Incubation": "30-50 days",
        "Diagnosis": "Serology (Monospot, Specific Abs)",
        "Treatment": "Supportive care. Corticosteroids may be considered if there is impending airway obstruction. Antivirals (Acyclovir) generally NOT recommended for acute mono."
    },
    {
        "Pneumonia Cause": "Haemophilus influenzae (Type b)",
        "Risk Factors": "Unvaccinated children, asplenia",
        "CXR Findings": "Lobar consolidation, pleural effusion common.",
        "Season": "Year-round",
        "Region": "Worldwide (rare in vaccinated areas)",
        "Age": "< 5 years",
        "Sex": "Equal",
        "Incubation": "Unknown (likely 2-4 days)",
        "Diagnosis": "Culture (Blood/Pleural fluid), PCR",
        "Treatment": "Ceftriaxone or Cefotaxime (IV) initially. Ampicillin can be used if strain is beta-lactamase negative. Rifampin prophylaxis for household contacts may be indicated."
    },
    {
        "Pneumonia Cause": "Influenza Virus (A & B)",
        "Risk Factors": "Chronic heart/lung disease, pregnancy, young age",
        "CXR Findings": "Bilateral diffuse infiltrates, can look like bacterial pneumonia.",
        "Season": "Winter",
        "Region": "Worldwide",
        "Age": "Any",
        "Sex": "Equal",
        "Incubation": "1-4 days",
        "Diagnosis": "PCR (Rapid molecular assay)",
        "Treatment": "Oseltamivir (Tamiflu) should be started within 48 hours of onset. Baloxavir (single dose) for older children. Antibiotics added if secondary bacterial pneumonia (S. aureus/Pneumococcus) is suspected."
    },
    {
        "Pneumonia Cause": "Legionella pneumophila",
        "Risk Factors": "Immunosuppression, chronic lung disease, exposure to water systems",
        "CXR Findings": "Patchy unilobar infiltrates progressing to consolidation.",
        "Season": "Summer/Early Fall",
        "Region": "Worldwide",
        "Age": "Rare in healthy children",
        "Sex": "Male > Female",
        "Incubation": "2-10 days",
        "Diagnosis": "Urine Antigen (Serogroup 1), PCR, Culture",
        "Treatment": "Azithromycin or Levofloxacin (Fluoroquinolones) are preferred. Doxycycline is an alternative. Duration typically 5-14 days, longer (21 days) for immunocompromised."
    },
    {
        "Pneumonia Cause": "Measles (Rubeola)",
        "Risk Factors": "Unvaccinated, Vitamin A deficiency",
        "CXR Findings": "Diffuse reticulonodular infiltrates (Giant Cell Pneumonia).",
        "Season": "Late Winter/Spring",
        "Region": "Worldwide (Endemic areas)",
        "Age": "Unvaccinated",
        "Sex": "Equal",
        "Incubation": "8-12 days",
        "Diagnosis": "Serology (IgM), PCR",
        "Treatment": "Supportive care. High-dose Vitamin A is recommended for all children with severe measles. Ribavirin may be considered in severe pneumonitis in immunocompromised hosts."
    },
    {
        "Pneumonia Cause": "Mycoplasma pneumoniae",
        "Risk Factors": "School/Crowded settings",
        "CXR Findings": "Interstitial/Bronchopneumonia (worse than exam suggests).",
        "Season": "Year-round (peaks in Fall/Winter)",
        "Region": "Worldwide",
        "Age": "School age (5-15) & Young adults",
        "Sex": "Equal",
        "Incubation": "1-4 weeks",
        "Diagnosis": "PCR, Serology (IgM rise)",
        "Treatment": "Macrolides (Azithromycin 5 days, Clarithromycin). Tetracyclines (Doxycycline) or Fluoroquinolones (Levofloxacin) for older children or macrolide-resistant strains."
    },
    {
        "Pneumonia Cause": "Parainfluenza Virus",
        "Risk Factors": "Croup history, infants",
        "CXR Findings": "Hyperinflation, interstitial infiltrates.",
        "Season": "Fall (Types 1/2), Spring (Type 3)",
        "Region": "Worldwide",
        "Age": "6 months - 5 years",
        "Sex": "Male > Female",
        "Incubation": "2-6 days",
        "Diagnosis": "PCR",
        "Treatment": "Supportive care (Nebulized epinephrine/Corticosteroids if Croup is present). No specific antiviral therapy."
    },
    {
        "Pneumonia Cause": "Bordetella pertussis (Whooping Cough)",
        "Risk Factors": "Unvaccinated infants",
        "CXR Findings": "Perihilar infiltrates, 'shaggy heart' border.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Infants (most severe)",
        "Sex": "Female > Male (slight)",
        "Incubation": "7-10 days",
        "Diagnosis": "PCR, Culture",
        "Treatment": "Azithromycin (5 days), Clarithromycin (7 days), or Erythromycin (14 days). Treat early to reduce transmission; does not significantly alter course if started late."
    },
    {
        "Pneumonia Cause": "Pneumocystis jirovecii (PCP)",
        "Risk Factors": "HIV/AIDS, Chemotherapy, Transplant",
        "CXR Findings": "Bilateral diffuse ground-glass opacities.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Immunocompromised",
        "Sex": "Equal",
        "Incubation": "Variable",
        "Diagnosis": "Silver Stain, PCR of BAL",
        "Treatment": "Trimethoprim-Sulfamethoxazole (TMP-SMX) is the drug of choice (High dose). Adjunctive Corticosteroids indicated if PaO2 < 70 mmHg. Alternatives: Pentamidine, Atovaquone."
    },
    {
        "Pneumonia Cause": "Pseudomonas aeruginosa",
        "Risk Factors": "Cystic Fibrosis, Tracheostomy, Vent-associated",
        "CXR Findings": "Bronchopneumonia, nodular infiltrates with cavitation.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Any",
        "Sex": "Equal",
        "Incubation": "24-72 hours",
        "Diagnosis": "Culture",
        "Treatment": "Combination therapy typically required: Anti-pseudomonal Beta-lactam (Cefepime, Ceftazidime, Pip-Tazo, Meropenem) PLUS Aminoglycoside (Tobramycin/Amikacin) or Ciprofloxacin."
    },
    {
        "Pneumonia Cause": "Respiratory Syncytial Virus (RSV)",
        "Risk Factors": "Prematurity, BPD, CHD, Age < 6 months",
        "CXR Findings": "Hyperinflation, peribronchial thickening, atelectasis.",
        "Season": "Winter/Early Spring",
        "Region": "Worldwide",
        "Age": "Infants",
        "Sex": "Male > Female",
        "Incubation": "2-8 days",
        "Diagnosis": "PCR, Antigen test",
        "Treatment": "Supportive care (Hydration, Oxygen). Bronchodilators/Steroids NOT routinely recommended. Ribavirin aerosol considered only for severe immunocompromised cases."
    },
    {
        "Pneumonia Cause": "Staphylococcus aureus (MSSA/MRSA)",
        "Risk Factors": "Post-Influenza, Skin infection, CVCs",
        "CXR Findings": "Rapidly progressive consolidation, Pneumatoceles, Empyema.",
        "Season": "Year-round",
        "Region": "Worldwide",
        "Age": "Any (Infants/Elderly)",
        "Sex": "Male > Female",
        "Incubation": "Variable",
        "Diagnosis": "Culture (Blood/Sputum)",
        "Treatment": "MSSA: Oxacillin/Nafcillin or Cefazolin. MRSA: Vancomycin or Linezolid. Clindamycin if susceptible (D-test negative). Chest tube drainage often needed for empyema."
    },
    {
        "Pneumonia Cause": "Streptococcus pneumoniae (Pneumococcus)",
        "Risk Factors": "Asplenia, HIV, Cochlear implants",
        "CXR Findings": "Lobar consolidation (Classic), round pneumonia (kids).",
        "Season": "Winter",
        "Region": "Worldwide",
        "Age": "< 2 years & Elderly",
        "Sex": "Male > Female",
        "Incubation": "1-3 days",
        "Diagnosis": "Culture, Urine antigen",
        "Treatment": "High-dose Amoxicillin (oral) or Ampicillin (IV) for susceptible strains. Ceftriaxone or Cefotaxime for resistant strains or severe illness. Vancomycin added if meningitis suspected or highly resistant."
    },
    {
        "Pneumonia Cause": "Streptococcus pyogenes (Group A Strep)",
        "Risk Factors": "Recent Varicella (Chickenpox)",
        "CXR Findings": "Large pleural effusions/Empyema common.",
        "Season": "Winter/Spring",
        "Region": "Worldwide",
        "Age": "School age",
        "Sex": "Equal",
        "Incubation": "2-5 days",
        "Diagnosis": "Culture",
        "Treatment": "Penicillin G or Ampicillin. Clindamycin should be added for toxin suppression (Toxic Shock) and to improve efficacy."
    },
    {
        "Pneumonia Cause": "Mycobacterium tuberculosis (TB)",
        "Risk Factors": "Contact with active TB, travel to endemic area",
        "CXR Findings": "Hilar adenopathy, Ghon complex, cavitation (rare in young kids).",
        "Season": "Year-round",
        "Region": "Endemic areas",
        "Age": "Any",
        "Sex": "Equal",
        "Incubation": "2-10 weeks (to primary lesion)",
        "Diagnosis": "TST, IGRA, Gastric aspirate PCR/Culture",
        "Treatment": "Standard regimen: Isoniazid (INH), Rifampin (RIF), Pyrazinamide (PZA), and Ethambutol (EMB) for 2 months, followed by INH/RIF for 4 months. DOT (Directly Observed Therapy) recommended."
    }
]

# تحويل البيانات إلى إطار بيانات (DataFrame)
df = pd.DataFrame(data)

# -----------------------------------------------------------------------------
# 3. واجهة التطبيق (Sidebar & Main Area)
# -----------------------------------------------------------------------------

# الشريط الجانبي (Sidebar)
with st.sidebar:
    st.header("🔍 البحث والتصفية")
    
    # فلترة حسب المسبب
    search_term = st.text_input("ابحث عن اسم الفيروس/الجرثومة:")
    
    # قائمة الاختيار
    disease_list = df["Pneumonia Cause"].unique()
    selected_disease = st.selectbox(
        "أو اختر من القائمة الكاملة:",
        disease_list,
        index=list(disease_list).index("Cytomegalovirus (CMV)") if "Cytomegalovirus (CMV)" in disease_list else 0
    )
    
    st.markdown("---")
    
    # زر تحميل البيانات
    st.write("📥 **تصدير البيانات**")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل ملف Excel (CSV)",
        data=csv,
        file_name='redbook_pneumonia_comprehensive.csv',
        mime='text/csv',
    )
    
    st.markdown("---")
    st.info("Source: AAP Red Book Guidelines")

# تحديد المرض المعروض بناءً على البحث أو الاختيار
if search_term:
    filtered_df = df[df["Pneumonia Cause"].str.contains(search_term, case=False)]
    if not filtered_df.empty:
        row = filtered_df.iloc[0]
    else:
        st.error("لم يتم العثور على نتائج.")
        st.stop()
else:
    row = df[df["Pneumonia Cause"] == selected_disease].iloc[0]

# -----------------------------------------------------------------------------
# 4. عرض التفاصيل (Main Content)
# -----------------------------------------------------------------------------

st.title(f"🦠 {row['Pneumonia Cause']}")
st.caption(f"Comprehensive details based on Clinical Guidelines")
st.markdown("---")

# عرض المعلومات الديموغرافية في أعمدة
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Region", value=row['Region'])
with col2:
    st.metric(label="Season", value=row['Season'])
with col3:
    st.metric(label="Typical Age", value=row['Age'])
with col4:
    st.metric(label="Sex Predilection", value=row['Sex'])

# تفاصيل التشخيص والعوامل
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("⚠️ Risk Factors")
    st.info(row['Risk Factors'])
    
    st.subheader("🧪 Diagnosis")
    st.write(row['Diagnosis'])

with c2:
    st.subheader("🩻 CXR Findings")
    st.warning(row['CXR Findings'])
    
    st.subheader("⏳ Incubation")
    st.write(row['Incubation'])

# قسم العلاج (مميز)
st.markdown("---")
st.header("💊 Treatment & Management (Red Book Style)")

# تنسيق مخصص لصندوق العلاج
st.markdown(f"""
<div style="
    background-color: #e8f4f8;
    border-left: 6px solid #0072b5;
    padding: 20px;
    border-radius: 8px;
    font-size: 18px;
    color: #333;
    line-height: 1.6;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
">
    {row['Treatment']}
</div>
""", unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("**Note:** This application is for educational purposes. Dosages should always be verified with the latest edition of the AAP Red Book.")
