
import streamlit as st
# Add this as the FIRST line of app.py
from database import *

# Page configuration
st.set_page_config(
    page_title="Maternal Health Platform",
    page_icon="🤱",
    layout="wide"
)

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title("🤱 MaternalCare")
st.sidebar.markdown("---")

page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "📝 Register",
    "📊 Health Tracker",
    "💊 Medicine Tracker",
    "🥗 Nutrition Guide",
    "🔮 Risk Assessment",
    "🏛️ Government Schemes",
    "📈 Dashboard",
    "🧠 PPD Screening"
])

# ============================================
# PAGE 1: HOME
# ============================================
if page == "🏠 Home":
    st.title("🤱 Smart Maternal Health Platform")
    st.markdown("### *From Pregnancy to Recovery — Powered by Data*")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👩 Total Users", "1,247")
    col2.metric("🔴 High Risk", "43")
    col3.metric("💊 Medicine Compliance", "78%")
    col4.metric("💰 Schemes Claimed", "₹12.5L")
    
    st.markdown("---")
    
    st.markdown("""
    ## Welcome! 🙏
    
    This app helps pregnant women in rural areas by providing:
    
    - 📊 **Health Tracking** — Log your daily vitals
    - 💊 **Medicine Reminders** — Never miss your supplements
    - 🥗 **Nutrition Guide** — Eat right for your baby
    - 🔮 **Risk Assessment** — AI-powered health predictions
    - 🏛️ **Government Schemes** — Get the money you deserve
    - 📈 **Health Dashboard** — See your progress
    - 🧠 **Mental Health** — Postpartum depression screening
    
    ### How to use:
    1. First, go to **📝 Register** and enter your details
    2. Then use **📊 Health Tracker** daily
    3. Check **💊 Medicine Tracker** every morning
    4. Visit **🏛️ Government Schemes** to see your benefits
    """)

# ============================================
# PAGE 2: REGISTRATION
# ============================================
elif page == "📝 Register":
    st.title("📝 New Registration")
    st.markdown("Enter the pregnant woman's details below:")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👩 Full Name", placeholder="Enter full name")
        age = st.number_input("📅 Age", min_value=15, max_value=50, value=25)
        phone = st.text_input("📱 Phone Number", placeholder="10 digit number")
        village = st.text_input("🏘️ Village", placeholder="Village name")
        district = st.text_input("📍 District", placeholder="District name")
        state = st.selectbox("🗺️ State", [
            "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan",
            "Jharkhand", "Odisha", "Chhattisgarh", "Assam",
            "West Bengal", "Maharashtra", "Other"
        ])
    
    with col2:
        lmp_date = st.date_input("🩸 Last Menstrual Period (LMP) Date")
        height = st.number_input("📏 Height (cm)", min_value=120, max_value=200, value=155)
        weight = st.number_input("⚖️ Current Weight (kg)", min_value=30.0, max_value=150.0, value=55.0)
        blood_group = st.selectbox("🩸 Blood Group", [
            "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Don't know"
        ])
        previous_pregnancies = st.number_input("🤰 Previous Pregnancies", min_value=0, max_value=10, value=0)
        previous_complications = st.selectbox("⚠️ Any Previous Complications?", [
            "No", "High BP", "Diabetes", "Miscarriage", "C-Section", "Other"
        ])
    
    st.markdown("---")
    
    if st.button("✅ Register Now", type="primary"):
        if name and phone:
            # Calculate pregnancy details
            from datetime import date, timedelta
            today = date.today()
            days_pregnant = (today - lmp_date).days
            current_week = days_pregnant // 7
            edd = lmp_date + timedelta(days=280)
            
            # Determine trimester
            if current_week <= 12:
                trimester = "First Trimester"
            elif current_week <= 26:
                trimester = "Second Trimester"
            else:
                trimester = "Third Trimester"
            
            # Calculate BMI
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            # Save to database
            user_id = add_user(
                name, age, phone, village, district, state,
                str(lmp_date), str(edd), current_week, trimester,
                weight, height, round(bmi, 1), blood_group,
                previous_pregnancies, previous_complications
            )
            st.session_state['user_id'] = user_id
            # Save to session state (temporary storage)
            st.session_state['user_data'] = {
                'name': name,
                'age': age,
                'phone': phone,
                'village': village,
                'district': district,
                'state': state,
                'lmp_date': str(lmp_date),
                'edd_date': str(edd),
                'current_week': current_week,
                'trimester': trimester,
                'weight': weight,
                'height': height,
                'bmi': round(bmi, 1),
                'blood_group': blood_group,
                'previous_pregnancies': previous_pregnancies,
                'previous_complications': previous_complications
            }
            
            # Show success
            st.success("✅ Registration Successful!")
            st.balloons()
            
            st.markdown("---")
            st.subheader("📋 Your Pregnancy Summary:")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Week", f"Week {current_week}")
            col2.metric("Trimester", trimester)
            col3.metric("Expected Delivery", str(edd))
            col4.metric("BMI", f"{bmi:.1f}")
            
            # Week-specific advice
            st.markdown("---")
            st.subheader(f"📖 Week {current_week} Guide:")
            
            if current_week <= 4:
                st.info("""
                🌱 **Very Early Pregnancy**
                - Start taking Folic Acid (400mcg) immediately
                - Avoid smoking and alcohol
                - Eat healthy, drink plenty of water
                - Schedule your first doctor visit
                """)
            elif current_week <= 8:
                st.info("""
                🌱 **Weeks 5-8: Baby's organs are forming**
                - Continue Folic Acid
                - Morning sickness is normal
                - Eat small, frequent meals
                - Get blood tests done (hemoglobin, blood group)
                """)
            elif current_week <= 12:
                st.info("""
                🌱 **Weeks 9-12: First trimester ending**
                - Get first ultrasound done
                - Start Iron + Folic Acid tablets
                - Register at nearest PHC/hospital
                - Apply for PMMVY scheme
                """)
            elif current_week <= 16:
                st.info("""
                🌿 **Weeks 13-16: Second trimester begins**
                - Energy levels improving
                - Start gentle walking daily
                - Eat calcium-rich foods (milk, curd)
                - Take Calcium supplements
                """)
            elif current_week <= 20:
                st.info("""
                🌿 **Weeks 17-20: Baby is growing fast**
                - You may feel baby's first movements!
                - Get anomaly scan (ultrasound)
                - Continue all supplements
                - Eat protein-rich food (dal, eggs)
                """)
            elif current_week <= 26:
                st.info("""
                🌿 **Weeks 21-26: Baby is getting bigger**
                - Glucose tolerance test due
                - Watch for swelling in feet
                - Sleep on your left side
                - Stay hydrated
                """)
            elif current_week <= 32:
                st.info("""
                🌳 **Weeks 27-32: Third trimester!**
                - More frequent checkups needed
                - Watch for warning signs (headache, blurred vision)
                - Pack your hospital bag
                - Get TT vaccination
                """)
            elif current_week <= 36:
                st.info("""
                🌳 **Weeks 33-36: Almost there!**
                - Baby is getting into position
                - Hospital bag should be ready
                - Know the signs of labor
                - Keep emergency numbers handy
                """)
            else:
                st.warning("""
                🌳 **Weeks 37-40: Baby can come any day!**
                - Be ready to go to hospital
                - Signs of labor: regular contractions, water breaking
                - Keep documents ready (Aadhar, MCP card)
                - Call ASHA worker when labor starts
                """)
        else:
            st.error("❌ Please enter at least Name and Phone Number!")

# ============================================
# PAGE 3: HEALTH TRACKER
# ============================================
elif page == "📊 Health Tracker":
    st.title("📊 Daily Health Tracker")
    st.markdown("Log your health details every day:")
    st.markdown("---")
    
    # Check if user is registered
    user_data = st.session_state.get('user_data', None)
    if user_data:
        st.success(f"👩 Patient: {user_data['name']} | Week: {user_data['current_week']} | {user_data['trimester']}")
    
    st.subheader("Today's Vitals")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight = st.number_input("⚖️ Weight (kg)", 30.0, 150.0, 55.0, 0.5)
        temperature = st.number_input("🌡️ Temperature (°F)", 95.0, 105.0, 98.6, 0.1)
    
    with col2:
        bp_systolic = st.number_input("🫀 BP Upper (Systolic)", 70, 200, 120)
        bp_diastolic = st.number_input("🫀 BP Lower (Diastolic)", 40, 130, 80)
    
    with col3:
        hemoglobin = st.number_input("🩸 Hemoglobin (g/dL)", 4.0, 18.0, 11.0, 0.1)
        blood_sugar = st.number_input("🍬 Blood Sugar (mg/dL)", 50, 400, 100)
    
    st.markdown("---")
    st.subheader("Symptoms Today")
    
    symptoms = st.multiselect("Select any symptoms you have:", [
        "Headache",
        "Swelling in feet/hands",
        "Bleeding/Spotting",
        "Severe nausea/vomiting",
        "Blurred vision",
        "Chest pain",
        "Reduced baby movement",
        "Fever",
        "Painful urination",
        "Back pain",
        "Difficulty breathing",
        "No symptoms - feeling good! ✅"
    ])
    
    water_intake = st.slider("💧 How many glasses of water today?", 0, 15, 8)
    sleep_hours = st.slider("😴 Hours of sleep last night?", 0, 14, 7)
    mood = st.select_slider("😊 How are you feeling?", 
        options=["Very Sad 😢", "Sad 😔", "Okay 😐", "Good 😊", "Very Happy 😄"])
    
    st.markdown("---")
    
    if st.button("💾 Save Today's Health Log", type="primary"):
        # Save to session state
        if 'health_logs' not in st.session_state:
            st.session_state['health_logs'] = []
        
        from datetime import date
        log = {
            'date': str(date.today()),
            'weight': weight,
            'bp_systolic': bp_systolic,
            'bp_diastolic': bp_diastolic,
            'hemoglobin': hemoglobin,
            'blood_sugar': blood_sugar,
            'temperature': temperature,
            'symptoms': symptoms,
            'water_intake': water_intake,
            'sleep_hours': sleep_hours,
            'mood': mood
        }
        st.session_state['health_logs'].append(log)
                # Save to database
        if 'user_id' in st.session_state:
            add_health_log(
                st.session_state['user_id'],
                weight, bp_systolic, bp_diastolic,
                hemoglobin, blood_sugar, temperature,
                symptoms, water_intake, sleep_hours, mood
            )
        
        st.success("✅ Health log saved successfully!")
        
        # INSTANT HEALTH ALERTS
        st.markdown("### 🔍 Instant Health Analysis:")
        
        alerts = []
        
        # BP Check
        if bp_systolic > 140 or bp_diastolic > 90:
            alerts.append(("🔴 HIGH BLOOD PRESSURE", 
                "BP is above 140/90. This could be a sign of preeclampsia. Visit doctor TODAY!", 
                "error"))
        elif bp_systolic > 130 or bp_diastolic > 85:
            alerts.append(("🟡 SLIGHTLY HIGH BP", 
                "BP is slightly elevated. Rest, reduce salt, monitor daily.", 
                "warning"))
        else:
            alerts.append(("🟢 BP Normal", "Blood pressure is in healthy range.", "success"))
        
        # Hemoglobin Check
        if hemoglobin < 7:
            alerts.append(("🔴 SEVERE ANEMIA", 
                "Hemoglobin is dangerously low! You need immediate medical attention and possibly a blood transfusion.", 
                "error"))
        elif hemoglobin < 11:
            alerts.append(("🟡 MILD ANEMIA", 
                "Hemoglobin is low. Take Iron tablets regularly and eat iron-rich foods (spinach, jaggery, dates).", 
                "warning"))
        else:
            alerts.append(("🟢 Hemoglobin Normal", "Iron levels are good. Keep taking supplements.", "success"))
        
        # Blood Sugar Check
        if blood_sugar > 200:
            alerts.append(("🔴 VERY HIGH BLOOD SUGAR", 
                "This could indicate gestational diabetes. See doctor immediately!", 
                "error"))
        elif blood_sugar > 140:
            alerts.append(("🟡 HIGH BLOOD SUGAR", 
                "Blood sugar is elevated. Reduce sweets, eat more fiber.", 
                "warning"))
        else:
            alerts.append(("🟢 Blood Sugar Normal", "Sugar levels are fine.", "success"))
        
        # Temperature Check
        if temperature > 100.4:
            alerts.append(("🔴 FEVER DETECTED", 
                "You have fever. This needs medical attention during pregnancy!", 
                "error"))
        
        # Symptom Checks
        dangerous_symptoms = ["Bleeding/Spotting", "Blurred vision", "Chest pain", 
                              "Reduced baby movement", "Severe nausea/vomiting"]
        found_dangerous = [s for s in symptoms if s in dangerous_symptoms]
        
        if found_dangerous:
            alerts.append(("🔴 DANGEROUS SYMPTOMS", 
                f"You reported: {', '.join(found_dangerous)}. Visit hospital IMMEDIATELY!", 
                "error"))
        
        # Water intake
        if water_intake < 5:
            alerts.append(("🟡 LOW WATER INTAKE", 
                "Drink at least 8-10 glasses of water daily!", 
                "warning"))
        
        # Display all alerts
        for title, message, alert_type in alerts:
            if alert_type == "error":
                st.error(f"**{title}**: {message}")
            elif alert_type == "warning":
                st.warning(f"**{title}**: {message}")
            else:
                st.success(f"**{title}**: {message}")

# ============================================
# PAGE 4: MEDICINE TRACKER
# ============================================
elif page == "💊 Medicine Tracker":
    st.title("💊 Medicine Schedule & Tracker")
    st.markdown("---")
    
    # Get current week
    user_data = st.session_state.get('user_data', None)
    current_week = user_data['current_week'] if user_data else st.number_input("Enter your pregnancy week:", 1, 42, 12)
    
    # Determine trimester
    if current_week <= 12:
        trimester = "First Trimester"
    elif current_week <= 26:
        trimester = "Second Trimester"
    elif current_week <= 40:
        trimester = "Third Trimester"
    else:
        trimester = "Post Delivery"
    
    st.subheader(f"📅 Week {current_week} — {trimester}")
    st.markdown("---")
    
    # Medicine schedules by trimester
    st.subheader("Your Daily Medicines:")
    
    medicines = []
    
    if current_week <= 12:
        medicines = [
            {"name": "Folic Acid", "dose": "400 mcg (1 tablet)", "time": "🌅 Morning after breakfast", "why": "Prevents brain/spine defects in baby"},
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Prevents anemia, keeps blood healthy"},
        ]
    elif current_week <= 26:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Prevents anemia"},
            {"name": "Calcium", "dose": "500mg (1 tablet)", "time": "🌅 Morning", "why": "Baby's bones need calcium"},
            {"name": "Vitamin D", "dose": "As prescribed", "time": "☀️ With meals", "why": "Helps absorb calcium"},
        ]
    elif current_week <= 40:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Continue for blood health"},
            {"name": "Calcium", "dose": "500mg (1 tablet)", "time": "🌅 Morning", "why": "Baby's bones growing rapidly"},
            {"name": "TT Vaccine", "dose": "Check with doctor", "time": "🏥 At health center", "why": "Protects baby from tetanus"},
        ]
    else:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "Continue for 6 months", "time": "🌙 Night", "why": "Recovery from delivery"},
            {"name": "Calcium", "dose": "500mg", "time": "🌅 Morning", "why": "Breastfeeding needs calcium"},
            {"name": "Vitamin A", "dose": "As prescribed", "time": "🏥 At health center", "why": "Postpartum recovery"},
        ]
    
    # Display medicines with checkboxes
    st.markdown("### ✅ Mark what you took today:")
    
    taken_count = 0
    for i, med in enumerate(medicines):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            **{med['name']}**  
            💊 Dose: {med['dose']}  
            ⏰ When: {med['time']}  
            ❓ Why: {med['why']}
            """)
        with col2:
            taken = st.checkbox("Taken ✅", key=f"med_{i}")
            if taken:
                taken_count += 1
        st.markdown("---")
    
    # Compliance score
    if medicines:
        compliance = (taken_count / len(medicines)) * 100
        st.subheader(f"Today's Compliance: {compliance:.0f}%")
        
        if compliance == 100:
            st.success("🌟 Excellent! All medicines taken! Keep it up!")
            st.balloons()
        elif compliance >= 50:
            st.warning("⚠️ You missed some medicines. Try to take them all!")
        else:
            st.error("❌ Please take your medicines! They are very important for your baby's health!")
    
    # Important tips
    st.markdown("---")
    st.subheader("💡 Important Tips:")
    st.info("""
    - Take Iron tablets with **orange juice or lemon water** (Vitamin C helps absorption)
    - Do NOT take Iron tablets with **milk or tea** (they block absorption)
    - Take Iron and Calcium at **different times** (they interfere with each other)
    - If Iron tablets cause constipation, eat **papaya, isabgol, or more vegetables**
    - Never stop medicines without asking doctor
    """)

# ============================================
# PAGE 5: NUTRITION GUIDE
# ============================================
elif page == "🥗 Nutrition Guide":
    st.title("🥗 Nutrition Guide & Food Logger")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📝 Log Today's Food", "📖 Nutrition Guide"])
    
    with tab1:
        st.subheader("What did you eat today?")
        
        st.markdown("### 🌅 Breakfast")
        breakfast = st.multiselect("Select breakfast items:", [
            "Roti (2)", "Paratha", "Poha", "Upma", "Idli", "Dosa",
            "Daliya (Porridge)", "Bread & Butter", "Egg (boiled/omelette)",
            "Milk (1 glass)", "Tea", "Banana", "Apple", "Sprouts",
            "Curd/Yogurt", "Peanuts/Dry fruits"
        ], key="breakfast")
        
        st.markdown("### ☀️ Lunch")
        lunch = st.multiselect("Select lunch items:", [
            "Rice (1 plate)", "Roti (2-3)", "Dal/Lentils", "Rajma/Chole",
            "Green Sabzi (Palak/Methi)", "Mixed Vegetable", "Salad",
            "Curd/Raita", "Fish", "Chicken", "Egg", "Pickle",
            "Buttermilk (Chaas)"
        ], key="lunch")
        
        st.markdown("### 🌅 Evening Snack")
        snack = st.multiselect("Select snacks:", [
            "Fruit (any)", "Milk", "Biscuits", "Roasted Chana",
            "Peanuts", "Murmura/Puffed Rice", "Sprouts",
            "Boiled Egg", "Juice (fresh)", "Dry Fruits"
        ], key="snack")
        
        st.markdown("### 🌙 Dinner")
        dinner = st.multiselect("Select dinner items:", [
            "Roti (2-3)", "Rice", "Dal", "Sabzi", "Khichdi",
            "Milk (1 glass)", "Curd", "Egg", "Soup",
            "Fruit"
        ], key="dinner")
        
        if st.button("🔍 Analyze My Diet", type="primary"):
            all_foods = breakfast + lunch + snack + dinner
            
            st.markdown("---")
            st.subheader("📊 Your Diet Analysis:")
            
            # Check food groups
            protein_foods = ["Dal/Lentils", "Rajma/Chole", "Egg (boiled/omelette)", 
                           "Fish", "Chicken", "Egg", "Milk (1 glass)", "Curd/Yogurt",
                           "Sprouts", "Boiled Egg", "Curd", "Curd/Raita", "Milk"]
            iron_foods = ["Green Sabzi (Palak/Methi)", "Dal/Lentils", "Rajma/Chole",
                        "Dates", "Dry Fruits", "Peanuts", "Sprouts"]
            calcium_foods = ["Milk (1 glass)", "Curd/Yogurt", "Curd/Raita", "Curd",
                           "Buttermilk (Chaas)", "Milk"]
            vitamin_foods = ["Fruit (any)", "Salad", "Green Sabzi (Palak/Methi)",
                           "Mixed Vegetable", "Juice (fresh)", "Banana", "Apple"]
            carb_foods = ["Rice (1 plate)", "Roti (2-3)", "Roti (2)", "Paratha",
                        "Bread & Butter", "Rice", "Poha", "Upma", "Idli", "Dosa"]
            
            has_protein = any(f in all_foods for f in protein_foods)
            has_iron = any(f in all_foods for f in iron_foods)
            has_calcium = any(f in all_foods for f in calcium_foods)
            has_vitamins = any(f in all_foods for f in vitamin_foods)
            has_carbs = any(f in all_foods for f in carb_foods)
            
            # Score
            score = sum([has_protein, has_iron, has_calcium, has_vitamins, has_carbs])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if has_protein:
                    st.success("✅ **Protein:** Good! You ate protein-rich food.")
                else:
                    st.error("❌ **Protein Missing!** Add: Dal, Egg, Milk, Curd, or Sprouts")
                
                if has_iron:
                    st.success("✅ **Iron:** Good! You ate iron-rich food.")
                else:
                    st.error("❌ **Iron Missing!** Add: Green leafy vegetables, Dal, Dry fruits")
                
                if has_calcium:
                    st.success("✅ **Calcium:** Good! You had dairy products.")
                else:
                    st.error("❌ **Calcium Missing!** Add: Milk, Curd, or Buttermilk")
            
            with col2:
                if has_vitamins:
                    st.success("✅ **Vitamins:** Good! You ate fruits/vegetables.")
                else:
                    st.error("❌ **Vitamins Missing!** Add: Any fruit or salad")
                
                if has_carbs:
                    st.success("✅ **Energy Foods:** Good! You had enough carbs.")
                else:
                    st.error("❌ **Energy Missing!** Add: Roti, Rice, or Daliya")
            
            # Overall score
            st.markdown("---")
            if score == 5:
                st.success(f"### 🌟 Diet Score: {score}/5 — EXCELLENT! Perfect diet today!")
                st.balloons()
            elif score >= 3:
                st.warning(f"### 😊 Diet Score: {score}/5 — Good, but can improve!")
            else:
                st.error(f"### 😟 Diet Score: {score}/5 — Please eat more variety!")
    
    with tab2:
        st.subheader("📖 What to Eat During Pregnancy")
        
        st.markdown("""
        ### Daily Requirements:
        
        | Nutrient | What to Eat | How Much |
        |----------|------------|----------|
        | **Protein** | Dal, Egg, Milk, Curd, Sprouts | 2-3 servings daily |
        | **Iron** | Spinach, Methi, Jaggery, Dates | Every meal |
        | **Calcium** | Milk, Curd, Paneer, Ragi | 3 glasses milk daily |
        | **Folic Acid** | Green leafy vegetables, Dal | Daily |
        | **Vitamin C** | Orange, Amla, Lemon, Tomato | With iron-rich food |
        | **Fiber** | Vegetables, Fruits, Whole grains | Every meal |
        | **Water** | Plain water | 8-10 glasses daily |
        
        ### ❌ Foods to AVOID:
        - Raw papaya (can cause contractions)
        - Raw/undercooked eggs or meat
        - Too much caffeine (limit tea to 2 cups)
        - Alcohol (completely avoid)
        - Junk food and excess sugar
        - Unpasteurized milk
        
        ### 💡 Tips:
        - Eat **small, frequent meals** (5-6 times a day)
        - Drink **lemon water with meals** (helps absorb iron)
        - Eat **dates** in third trimester (helps in delivery)
        - Have **warm milk with turmeric** at night
        """)

# ============================================
# PAGE 6: RISK ASSESSMENT (ML MODEL)
# ============================================
elif page == "🔮 Risk Assessment":
    st.title("🔮 AI Risk Assessment")
    st.markdown("### Machine Learning powered pregnancy risk prediction")
    st.markdown("---")
    
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    
    # ---- TRAIN MODEL (happens once) ----
    @st.cache_resource
    def train_model():
        np.random.seed(42)
        n = 1000
        
        # Generate synthetic training data
        ages = np.random.randint(16, 45, n)
        bmis = np.random.uniform(16, 38, n)
        bp_sys = np.random.randint(85, 180, n)
        bp_dia = np.random.randint(55, 120, n)
        hemoglobin = np.random.uniform(5, 16, n)
        blood_sugar = np.random.randint(60, 300, n)
        prev_comp = np.random.choice([0, 1], n, p=[0.7, 0.3])
        week = np.random.randint(1, 42, n)
        
        # Create labels based on medical rules
        risk = []
        for i in range(n):
            score = 0
            if ages[i] < 20 or ages[i] > 35: score += 2
            if bmis[i] < 18.5 or bmis[i] > 30: score += 2
            if bp_sys[i] > 140: score += 3
            if bp_dia[i] > 90: score += 2
            if hemoglobin[i] < 7: score += 3
            elif hemoglobin[i] < 11: score += 1
            if blood_sugar[i] > 200: score += 3
            elif blood_sugar[i] > 140: score += 1
            if prev_comp[i] == 1: score += 2
            
            if score >= 5: risk.append(2)     # High
            elif score >= 2: risk.append(1)   # Medium
            else: risk.append(0)              # Low
        
        X = np.column_stack([ages, bmis, bp_sys, bp_dia, hemoglobin, blood_sugar, prev_comp, week])
        y = np.array(risk)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        model.fit(X, y)
        
        return model
    
    model = train_model()
    
    # ---- USER INPUT ----
    st.subheader("Enter Patient Details:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 15, 50, 25, key="risk_age")
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 55.0, key="risk_weight")
        height = st.number_input("Height (cm)", 120, 200, 155, key="risk_height")
        bp_systolic = st.number_input("BP Systolic", 70, 200, 120, key="risk_bp_sys")
    
    with col2:
        bp_diastolic = st.number_input("BP Diastolic", 40, 130, 80, key="risk_bp_dia")
        hemoglobin = st.number_input("Hemoglobin (g/dL)", 4.0, 18.0, 11.0, key="risk_hb")
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 100, key="risk_sugar")
        pregnancy_week = st.number_input("Pregnancy Week", 1, 42, 20, key="risk_week")
    
    prev_complications = st.selectbox("Previous Complications?", ["No", "Yes"], key="risk_comp")
    
    bmi = weight / ((height/100) ** 2)
    st.info(f"📊 Calculated BMI: {bmi:.1f}")
    
    if st.button("🔮 Predict Risk Level", type="primary"):
        # Prepare input
        input_data = np.array([[
            age, bmi, bp_systolic, bp_diastolic, hemoglobin,
            blood_sugar, 1 if prev_complications == "Yes" else 0, pregnancy_week
        ]])
        
        # Predict
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        st.markdown("---")
        st.subheader("🔍 Risk Assessment Result:")
        
        risk_labels = {0: "LOW RISK 🟢", 1: "MEDIUM RISK 🟡", 2: "HIGH RISK 🔴"}
        
        # Display result prominently
        if prediction == 2:
            st.error(f"## 🔴 {risk_labels[prediction]}")
            st.error("""
            **⚠️ IMMEDIATE ACTION NEEDED:**
            - Visit nearest health center TODAY
            - Do NOT ignore warning signs
            - Call ASHA worker or 108 ambulance
            - Carry all medical records
            """)
        elif prediction == 1:
            st.warning(f"## 🟡 {risk_labels[prediction]}")
            st.warning("""
            **📋 RECOMMENDED ACTIONS:**
            - Schedule a doctor visit within this week
            - Monitor BP and symptoms daily
            - Take all medicines on time
            - Get recommended tests done
            """)
        else:
            st.success(f"## 🟢 {risk_labels[prediction]}")
            st.success("""
            **✅ KEEP IT UP:**
            - Continue your current routine
            - Take medicines and eat well
            - Attend all scheduled checkups
            - Log your health daily in the app
            """)
        
        # Show probability chart
        st.markdown("---")
        st.subheader("📊 Risk Probability Breakdown:")
        
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Low Risk', 'Medium Risk', 'High Risk'],
                y=[probabilities[0]*100, probabilities[1]*100, probabilities[2]*100],
                marker_color=['green', 'orange', 'red'],
                text=[f"{p*100:.1f}%" for p in probabilities],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Risk Probability (%)",
            yaxis_title="Probability %",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show risk factors
        st.subheader("📋 Individual Risk Factors:")
        
        factors = []
        if age < 20: factors.append(("🔴", "Age below 20 - teenage pregnancy risk"))
        elif age > 35: factors.append(("🔴", "Age above 35 - advanced maternal age"))
        else: factors.append(("🟢", "Age is in healthy range"))
        
        if bmi < 18.5: factors.append(("🔴", f"BMI {bmi:.1f} - Underweight"))
        elif bmi > 30: factors.append(("🔴", f"BMI {bmi:.1f} - Obese"))
        elif bmi > 25: factors.append(("🟡", f"BMI {bmi:.1f} - Overweight"))
        else: factors.append(("🟢", f"BMI {bmi:.1f} - Normal weight"))
        
        if bp_systolic > 140: factors.append(("🔴", "Blood Pressure HIGH - risk of preeclampsia"))
        elif bp_systolic > 130: factors.append(("🟡", "Blood Pressure slightly elevated"))
        else: factors.append(("🟢", "Blood Pressure normal"))
        
        if hemoglobin < 7: factors.append(("🔴", "Severe Anemia - needs immediate treatment"))
        elif hemoglobin < 11: factors.append(("🟡", "Mild Anemia - increase iron intake"))
        else: factors.append(("🟢", "Hemoglobin normal"))
        
        if blood_sugar > 200: factors.append(("🔴", "Blood Sugar very high - gestational diabetes likely"))
        elif blood_sugar > 140: factors.append(("🟡", "Blood Sugar elevated - monitor closely"))
        else: factors.append(("🟢", "Blood Sugar normal"))
        
        for icon, text in factors:
            st.write(f"{icon} {text}")

# ============================================
# PAGE 7: GOVERNMENT SCHEMES
# ============================================
elif page == "🏛️ Government Schemes":
    st.title("🏛️ Government Schemes For You")
    st.markdown("### Know your rights! Get the benefits you deserve!")
    st.markdown("---")
    
    # Get user data for eligibility
    user_data = st.session_state.get('user_data', None)
    
    st.subheader("📋 Tell us about yourself:")
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.selectbox("Where do you live?", ["Rural", "Urban"])
        income = st.selectbox("Family Annual Income", [
            "Below ₹1 Lakh (BPL)", "₹1-3 Lakh", "₹3-5 Lakh", "Above ₹5 Lakh"
        ])
        first_baby = st.selectbox("Is this your first baby?", ["Yes", "No"])
    
    with col2:
        delivery_plan = st.selectbox("Where will you deliver?", [
            "Government Hospital", "Private Hospital", "Not decided yet"
        ])
        has_aadhar = st.selectbox("Do you have Aadhar Card?", ["Yes", "No"])
        has_bank = st.selectbox("Do you have Bank Account?", ["Yes", "No"])
    
    if st.button("🔍 Find My Schemes", type="primary"):
        st.markdown("---")
        st.subheader("✅ Schemes You Are Eligible For:")
        
        total_benefit = 0
        
        # SCHEME 1: JSY
        if area == "Rural" or income == "Below ₹1 Lakh (BPL)":
            total_benefit += 1400
            st.markdown("""
            ---
            ### 💰 1. Janani Suraksha Yojana (JSY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹1,400 cash (Rural) / ₹1,000 cash (Urban) |
            | **For** | Institutional delivery (hospital delivery) |
            | **Eligibility** | BPL pregnant women, age 19+ |
            
            **📋 Documents Needed:**
            - ✅ Aadhar Card
            - ✅ BPL Card
            - ✅ MCP (Mother & Child Protection) Card
            - ✅ Bank Account Details
            
            **📝 How to Apply:**
            1. Contact your ASHA worker
            2. Register at nearest government hospital
            3. Deliver at the registered hospital
            4. Money will be transferred to your bank account
            
            **📞 Helpline:** 104 (Health Helpline)
            """)
        
        # SCHEME 2: PMMVY
        if first_baby == "Yes":
            total_benefit += 5000
            st.markdown("""
            ---
            ### 💰 2. Pradhan Mantri Matru Vandana Yojana (PMMVY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹5,000 in 3 installments |
            | **For** | First live birth |
            | **Eligibility** | All pregnant women (first pregnancy), age 19+ |
            
            **💸 Installment Schedule:**
            
            | Installment | Amount | When |
            |-------------|--------|------|
            | 1st | ₹1,000 | After pregnancy registration |
            | 2nd | ₹2,000 | After 6 months of pregnancy |
            | 3rd | ₹2,000 | After child birth & registration |
            
            **📋 Documents Needed:**
            - ✅ Aadhar Card (Mother & Husband)
            - ✅ Bank Passbook
            - ✅ MCP Card
            - ✅ Pregnancy Registration proof
            
            **📝 How to Apply:**
            1. Visit nearest Anganwadi Center
            2. Fill Form 1-A for first installment
            3. Fill Form 1-B for second installment
            4. Fill Form 1-C for third installment
            """)
        
        # SCHEME 3: JSSK
        if delivery_plan == "Government Hospital":
            st.markdown("""
            ---
            ### 🏥 3. Janani Shishu Suraksha Karyakram (JSSK)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | Completely FREE delivery services |
            | **For** | All pregnant women at government hospitals |
            
            **🆓 What You Get FREE:**
            - ✅ Free normal delivery
            - ✅ Free C-section if needed
            - ✅ Free medicines
            - ✅ Free blood transfusion
            - ✅ Free diagnostic tests
            - ✅ Free diet/food during stay
            - ✅ Free transport (home → hospital → home)
            - ✅ Free treatment for sick newborn (up to 30 days)
            
            **⚠️ IMPORTANT:** If any government hospital charges you for these services, 
            you can **COMPLAIN** to the District Health Officer!
            
            **📞 Complaint Helpline:** 104 or 108
            """)
        
        # SCHEME 4: POSHAN
        total_benefit += 0  # Non-cash benefit
        st.markdown("""
        ---
        ### 🥗 4. Poshan Abhiyaan (Nutrition Mission)
        
        | Detail | Information |
        |--------|------------|
        | **Benefit** | Free nutrition supplements & food |
        | **For** | All pregnant & lactating women |
        
        **🍱 What You Get:**
        - Free Take-Home Ration (THR) from Anganwadi
        - Hot cooked meals at Anganwadi Center
        - Free eggs, milk, fruits (in some states)
        - Nutrition counseling
        - Growth monitoring
        
        **📝 How to Get It:**
        1. Visit your nearest Anganwadi Center
        2. Register as a beneficiary
        3. Collect your monthly ration
        """)
        
        # SCHEME 5: Ayushman Bharat
        if income in ["Below ₹1 Lakh (BPL)", "₹1-3 Lakh"]:
            st.markdown("""
            ---
            ### 🏥 5. Ayushman Bharat (PM-JAY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹5 Lakh health insurance per family per year |
            | **For** | Low income families |
            
            **🏥 Coverage:**
            - Hospitalization (including pregnancy complications)
            - Pre & post hospitalization expenses
            - All pre-existing diseases covered
            
            **📝 How to Check Eligibility:**
            1. Visit: https://pmjay.gov.in
            2. Or call: 14555
            3. Or visit nearest CSC (Common Service Center)
            
            **📋 Documents:**
            - Aadhar Card
            - Ration Card
            """)
        
        # Total benefits
        st.markdown("---")
        st.success(f"""
        ### 💰 Total Cash Benefits You Can Get: ₹{total_benefit:,}+
        
        Plus FREE hospital delivery, FREE medicines, FREE nutrition support!
        
        **👉 Contact your ASHA worker TODAY to start the process!**
        """)

# ============================================
# PAGE 8: DASHBOARD
# ============================================
elif page == "📈 Dashboard":
    st.title("📈 Health Analytics Dashboard")
    st.markdown("---")
    
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    
    tab1, tab2, tab3 = st.tabs(["👩 My Health", "📊 Trends", "🗺️ District Data"])
    
    with tab1:
        st.subheader("Your Health Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Week", "24", "+1")
        col2.metric("Weight", "62 kg", "+0.5 kg")
        col3.metric("Risk Level", "LOW ✅")
        col4.metric("Medicine Score", "85%", "+5%")
        
        st.markdown("---")
        
        # Weight progress chart
        weeks_data = list(range(1, 25))
        weight_data = [52, 52, 52.5, 53, 53, 53.5, 54, 54.5, 55, 55.5,
                      56, 56.5, 57, 58, 58.5, 59, 59.5, 60, 60.5, 61,
                      61, 61.5, 62, 62]
        ideal_min = [51, 51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55,
                    55.5, 56, 56.5, 57, 57.5, 58, 58.5, 59, 59.5, 60,
                    60, 60.5, 61, 61]
        ideal_max = [53, 53, 53.5, 54, 54.5, 55, 55.5, 56, 56.5, 57,
                    57.5, 58, 58.5, 59.5, 60, 60.5, 61, 61.5, 62, 62.5,
                    63, 63.5, 64, 64]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_data, y=weight_data, name="Your Weight",
                                line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=weeks_data, y=ideal_min, name="Ideal Min",
                                line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=weeks_data, y=ideal_max, name="Ideal Max",
                                line=dict(color='green', dash='dash')))
        fig.update_layout(title="📈 Weight Progress Over Pregnancy",
                         xaxis_title="Week", yaxis_title="Weight (kg)", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # BP trend
        bp_sys_data = [110, 112, 115, 118, 116, 120, 118, 122, 119, 121,
                      120, 118, 115, 120, 122, 125, 118, 120, 119, 121,
                      123, 120, 118, 120]
        bp_dia_data = [70, 72, 74, 75, 73, 76, 74, 78, 75, 77,
                      76, 74, 72, 76, 78, 80, 74, 76, 75, 77,
                      79, 76, 74, 76]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weeks_data, y=bp_sys_data, name="Systolic",
                                 line=dict(color='red', width=2)))
        fig2.add_trace(go.Scatter(x=weeks_data, y=bp_dia_data, name="Diastolic",
                                 line=dict(color='orange', width=2)))
        fig2.add_hline(y=140, line_dash="dash", line_color="red", 
                      annotation_text="Danger: Systolic > 140")
        fig2.add_hline(y=90, line_dash="dash", line_color="orange",
                      annotation_text="Danger: Diastolic > 90")
        fig2.update_layout(title="🫀 Blood Pressure Trend",
                          xaxis_title="Week", yaxis_title="BP (mmHg)", height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("Weekly Trends")
        
        # Medicine compliance weekly
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        compliance = [100, 100, 67, 100, 100, 100, 33]
        colors = ['green' if c >= 80 else 'orange' if c >= 50 else 'red' for c in compliance]
        
        fig3 = go.Figure(data=[
            go.Bar(x=days, y=compliance, marker_color=colors,
                  text=[f"{c}%" for c in compliance], textposition='auto')
        ])
        fig3.update_layout(title="💊 This Week's Medicine Compliance",
                          yaxis_title="Compliance %", height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Nutrition score weekly
        nutrition_scores = [3, 4, 5, 3, 4, 5, 4]
        fig4 = go.Figure(data=[
            go.Bar(x=days, y=nutrition_scores,
                  marker_color=['red' if n <= 2 else 'orange' if n <= 3 else 'green' for n in nutrition_scores],
                  text=[f"{n}/5" for n in nutrition_scores], textposition='auto')
        ])
        fig4.update_layout(title="🥗 Daily Nutrition Score",
                          yaxis_title="Score (out of 5)", height=400)
        st.plotly_chart(fig4, use_container_width=True)
        
        # Checkup schedule
        st.subheader("🏥 Upcoming Checkups")
        checkups = pd.DataFrame({
            'Checkup': ['ANC-3', 'Growth Scan', 'Blood Test', 'ANC-4'],
            'Due Date': ['2024-03-15', '2024-04-01', '2024-04-10', '2024-05-01'],
            'Status': ['✅ Done', '📅 Upcoming', '📅 Upcoming', '📅 Upcoming'],
            'Tests': ['BP, Weight, Hemoglobin', 'Ultrasound', 'CBC, Sugar', 'Full checkup']
        })
        st.dataframe(checkups, use_container_width=True)
    
    with tab3:
        st.subheader("🗺️ District Overview (Admin View)")
        
        district_data = pd.DataFrame({
            'District': ['Varanasi', 'Lucknow', 'Jhansi', 'Gorakhpur', 'Agra',
                        'Allahabad', 'Kanpur', 'Bareilly', 'Moradabad', 'Meerut'],
            'Total_Users': [150, 200, 80, 120, 180, 95, 160, 70, 85, 140],
            'High_Risk': [12, 8, 15, 20, 10, 14, 9, 11, 13, 7],
            'Medicine_Compliance': [78, 85, 65, 60, 82, 72, 80, 58, 68, 88],
            'Scheme_Claims': [45, 80, 20, 35, 60, 28, 55, 15, 22, 65]
        })
        
        st.dataframe(district_data, use_container_width=True)
        
        # Bar chart
        fig5 = px.bar(district_data, x='District', y=['High_Risk', 'Scheme_Claims'],
                     title="District Comparison", barmode='group', height=400)
        st.plotly_chart(fig5, use_container_width=True)
        
        # Compliance chart
        fig6 = px.bar(district_data, x='District', y='Medicine_Compliance',
                     title="Medicine Compliance by District (%)",
                     color='Medicine_Compliance',
                     color_continuous_scale=['red', 'orange', 'green'],
                     height=400)
        st.plotly_chart(fig6, use_container_width=True)
        
        # Pie chart - Risk distribution
        risk_dist = pd.DataFrame({
            'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
            'Count': [850, 258, 139]
        })
        fig7 = px.pie(risk_dist, values='Count', names='Risk Level',
                     title="Overall Risk Distribution",
                     color='Risk Level',
                     color_discrete_map={'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'})
        st.plotly_chart(fig7, use_container_width=True)

# ============================================
# PAGE 9: PPD SCREENING
# ============================================
elif page == "🧠 PPD Screening":
    st.title("🧠 Postpartum Depression Screening")
    st.markdown("### Edinburgh Postnatal Depression Scale (EPDS)")
    st.markdown("""
    > This screening is for women who have **recently delivered** (within 6 months).
    > Answer honestly — there are no right or wrong answers.
    > Your answers are **confidential**.
    """)
    st.markdown("---")
    
    st.subheader("In the past 7 days:")
    
    q1 = st.radio(
        "1. I have been able to laugh and see the funny side of things:",
        ["As much as I always could (0)", "Not quite so much now (1)", 
         "Definitely not so much now (2)", "Not at all (3)"],
        key="ppd1"
    )
    
    q2 = st.radio(
        "2. I have looked forward with enjoyment to things:",
        ["As much as I ever did (0)", "Rather less than I used to (1)",
         "Definitely less than I used to (2)", "Hardly at all (3)"],
        key="ppd2"
    )
    
    q3 = st.radio(
        "3. I have blamed myself unnecessarily when things went wrong:",
        ["No, never (0)", "Not very often (1)",
         "Yes, some of the time (2)", "Yes, most of the time (3)"],
        key="ppd3"
    )
    
    q4 = st.radio(
        "4. I have been anxious or worried for no good reason:",
        ["No, not at all (0)", "Hardly ever (1)",
         "Yes, sometimes (2)", "Yes, very often (3)"],
        key="ppd4"
    )
    
    q5 = st.radio(
        "5. I have felt scared or panicky for no good reason:",
        ["No, not at all (0)", "No, not much (1)",
         "Yes, sometimes (2)", "Yes, quite a lot (3)"],
        key="ppd5"
    )
    
    q6 = st.radio(
        "6. Things have been getting too much for me:",
        ["No, I have been coping well (0)", "No, mostly I have coped well (1)",
         "Yes, sometimes I haven't coped well (2)", "Yes, most of the time I haven't coped (3)"],
        key="ppd6"
    )
    
    q7 = st.radio(
        "7. I have been so unhappy that I have had difficulty sleeping:",
        ["No, not at all (0)", "Not very often (1)",
         "Yes, sometimes (2)", "Yes, most of the time (3)"],
        key="ppd7"
    )
    
    q8 = st.radio(
        "8. I have felt sad or miserable:",
        ["No, not at all (0)", "Not very often (1)",
         "Yes, quite often (2)", "Yes, most of the time (3)"],
        key="ppd8"
    )
    
    q9 = st.radio(
        "9. I have been so unhappy that I have been crying:",
        ["No, never (0)", "Only occasionally (1)",
         "Yes, quite often (2)", "Yes, most of the time (3)"],
        key="ppd9"
    )
    
    q10 = st.radio(
        "10. The thought of harming myself has occurred to me:",
        ["Never (0)", "Hardly ever (1)",
         "Sometimes (2)", "Yes, quite often (3)"],
        key="ppd10"
    )
    
    if st.button("📊 Get My Score", type="primary"):
        # Extract scores
        answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        scores = []
        for ans in answers:
            # Extract number from parentheses
            score = int(ans.split("(")[1].split(")")[0])
            scores.append(score)
        
        total_score = sum(scores)
        
        st.markdown("---")
        st.subheader(f"Your EPDS Score: {total_score}/30")
        
        # Progress bar
        st.progress(total_score / 30)
        
        # Interpretation
        if total_score <= 8:
            st.success("""
            ### 🟢 Low Risk — Score: {}/30
            
            Your score suggests you are coping well. This is great!
            
            **Advice:**
            - Continue taking care of yourself
            - Talk to family and friends
            - Sleep when the baby sleeps
            - It's okay to ask for help
            """.format(total_score))
        
        elif total_score <= 12:
            st.warning("""
            ### 🟡 Possible Depression — Score: {}/30
            
            Your score suggests you may be experiencing some difficulties.
            
            **Advice:**
            - Talk to someone you trust about how you feel
            - Visit your doctor or ASHA worker
            - You are NOT a bad mother for feeling this way
            - This is common and TREATABLE
            - Consider counseling
            
            **📞 iCall Helpline: 9152987821**
            """.format(total_score))
        
        else:
            st.error("""
            ### 🔴 Likely Depression — Score: {}/30
            
            Your score suggests you may be experiencing significant depression.
            
            **⚠️ PLEASE SEEK HELP:**
            - Talk to your doctor IMMEDIATELY
            - Tell your family how you feel
            - You are NOT alone
            - Postpartum depression is a MEDICAL CONDITION, not weakness
            - With treatment, you WILL feel better
            
            **📞 Emergency Helplines:**
            - Vandrevala Foundation: 1860-2662-345 (24x7)
            - iCall: 9152987821
            - NIMHANS: 080-46110007
            """.format(total_score))
        
        # Question 10 special check
        if scores[9] >= 2:
            st.error("""
            ### ⚠️ URGENT ATTENTION NEEDED
            
            Your response to question 10 (thoughts of self-harm) is concerning.
            
            **PLEASE REACH OUT NOW:**
            - Tell someone you trust IMMEDIATELY
            - Call: 9152987821 (iCall)
            - Call: 1860-2662-345 (Vandrevala Foundation)
            - Go to nearest hospital
            
            **You matter. Your baby needs you. Help is available.**
            """)

# ============================================
# FOOTER
# ============================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Made with ❤️ for Rural India**

Team Members:
- Person 1 (ML Engineer)
- Person 2 (Backend Dev)
- Person 3 (Frontend Dev)  
- Person 4 (Data Analyst)

© 2024 Maternal Health Platform
=======
import streamlit as st
# Add this as the FIRST line of app.py
from database import *

# Page configuration
st.set_page_config(
    page_title="Maternal Health Platform",
    page_icon="🤱",
    layout="wide"
)

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title("🤱 MaternalCare")
st.sidebar.markdown("---")

page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "📝 Register",
    "📊 Health Tracker",
    "💊 Medicine Tracker",
    "🥗 Nutrition Guide",
    "🔮 Risk Assessment",
    "🏛️ Government Schemes",
    "📈 Dashboard",
    "🧠 PPD Screening"
])

# ============================================
# PAGE 1: HOME
# ============================================
if page == "🏠 Home":
    st.title("🤱 Smart Maternal Health Platform")
    st.markdown("### *From Pregnancy to Recovery — Powered by Data*")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👩 Total Users", "1,247")
    col2.metric("🔴 High Risk", "43")
    col3.metric("💊 Medicine Compliance", "78%")
    col4.metric("💰 Schemes Claimed", "₹12.5L")
    
    st.markdown("---")
    
    st.markdown("""
    ## Welcome! 🙏
    
    This app helps pregnant women in rural areas by providing:
    
    - 📊 **Health Tracking** — Log your daily vitals
    - 💊 **Medicine Reminders** — Never miss your supplements
    - 🥗 **Nutrition Guide** — Eat right for your baby
    - 🔮 **Risk Assessment** — AI-powered health predictions
    - 🏛️ **Government Schemes** — Get the money you deserve
    - 📈 **Health Dashboard** — See your progress
    - 🧠 **Mental Health** — Postpartum depression screening
    
    ### How to use:
    1. First, go to **📝 Register** and enter your details
    2. Then use **📊 Health Tracker** daily
    3. Check **💊 Medicine Tracker** every morning
    4. Visit **🏛️ Government Schemes** to see your benefits
    """)

# ============================================
# PAGE 2: REGISTRATION
# ============================================
elif page == "📝 Register":
    st.title("📝 New Registration")
    st.markdown("Enter the pregnant woman's details below:")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👩 Full Name", placeholder="Enter full name")
        age = st.number_input("📅 Age", min_value=15, max_value=50, value=25)
        phone = st.text_input("📱 Phone Number", placeholder="10 digit number")
        village = st.text_input("🏘️ Village", placeholder="Village name")
        district = st.text_input("📍 District", placeholder="District name")
        state = st.selectbox("🗺️ State", [
            "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan",
            "Jharkhand", "Odisha", "Chhattisgarh", "Assam",
            "West Bengal", "Maharashtra", "Other"
        ])
    
    with col2:
        lmp_date = st.date_input("🩸 Last Menstrual Period (LMP) Date")
        height = st.number_input("📏 Height (cm)", min_value=120, max_value=200, value=155)
        weight = st.number_input("⚖️ Current Weight (kg)", min_value=30.0, max_value=150.0, value=55.0)
        blood_group = st.selectbox("🩸 Blood Group", [
            "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Don't know"
        ])
        previous_pregnancies = st.number_input("🤰 Previous Pregnancies", min_value=0, max_value=10, value=0)
        previous_complications = st.selectbox("⚠️ Any Previous Complications?", [
            "No", "High BP", "Diabetes", "Miscarriage", "C-Section", "Other"
        ])
    
    st.markdown("---")
    
    if st.button("✅ Register Now", type="primary"):
        if name and phone:
            # Calculate pregnancy details
            from datetime import date, timedelta
            today = date.today()
            days_pregnant = (today - lmp_date).days
            current_week = days_pregnant // 7
            edd = lmp_date + timedelta(days=280)
            
            # Determine trimester
            if current_week <= 12:
                trimester = "First Trimester"
            elif current_week <= 26:
                trimester = "Second Trimester"
            else:
                trimester = "Third Trimester"
            
            # Calculate BMI
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            # Save to database
            user_id = add_user(
                name, age, phone, village, district, state,
                str(lmp_date), str(edd), current_week, trimester,
                weight, height, round(bmi, 1), blood_group,
                previous_pregnancies, previous_complications
            )
            st.session_state['user_id'] = user_id
            # Save to session state (temporary storage)
            st.session_state['user_data'] = {
                'name': name,
                'age': age,
                'phone': phone,
                'village': village,
                'district': district,
                'state': state,
                'lmp_date': str(lmp_date),
                'edd_date': str(edd),
                'current_week': current_week,
                'trimester': trimester,
                'weight': weight,
                'height': height,
                'bmi': round(bmi, 1),
                'blood_group': blood_group,
                'previous_pregnancies': previous_pregnancies,
                'previous_complications': previous_complications
            }
            
            # Show success
            st.success("✅ Registration Successful!")
            st.balloons()
            
            st.markdown("---")
            st.subheader("📋 Your Pregnancy Summary:")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Week", f"Week {current_week}")
            col2.metric("Trimester", trimester)
            col3.metric("Expected Delivery", str(edd))
            col4.metric("BMI", f"{bmi:.1f}")
            
            # Week-specific advice
            st.markdown("---")
            st.subheader(f"📖 Week {current_week} Guide:")
            
            if current_week <= 4:
                st.info("""
                🌱 **Very Early Pregnancy**
                - Start taking Folic Acid (400mcg) immediately
                - Avoid smoking and alcohol
                - Eat healthy, drink plenty of water
                - Schedule your first doctor visit
                """)
            elif current_week <= 8:
                st.info("""
                🌱 **Weeks 5-8: Baby's organs are forming**
                - Continue Folic Acid
                - Morning sickness is normal
                - Eat small, frequent meals
                - Get blood tests done (hemoglobin, blood group)
                """)
            elif current_week <= 12:
                st.info("""
                🌱 **Weeks 9-12: First trimester ending**
                - Get first ultrasound done
                - Start Iron + Folic Acid tablets
                - Register at nearest PHC/hospital
                - Apply for PMMVY scheme
                """)
            elif current_week <= 16:
                st.info("""
                🌿 **Weeks 13-16: Second trimester begins**
                - Energy levels improving
                - Start gentle walking daily
                - Eat calcium-rich foods (milk, curd)
                - Take Calcium supplements
                """)
            elif current_week <= 20:
                st.info("""
                🌿 **Weeks 17-20: Baby is growing fast**
                - You may feel baby's first movements!
                - Get anomaly scan (ultrasound)
                - Continue all supplements
                - Eat protein-rich food (dal, eggs)
                """)
            elif current_week <= 26:
                st.info("""
                🌿 **Weeks 21-26: Baby is getting bigger**
                - Glucose tolerance test due
                - Watch for swelling in feet
                - Sleep on your left side
                - Stay hydrated
                """)
            elif current_week <= 32:
                st.info("""
                🌳 **Weeks 27-32: Third trimester!**
                - More frequent checkups needed
                - Watch for warning signs (headache, blurred vision)
                - Pack your hospital bag
                - Get TT vaccination
                """)
            elif current_week <= 36:
                st.info("""
                🌳 **Weeks 33-36: Almost there!**
                - Baby is getting into position
                - Hospital bag should be ready
                - Know the signs of labor
                - Keep emergency numbers handy
                """)
            else:
                st.warning("""
                🌳 **Weeks 37-40: Baby can come any day!**
                - Be ready to go to hospital
                - Signs of labor: regular contractions, water breaking
                - Keep documents ready (Aadhar, MCP card)
                - Call ASHA worker when labor starts
                """)
        else:
            st.error("❌ Please enter at least Name and Phone Number!")

# ============================================
# PAGE 3: HEALTH TRACKER
# ============================================
elif page == "📊 Health Tracker":
    st.title("📊 Daily Health Tracker")
    st.markdown("Log your health details every day:")
    st.markdown("---")
    
    # Check if user is registered
    user_data = st.session_state.get('user_data', None)
    if user_data:
        st.success(f"👩 Patient: {user_data['name']} | Week: {user_data['current_week']} | {user_data['trimester']}")
    
    st.subheader("Today's Vitals")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight = st.number_input("⚖️ Weight (kg)", 30.0, 150.0, 55.0, 0.5)
        temperature = st.number_input("🌡️ Temperature (°F)", 95.0, 105.0, 98.6, 0.1)
    
    with col2:
        bp_systolic = st.number_input("🫀 BP Upper (Systolic)", 70, 200, 120)
        bp_diastolic = st.number_input("🫀 BP Lower (Diastolic)", 40, 130, 80)
    
    with col3:
        hemoglobin = st.number_input("🩸 Hemoglobin (g/dL)", 4.0, 18.0, 11.0, 0.1)
        blood_sugar = st.number_input("🍬 Blood Sugar (mg/dL)", 50, 400, 100)
    
    st.markdown("---")
    st.subheader("Symptoms Today")
    
    symptoms = st.multiselect("Select any symptoms you have:", [
        "Headache",
        "Swelling in feet/hands",
        "Bleeding/Spotting",
        "Severe nausea/vomiting",
        "Blurred vision",
        "Chest pain",
        "Reduced baby movement",
        "Fever",
        "Painful urination",
        "Back pain",
        "Difficulty breathing",
        "No symptoms - feeling good! ✅"
    ])
    
    water_intake = st.slider("💧 How many glasses of water today?", 0, 15, 8)
    sleep_hours = st.slider("😴 Hours of sleep last night?", 0, 14, 7)
    mood = st.select_slider("😊 How are you feeling?", 
        options=["Very Sad 😢", "Sad 😔", "Okay 😐", "Good 😊", "Very Happy 😄"])
    
    st.markdown("---")
    
    if st.button("💾 Save Today's Health Log", type="primary"):
        # Save to session state
        if 'health_logs' not in st.session_state:
            st.session_state['health_logs'] = []
        
        from datetime import date
        log = {
            'date': str(date.today()),
            'weight': weight,
            'bp_systolic': bp_systolic,
            'bp_diastolic': bp_diastolic,
            'hemoglobin': hemoglobin,
            'blood_sugar': blood_sugar,
            'temperature': temperature,
            'symptoms': symptoms,
            'water_intake': water_intake,
            'sleep_hours': sleep_hours,
            'mood': mood
        }
        st.session_state['health_logs'].append(log)
                # Save to database
        if 'user_id' in st.session_state:
            add_health_log(
                st.session_state['user_id'],
                weight, bp_systolic, bp_diastolic,
                hemoglobin, blood_sugar, temperature,
                symptoms, water_intake, sleep_hours, mood
            )
        
        st.success("✅ Health log saved successfully!")
        
        # INSTANT HEALTH ALERTS
        st.markdown("### 🔍 Instant Health Analysis:")
        
        alerts = []
        
        # BP Check
        if bp_systolic > 140 or bp_diastolic > 90:
            alerts.append(("🔴 HIGH BLOOD PRESSURE", 
                "BP is above 140/90. This could be a sign of preeclampsia. Visit doctor TODAY!", 
                "error"))
        elif bp_systolic > 130 or bp_diastolic > 85:
            alerts.append(("🟡 SLIGHTLY HIGH BP", 
                "BP is slightly elevated. Rest, reduce salt, monitor daily.", 
                "warning"))
        else:
            alerts.append(("🟢 BP Normal", "Blood pressure is in healthy range.", "success"))
        
        # Hemoglobin Check
        if hemoglobin < 7:
            alerts.append(("🔴 SEVERE ANEMIA", 
                "Hemoglobin is dangerously low! You need immediate medical attention and possibly a blood transfusion.", 
                "error"))
        elif hemoglobin < 11:
            alerts.append(("🟡 MILD ANEMIA", 
                "Hemoglobin is low. Take Iron tablets regularly and eat iron-rich foods (spinach, jaggery, dates).", 
                "warning"))
        else:
            alerts.append(("🟢 Hemoglobin Normal", "Iron levels are good. Keep taking supplements.", "success"))
        
        # Blood Sugar Check
        if blood_sugar > 200:
            alerts.append(("🔴 VERY HIGH BLOOD SUGAR", 
                "This could indicate gestational diabetes. See doctor immediately!", 
                "error"))
        elif blood_sugar > 140:
            alerts.append(("🟡 HIGH BLOOD SUGAR", 
                "Blood sugar is elevated. Reduce sweets, eat more fiber.", 
                "warning"))
        else:
            alerts.append(("🟢 Blood Sugar Normal", "Sugar levels are fine.", "success"))
        
        # Temperature Check
        if temperature > 100.4:
            alerts.append(("🔴 FEVER DETECTED", 
                "You have fever. This needs medical attention during pregnancy!", 
                "error"))
        
        # Symptom Checks
        dangerous_symptoms = ["Bleeding/Spotting", "Blurred vision", "Chest pain", 
                              "Reduced baby movement", "Severe nausea/vomiting"]
        found_dangerous = [s for s in symptoms if s in dangerous_symptoms]
        
        if found_dangerous:
            alerts.append(("🔴 DANGEROUS SYMPTOMS", 
                f"You reported: {', '.join(found_dangerous)}. Visit hospital IMMEDIATELY!", 
                "error"))
        
        # Water intake
        if water_intake < 5:
            alerts.append(("🟡 LOW WATER INTAKE", 
                "Drink at least 8-10 glasses of water daily!", 
                "warning"))
        
        # Display all alerts
        for title, message, alert_type in alerts:
            if alert_type == "error":
                st.error(f"**{title}**: {message}")
            elif alert_type == "warning":
                st.warning(f"**{title}**: {message}")
            else:
                st.success(f"**{title}**: {message}")

# ============================================
# PAGE 4: MEDICINE TRACKER
# ============================================
elif page == "💊 Medicine Tracker":
    st.title("💊 Medicine Schedule & Tracker")
    st.markdown("---")
    
    # Get current week
    user_data = st.session_state.get('user_data', None)
    current_week = user_data['current_week'] if user_data else st.number_input("Enter your pregnancy week:", 1, 42, 12)
    
    # Determine trimester
    if current_week <= 12:
        trimester = "First Trimester"
    elif current_week <= 26:
        trimester = "Second Trimester"
    elif current_week <= 40:
        trimester = "Third Trimester"
    else:
        trimester = "Post Delivery"
    
    st.subheader(f"📅 Week {current_week} — {trimester}")
    st.markdown("---")
    
    # Medicine schedules by trimester
    st.subheader("Your Daily Medicines:")
    
    medicines = []
    
    if current_week <= 12:
        medicines = [
            {"name": "Folic Acid", "dose": "400 mcg (1 tablet)", "time": "🌅 Morning after breakfast", "why": "Prevents brain/spine defects in baby"},
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Prevents anemia, keeps blood healthy"},
        ]
    elif current_week <= 26:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Prevents anemia"},
            {"name": "Calcium", "dose": "500mg (1 tablet)", "time": "🌅 Morning", "why": "Baby's bones need calcium"},
            {"name": "Vitamin D", "dose": "As prescribed", "time": "☀️ With meals", "why": "Helps absorb calcium"},
        ]
    elif current_week <= 40:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "1 tablet", "time": "🌙 Night after dinner", "why": "Continue for blood health"},
            {"name": "Calcium", "dose": "500mg (1 tablet)", "time": "🌅 Morning", "why": "Baby's bones growing rapidly"},
            {"name": "TT Vaccine", "dose": "Check with doctor", "time": "🏥 At health center", "why": "Protects baby from tetanus"},
        ]
    else:
        medicines = [
            {"name": "Iron + Folic Acid (IFA)", "dose": "Continue for 6 months", "time": "🌙 Night", "why": "Recovery from delivery"},
            {"name": "Calcium", "dose": "500mg", "time": "🌅 Morning", "why": "Breastfeeding needs calcium"},
            {"name": "Vitamin A", "dose": "As prescribed", "time": "🏥 At health center", "why": "Postpartum recovery"},
        ]
    
    # Display medicines with checkboxes
    st.markdown("### ✅ Mark what you took today:")
    
    taken_count = 0
    for i, med in enumerate(medicines):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            **{med['name']}**  
            💊 Dose: {med['dose']}  
            ⏰ When: {med['time']}  
            ❓ Why: {med['why']}
            """)
        with col2:
            taken = st.checkbox("Taken ✅", key=f"med_{i}")
            if taken:
                taken_count += 1
        st.markdown("---")
    
    # Compliance score
    if medicines:
        compliance = (taken_count / len(medicines)) * 100
        st.subheader(f"Today's Compliance: {compliance:.0f}%")
        
        if compliance == 100:
            st.success("🌟 Excellent! All medicines taken! Keep it up!")
            st.balloons()
        elif compliance >= 50:
            st.warning("⚠️ You missed some medicines. Try to take them all!")
        else:
            st.error("❌ Please take your medicines! They are very important for your baby's health!")
    
    # Important tips
    st.markdown("---")
    st.subheader("💡 Important Tips:")
    st.info("""
    - Take Iron tablets with **orange juice or lemon water** (Vitamin C helps absorption)
    - Do NOT take Iron tablets with **milk or tea** (they block absorption)
    - Take Iron and Calcium at **different times** (they interfere with each other)
    - If Iron tablets cause constipation, eat **papaya, isabgol, or more vegetables**
    - Never stop medicines without asking doctor
    """)

# ============================================
# PAGE 5: NUTRITION GUIDE
# ============================================
elif page == "🥗 Nutrition Guide":
    st.title("🥗 Nutrition Guide & Food Logger")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📝 Log Today's Food", "📖 Nutrition Guide"])
    
    with tab1:
        st.subheader("What did you eat today?")
        
        st.markdown("### 🌅 Breakfast")
        breakfast = st.multiselect("Select breakfast items:", [
            "Roti (2)", "Paratha", "Poha", "Upma", "Idli", "Dosa",
            "Daliya (Porridge)", "Bread & Butter", "Egg (boiled/omelette)",
            "Milk (1 glass)", "Tea", "Banana", "Apple", "Sprouts",
            "Curd/Yogurt", "Peanuts/Dry fruits"
        ], key="breakfast")
        
        st.markdown("### ☀️ Lunch")
        lunch = st.multiselect("Select lunch items:", [
            "Rice (1 plate)", "Roti (2-3)", "Dal/Lentils", "Rajma/Chole",
            "Green Sabzi (Palak/Methi)", "Mixed Vegetable", "Salad",
            "Curd/Raita", "Fish", "Chicken", "Egg", "Pickle",
            "Buttermilk (Chaas)"
        ], key="lunch")
        
        st.markdown("### 🌅 Evening Snack")
        snack = st.multiselect("Select snacks:", [
            "Fruit (any)", "Milk", "Biscuits", "Roasted Chana",
            "Peanuts", "Murmura/Puffed Rice", "Sprouts",
            "Boiled Egg", "Juice (fresh)", "Dry Fruits"
        ], key="snack")
        
        st.markdown("### 🌙 Dinner")
        dinner = st.multiselect("Select dinner items:", [
            "Roti (2-3)", "Rice", "Dal", "Sabzi", "Khichdi",
            "Milk (1 glass)", "Curd", "Egg", "Soup",
            "Fruit"
        ], key="dinner")
        
        if st.button("🔍 Analyze My Diet", type="primary"):
            all_foods = breakfast + lunch + snack + dinner
            
            st.markdown("---")
            st.subheader("📊 Your Diet Analysis:")
            
            # Check food groups
            protein_foods = ["Dal/Lentils", "Rajma/Chole", "Egg (boiled/omelette)", 
                           "Fish", "Chicken", "Egg", "Milk (1 glass)", "Curd/Yogurt",
                           "Sprouts", "Boiled Egg", "Curd", "Curd/Raita", "Milk"]
            iron_foods = ["Green Sabzi (Palak/Methi)", "Dal/Lentils", "Rajma/Chole",
                        "Dates", "Dry Fruits", "Peanuts", "Sprouts"]
            calcium_foods = ["Milk (1 glass)", "Curd/Yogurt", "Curd/Raita", "Curd",
                           "Buttermilk (Chaas)", "Milk"]
            vitamin_foods = ["Fruit (any)", "Salad", "Green Sabzi (Palak/Methi)",
                           "Mixed Vegetable", "Juice (fresh)", "Banana", "Apple"]
            carb_foods = ["Rice (1 plate)", "Roti (2-3)", "Roti (2)", "Paratha",
                        "Bread & Butter", "Rice", "Poha", "Upma", "Idli", "Dosa"]
            
            has_protein = any(f in all_foods for f in protein_foods)
            has_iron = any(f in all_foods for f in iron_foods)
            has_calcium = any(f in all_foods for f in calcium_foods)
            has_vitamins = any(f in all_foods for f in vitamin_foods)
            has_carbs = any(f in all_foods for f in carb_foods)
            
            # Score
            score = sum([has_protein, has_iron, has_calcium, has_vitamins, has_carbs])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if has_protein:
                    st.success("✅ **Protein:** Good! You ate protein-rich food.")
                else:
                    st.error("❌ **Protein Missing!** Add: Dal, Egg, Milk, Curd, or Sprouts")
                
                if has_iron:
                    st.success("✅ **Iron:** Good! You ate iron-rich food.")
                else:
                    st.error("❌ **Iron Missing!** Add: Green leafy vegetables, Dal, Dry fruits")
                
                if has_calcium:
                    st.success("✅ **Calcium:** Good! You had dairy products.")
                else:
                    st.error("❌ **Calcium Missing!** Add: Milk, Curd, or Buttermilk")
            
            with col2:
                if has_vitamins:
                    st.success("✅ **Vitamins:** Good! You ate fruits/vegetables.")
                else:
                    st.error("❌ **Vitamins Missing!** Add: Any fruit or salad")
                
                if has_carbs:
                    st.success("✅ **Energy Foods:** Good! You had enough carbs.")
                else:
                    st.error("❌ **Energy Missing!** Add: Roti, Rice, or Daliya")
            
            # Overall score
            st.markdown("---")
            if score == 5:
                st.success(f"### 🌟 Diet Score: {score}/5 — EXCELLENT! Perfect diet today!")
                st.balloons()
            elif score >= 3:
                st.warning(f"### 😊 Diet Score: {score}/5 — Good, but can improve!")
            else:
                st.error(f"### 😟 Diet Score: {score}/5 — Please eat more variety!")
    
    with tab2:
        st.subheader("📖 What to Eat During Pregnancy")
        
        st.markdown("""
        ### Daily Requirements:
        
        | Nutrient | What to Eat | How Much |
        |----------|------------|----------|
        | **Protein** | Dal, Egg, Milk, Curd, Sprouts | 2-3 servings daily |
        | **Iron** | Spinach, Methi, Jaggery, Dates | Every meal |
        | **Calcium** | Milk, Curd, Paneer, Ragi | 3 glasses milk daily |
        | **Folic Acid** | Green leafy vegetables, Dal | Daily |
        | **Vitamin C** | Orange, Amla, Lemon, Tomato | With iron-rich food |
        | **Fiber** | Vegetables, Fruits, Whole grains | Every meal |
        | **Water** | Plain water | 8-10 glasses daily |
        
        ### ❌ Foods to AVOID:
        - Raw papaya (can cause contractions)
        - Raw/undercooked eggs or meat
        - Too much caffeine (limit tea to 2 cups)
        - Alcohol (completely avoid)
        - Junk food and excess sugar
        - Unpasteurized milk
        
        ### 💡 Tips:
        - Eat **small, frequent meals** (5-6 times a day)
        - Drink **lemon water with meals** (helps absorb iron)
        - Eat **dates** in third trimester (helps in delivery)
        - Have **warm milk with turmeric** at night
        """)

# ============================================
# PAGE 6: RISK ASSESSMENT (ML MODEL)
# ============================================
elif page == "🔮 Risk Assessment":
    st.title("🔮 AI Risk Assessment")
    st.markdown("### Machine Learning powered pregnancy risk prediction")
    st.markdown("---")
    
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    
    # ---- TRAIN MODEL (happens once) ----
    @st.cache_resource
    def train_model():
        np.random.seed(42)
        n = 1000
        
        # Generate synthetic training data
        ages = np.random.randint(16, 45, n)
        bmis = np.random.uniform(16, 38, n)
        bp_sys = np.random.randint(85, 180, n)
        bp_dia = np.random.randint(55, 120, n)
        hemoglobin = np.random.uniform(5, 16, n)
        blood_sugar = np.random.randint(60, 300, n)
        prev_comp = np.random.choice([0, 1], n, p=[0.7, 0.3])
        week = np.random.randint(1, 42, n)
        
        # Create labels based on medical rules
        risk = []
        for i in range(n):
            score = 0
            if ages[i] < 20 or ages[i] > 35: score += 2
            if bmis[i] < 18.5 or bmis[i] > 30: score += 2
            if bp_sys[i] > 140: score += 3
            if bp_dia[i] > 90: score += 2
            if hemoglobin[i] < 7: score += 3
            elif hemoglobin[i] < 11: score += 1
            if blood_sugar[i] > 200: score += 3
            elif blood_sugar[i] > 140: score += 1
            if prev_comp[i] == 1: score += 2
            
            if score >= 5: risk.append(2)     # High
            elif score >= 2: risk.append(1)   # Medium
            else: risk.append(0)              # Low
        
        X = np.column_stack([ages, bmis, bp_sys, bp_dia, hemoglobin, blood_sugar, prev_comp, week])
        y = np.array(risk)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        model.fit(X, y)
        
        return model
    
    model = train_model()
    
    # ---- USER INPUT ----
    st.subheader("Enter Patient Details:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 15, 50, 25, key="risk_age")
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 55.0, key="risk_weight")
        height = st.number_input("Height (cm)", 120, 200, 155, key="risk_height")
        bp_systolic = st.number_input("BP Systolic", 70, 200, 120, key="risk_bp_sys")
    
    with col2:
        bp_diastolic = st.number_input("BP Diastolic", 40, 130, 80, key="risk_bp_dia")
        hemoglobin = st.number_input("Hemoglobin (g/dL)", 4.0, 18.0, 11.0, key="risk_hb")
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 100, key="risk_sugar")
        pregnancy_week = st.number_input("Pregnancy Week", 1, 42, 20, key="risk_week")
    
    prev_complications = st.selectbox("Previous Complications?", ["No", "Yes"], key="risk_comp")
    
    bmi = weight / ((height/100) ** 2)
    st.info(f"📊 Calculated BMI: {bmi:.1f}")
    
    if st.button("🔮 Predict Risk Level", type="primary"):
        # Prepare input
        input_data = np.array([[
            age, bmi, bp_systolic, bp_diastolic, hemoglobin,
            blood_sugar, 1 if prev_complications == "Yes" else 0, pregnancy_week
        ]])
        
        # Predict
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        st.markdown("---")
        st.subheader("🔍 Risk Assessment Result:")
        
        risk_labels = {0: "LOW RISK 🟢", 1: "MEDIUM RISK 🟡", 2: "HIGH RISK 🔴"}
        
        # Display result prominently
        if prediction == 2:
            st.error(f"## 🔴 {risk_labels[prediction]}")
            st.error("""
            **⚠️ IMMEDIATE ACTION NEEDED:**
            - Visit nearest health center TODAY
            - Do NOT ignore warning signs
            - Call ASHA worker or 108 ambulance
            - Carry all medical records
            """)
        elif prediction == 1:
            st.warning(f"## 🟡 {risk_labels[prediction]}")
            st.warning("""
            **📋 RECOMMENDED ACTIONS:**
            - Schedule a doctor visit within this week
            - Monitor BP and symptoms daily
            - Take all medicines on time
            - Get recommended tests done
            """)
        else:
            st.success(f"## 🟢 {risk_labels[prediction]}")
            st.success("""
            **✅ KEEP IT UP:**
            - Continue your current routine
            - Take medicines and eat well
            - Attend all scheduled checkups
            - Log your health daily in the app
            """)
        
        # Show probability chart
        st.markdown("---")
        st.subheader("📊 Risk Probability Breakdown:")
        
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Low Risk', 'Medium Risk', 'High Risk'],
                y=[probabilities[0]*100, probabilities[1]*100, probabilities[2]*100],
                marker_color=['green', 'orange', 'red'],
                text=[f"{p*100:.1f}%" for p in probabilities],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Risk Probability (%)",
            yaxis_title="Probability %",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show risk factors
        st.subheader("📋 Individual Risk Factors:")
        
        factors = []
        if age < 20: factors.append(("🔴", "Age below 20 - teenage pregnancy risk"))
        elif age > 35: factors.append(("🔴", "Age above 35 - advanced maternal age"))
        else: factors.append(("🟢", "Age is in healthy range"))
        
        if bmi < 18.5: factors.append(("🔴", f"BMI {bmi:.1f} - Underweight"))
        elif bmi > 30: factors.append(("🔴", f"BMI {bmi:.1f} - Obese"))
        elif bmi > 25: factors.append(("🟡", f"BMI {bmi:.1f} - Overweight"))
        else: factors.append(("🟢", f"BMI {bmi:.1f} - Normal weight"))
        
        if bp_systolic > 140: factors.append(("🔴", "Blood Pressure HIGH - risk of preeclampsia"))
        elif bp_systolic > 130: factors.append(("🟡", "Blood Pressure slightly elevated"))
        else: factors.append(("🟢", "Blood Pressure normal"))
        
        if hemoglobin < 7: factors.append(("🔴", "Severe Anemia - needs immediate treatment"))
        elif hemoglobin < 11: factors.append(("🟡", "Mild Anemia - increase iron intake"))
        else: factors.append(("🟢", "Hemoglobin normal"))
        
        if blood_sugar > 200: factors.append(("🔴", "Blood Sugar very high - gestational diabetes likely"))
        elif blood_sugar > 140: factors.append(("🟡", "Blood Sugar elevated - monitor closely"))
        else: factors.append(("🟢", "Blood Sugar normal"))
        
        for icon, text in factors:
            st.write(f"{icon} {text}")

# ============================================
# PAGE 7: GOVERNMENT SCHEMES
# ============================================
elif page == "🏛️ Government Schemes":
    st.title("🏛️ Government Schemes For You")
    st.markdown("### Know your rights! Get the benefits you deserve!")
    st.markdown("---")
    
    # Get user data for eligibility
    user_data = st.session_state.get('user_data', None)
    
    st.subheader("📋 Tell us about yourself:")
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.selectbox("Where do you live?", ["Rural", "Urban"])
        income = st.selectbox("Family Annual Income", [
            "Below ₹1 Lakh (BPL)", "₹1-3 Lakh", "₹3-5 Lakh", "Above ₹5 Lakh"
        ])
        first_baby = st.selectbox("Is this your first baby?", ["Yes", "No"])
    
    with col2:
        delivery_plan = st.selectbox("Where will you deliver?", [
            "Government Hospital", "Private Hospital", "Not decided yet"
        ])
        has_aadhar = st.selectbox("Do you have Aadhar Card?", ["Yes", "No"])
        has_bank = st.selectbox("Do you have Bank Account?", ["Yes", "No"])
    
    if st.button("🔍 Find My Schemes", type="primary"):
        st.markdown("---")
        st.subheader("✅ Schemes You Are Eligible For:")
        
        total_benefit = 0
        
        # SCHEME 1: JSY
        if area == "Rural" or income == "Below ₹1 Lakh (BPL)":
            total_benefit += 1400
            st.markdown("""
            ---
            ### 💰 1. Janani Suraksha Yojana (JSY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹1,400 cash (Rural) / ₹1,000 cash (Urban) |
            | **For** | Institutional delivery (hospital delivery) |
            | **Eligibility** | BPL pregnant women, age 19+ |
            
            **📋 Documents Needed:**
            - ✅ Aadhar Card
            - ✅ BPL Card
            - ✅ MCP (Mother & Child Protection) Card
            - ✅ Bank Account Details
            
            **📝 How to Apply:**
            1. Contact your ASHA worker
            2. Register at nearest government hospital
            3. Deliver at the registered hospital
            4. Money will be transferred to your bank account
            
            **📞 Helpline:** 104 (Health Helpline)
            """)
        
        # SCHEME 2: PMMVY
        if first_baby == "Yes":
            total_benefit += 5000
            st.markdown("""
            ---
            ### 💰 2. Pradhan Mantri Matru Vandana Yojana (PMMVY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹5,000 in 3 installments |
            | **For** | First live birth |
            | **Eligibility** | All pregnant women (first pregnancy), age 19+ |
            
            **💸 Installment Schedule:**
            
            | Installment | Amount | When |
            |-------------|--------|------|
            | 1st | ₹1,000 | After pregnancy registration |
            | 2nd | ₹2,000 | After 6 months of pregnancy |
            | 3rd | ₹2,000 | After child birth & registration |
            
            **📋 Documents Needed:**
            - ✅ Aadhar Card (Mother & Husband)
            - ✅ Bank Passbook
            - ✅ MCP Card
            - ✅ Pregnancy Registration proof
            
            **📝 How to Apply:**
            1. Visit nearest Anganwadi Center
            2. Fill Form 1-A for first installment
            3. Fill Form 1-B for second installment
            4. Fill Form 1-C for third installment
            """)
        
        # SCHEME 3: JSSK
        if delivery_plan == "Government Hospital":
            st.markdown("""
            ---
            ### 🏥 3. Janani Shishu Suraksha Karyakram (JSSK)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | Completely FREE delivery services |
            | **For** | All pregnant women at government hospitals |
            
            **🆓 What You Get FREE:**
            - ✅ Free normal delivery
            - ✅ Free C-section if needed
            - ✅ Free medicines
            - ✅ Free blood transfusion
            - ✅ Free diagnostic tests
            - ✅ Free diet/food during stay
            - ✅ Free transport (home → hospital → home)
            - ✅ Free treatment for sick newborn (up to 30 days)
            
            **⚠️ IMPORTANT:** If any government hospital charges you for these services, 
            you can **COMPLAIN** to the District Health Officer!
            
            **📞 Complaint Helpline:** 104 or 108
            """)
        
        # SCHEME 4: POSHAN
        total_benefit += 0  # Non-cash benefit
        st.markdown("""
        ---
        ### 🥗 4. Poshan Abhiyaan (Nutrition Mission)
        
        | Detail | Information |
        |--------|------------|
        | **Benefit** | Free nutrition supplements & food |
        | **For** | All pregnant & lactating women |
        
        **🍱 What You Get:**
        - Free Take-Home Ration (THR) from Anganwadi
        - Hot cooked meals at Anganwadi Center
        - Free eggs, milk, fruits (in some states)
        - Nutrition counseling
        - Growth monitoring
        
        **📝 How to Get It:**
        1. Visit your nearest Anganwadi Center
        2. Register as a beneficiary
        3. Collect your monthly ration
        """)
        
        # SCHEME 5: Ayushman Bharat
        if income in ["Below ₹1 Lakh (BPL)", "₹1-3 Lakh"]:
            st.markdown("""
            ---
            ### 🏥 5. Ayushman Bharat (PM-JAY)
            
            | Detail | Information |
            |--------|------------|
            | **Benefit** | ₹5 Lakh health insurance per family per year |
            | **For** | Low income families |
            
            **🏥 Coverage:**
            - Hospitalization (including pregnancy complications)
            - Pre & post hospitalization expenses
            - All pre-existing diseases covered
            
            **📝 How to Check Eligibility:**
            1. Visit: https://pmjay.gov.in
            2. Or call: 14555
            3. Or visit nearest CSC (Common Service Center)
            
            **📋 Documents:**
            - Aadhar Card
            - Ration Card
            """)
        
        # Total benefits
        st.markdown("---")
        st.success(f"""
        ### 💰 Total Cash Benefits You Can Get: ₹{total_benefit:,}+
        
        Plus FREE hospital delivery, FREE medicines, FREE nutrition support!
        
        **👉 Contact your ASHA worker TODAY to start the process!**
        """)

# ============================================
# PAGE 8: DASHBOARD
# ============================================
elif page == "📈 Dashboard":
    st.title("📈 Health Analytics Dashboard")
    st.markdown("---")
    
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    
    tab1, tab2, tab3 = st.tabs(["👩 My Health", "📊 Trends", "🗺️ District Data"])
    
    with tab1:
        st.subheader("Your Health Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Week", "24", "+1")
        col2.metric("Weight", "62 kg", "+0.5 kg")
        col3.metric("Risk Level", "LOW ✅")
        col4.metric("Medicine Score", "85%", "+5%")
        
        st.markdown("---")
        
        # Weight progress chart
        weeks_data = list(range(1, 25))
        weight_data = [52, 52, 52.5, 53, 53, 53.5, 54, 54.5, 55, 55.5,
                      56, 56.5, 57, 58, 58.5, 59, 59.5, 60, 60.5, 61,
                      61, 61.5, 62, 62]
        ideal_min = [51, 51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55,
                    55.5, 56, 56.5, 57, 57.5, 58, 58.5, 59, 59.5, 60,
                    60, 60.5, 61, 61]
        ideal_max = [53, 53, 53.5, 54, 54.5, 55, 55.5, 56, 56.5, 57,
                    57.5, 58, 58.5, 59.5, 60, 60.5, 61, 61.5, 62, 62.5,
                    63, 63.5, 64, 64]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_data, y=weight_data, name="Your Weight",
                                line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=weeks_data, y=ideal_min, name="Ideal Min",
                                line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=weeks_data, y=ideal_max, name="Ideal Max",
                                line=dict(color='green', dash='dash')))
        fig.update_layout(title="📈 Weight Progress Over Pregnancy",
                         xaxis_title="Week", yaxis_title="Weight (kg)", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # BP trend
        bp_sys_data = [110, 112, 115, 118, 116, 120, 118, 122, 119, 121,
                      120, 118, 115, 120, 122, 125, 118, 120, 119, 121,
                      123, 120, 118, 120]
        bp_dia_data = [70, 72, 74, 75, 73, 76, 74, 78, 75, 77,
                      76, 74, 72, 76, 78, 80, 74, 76, 75, 77,
                      79, 76, 74, 76]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weeks_data, y=bp_sys_data, name="Systolic",
                                 line=dict(color='red', width=2)))
        fig2.add_trace(go.Scatter(x=weeks_data, y=bp_dia_data, name="Diastolic",
                                 line=dict(color='orange', width=2)))
        fig2.add_hline(y=140, line_dash="dash", line_color="red", 
                      annotation_text="Danger: Systolic > 140")
        fig2.add_hline(y=90, line_dash="dash", line_color="orange",
                      annotation_text="Danger: Diastolic > 90")
        fig2.update_layout(title="🫀 Blood Pressure Trend",
                          xaxis_title="Week", yaxis_title="BP (mmHg)", height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("Weekly Trends")
        
        # Medicine compliance weekly
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        compliance = [100, 100, 67, 100, 100, 100, 33]
        colors = ['green' if c >= 80 else 'orange' if c >= 50 else 'red' for c in compliance]
        
        fig3 = go.Figure(data=[
            go.Bar(x=days, y=compliance, marker_color=colors,
                  text=[f"{c}%" for c in compliance], textposition='auto')
        ])
        fig3.update_layout(title="💊 This Week's Medicine Compliance",
                          yaxis_title="Compliance %", height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Nutrition score weekly
        nutrition_scores = [3, 4, 5, 3, 4, 5, 4]
        fig4 = go.Figure(data=[
            go.Bar(x=days, y=nutrition_scores,
                  marker_color=['red' if n <= 2 else 'orange' if n <= 3 else 'green' for n in nutrition_scores],
                  text=[f"{n}/5" for n in nutrition_scores], textposition='auto')
        ])
        fig4.update_layout(title="🥗 Daily Nutrition Score",
                          yaxis_title="Score (out of 5)", height=400)
        st.plotly_chart(fig4, use_container_width=True)
        
        # Checkup schedule
        st.subheader("🏥 Upcoming Checkups")
        checkups = pd.DataFrame({
            'Checkup': ['ANC-3', 'Growth Scan', 'Blood Test', 'ANC-4'],
            'Due Date': ['2024-03-15', '2024-04-01', '2024-04-10', '2024-05-01'],
            'Status': ['✅ Done', '📅 Upcoming', '📅 Upcoming', '📅 Upcoming'],
            'Tests': ['BP, Weight, Hemoglobin', 'Ultrasound', 'CBC, Sugar', 'Full checkup']
        })
        st.dataframe(checkups, use_container_width=True)
    
    with tab3:
        st.subheader("🗺️ District Overview (Admin View)")
        
        district_data = pd.DataFrame({
            'District': ['Varanasi', 'Lucknow', 'Jhansi', 'Gorakhpur', 'Agra',
                        'Allahabad', 'Kanpur', 'Bareilly', 'Moradabad', 'Meerut'],
            'Total_Users': [150, 200, 80, 120, 180, 95, 160, 70, 85, 140],
            'High_Risk': [12, 8, 15, 20, 10, 14, 9, 11, 13, 7],
            'Medicine_Compliance': [78, 85, 65, 60, 82, 72, 80, 58, 68, 88],
            'Scheme_Claims': [45, 80, 20, 35, 60, 28, 55, 15, 22, 65]
        })
        
        st.dataframe(district_data, use_container_width=True)
        
        # Bar chart
        fig5 = px.bar(district_data, x='District', y=['High_Risk', 'Scheme_Claims'],
                     title="District Comparison", barmode='group', height=400)
        st.plotly_chart(fig5, use_container_width=True)
        
        # Compliance chart
        fig6 = px.bar(district_data, x='District', y='Medicine_Compliance',
                     title="Medicine Compliance by District (%)",
                     color='Medicine_Compliance',
                     color_continuous_scale=['red', 'orange', 'green'],
                     height=400)
        st.plotly_chart(fig6, use_container_width=True)
        
        # Pie chart - Risk distribution
        risk_dist = pd.DataFrame({
            'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
            'Count': [850, 258, 139]
        })
        fig7 = px.pie(risk_dist, values='Count', names='Risk Level',
                     title="Overall Risk Distribution",
                     color='Risk Level',
                     color_discrete_map={'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'})
        st.plotly_chart(fig7, use_container_width=True)

# ============================================
# PAGE 9: PPD SCREENING
# ============================================
elif page == "🧠 PPD Screening":
    st.title("🧠 Postpartum Depression Screening")
    st.markdown("### Edinburgh Postnatal Depression Scale (EPDS)")
    st.markdown("""
    > This screening is for women who have **recently delivered** (within 6 months).
    > Answer honestly — there are no right or wrong answers.
    > Your answers are **confidential**.
    """)
    st.markdown("---")
    
    st.subheader("In the past 7 days:")
    
    q1 = st.radio(
        "1. I have been able to laugh and see the funny side of things:",
        ["As much as I always could (0)", "Not quite so much now (1)", 
         "Definitely not so much now (2)", "Not at all (3)"],
        key="ppd1"
    )
    
    q2 = st.radio(
        "2. I have looked forward with enjoyment to things:",
        ["As much as I ever did (0)", "Rather less than I used to (1)",
         "Definitely less than I used to (2)", "Hardly at all (3)"],
        key="ppd2"
    )
    
    q3 = st.radio(
        "3. I have blamed myself unnecessarily when things went wrong:",
        ["No, never (0)", "Not very often (1)",
         "Yes, some of the time (2)", "Yes, most of the time (3)"],
        key="ppd3"
    )
    
    q4 = st.radio(
        "4. I have been anxious or worried for no good reason:",
        ["No, not at all (0)", "Hardly ever (1)",
         "Yes, sometimes (2)", "Yes, very often (3)"],
        key="ppd4"
    )
    
    q5 = st.radio(
        "5. I have felt scared or panicky for no good reason:",
        ["No, not at all (0)", "No, not much (1)",
         "Yes, sometimes (2)", "Yes, quite a lot (3)"],
        key="ppd5"
    )
    
    q6 = st.radio(
        "6. Things have been getting too much for me:",
        ["No, I have been coping well (0)", "No, mostly I have coped well (1)",
         "Yes, sometimes I haven't coped well (2)", "Yes, most of the time I haven't coped (3)"],
        key="ppd6"
    )
    
    q7 = st.radio(
        "7. I have been so unhappy that I have had difficulty sleeping:",
        ["No, not at all (0)", "Not very often (1)",
         "Yes, sometimes (2)", "Yes, most of the time (3)"],
        key="ppd7"
    )
    
    q8 = st.radio(
        "8. I have felt sad or miserable:",
        ["No, not at all (0)", "Not very often (1)",
         "Yes, quite often (2)", "Yes, most of the time (3)"],
        key="ppd8"
    )
    
    q9 = st.radio(
        "9. I have been so unhappy that I have been crying:",
        ["No, never (0)", "Only occasionally (1)",
         "Yes, quite often (2)", "Yes, most of the time (3)"],
        key="ppd9"
    )
    
    q10 = st.radio(
        "10. The thought of harming myself has occurred to me:",
        ["Never (0)", "Hardly ever (1)",
         "Sometimes (2)", "Yes, quite often (3)"],
        key="ppd10"
    )
    
    if st.button("📊 Get My Score", type="primary"):
        # Extract scores
        answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        scores = []
        for ans in answers:
            # Extract number from parentheses
            score = int(ans.split("(")[1].split(")")[0])
            scores.append(score)
        
        total_score = sum(scores)
        
        st.markdown("---")
        st.subheader(f"Your EPDS Score: {total_score}/30")
        
        # Progress bar
        st.progress(total_score / 30)
        
        # Interpretation
        if total_score <= 8:
            st.success("""
            ### 🟢 Low Risk — Score: {}/30
            
            Your score suggests you are coping well. This is great!
            
            **Advice:**
            - Continue taking care of yourself
            - Talk to family and friends
            - Sleep when the baby sleeps
            - It's okay to ask for help
            """.format(total_score))
        
        elif total_score <= 12:
            st.warning("""
            ### 🟡 Possible Depression — Score: {}/30
            
            Your score suggests you may be experiencing some difficulties.
            
            **Advice:**
            - Talk to someone you trust about how you feel
            - Visit your doctor or ASHA worker
            - You are NOT a bad mother for feeling this way
            - This is common and TREATABLE
            - Consider counseling
            
            **📞 iCall Helpline: 9152987821**
            """.format(total_score))
        
        else:
            st.error("""
            ### 🔴 Likely Depression — Score: {}/30
            
            Your score suggests you may be experiencing significant depression.
            
            **⚠️ PLEASE SEEK HELP:**
            - Talk to your doctor IMMEDIATELY
            - Tell your family how you feel
            - You are NOT alone
            - Postpartum depression is a MEDICAL CONDITION, not weakness
            - With treatment, you WILL feel better
            
            **📞 Emergency Helplines:**
            - Vandrevala Foundation: 1860-2662-345 (24x7)
            - iCall: 9152987821
            - NIMHANS: 080-46110007
            """.format(total_score))
        
        # Question 10 special check
        if scores[9] >= 2:
            st.error("""
            ### ⚠️ URGENT ATTENTION NEEDED
            
            Your response to question 10 (thoughts of self-harm) is concerning.
            
            **PLEASE REACH OUT NOW:**
            - Tell someone you trust IMMEDIATELY
            - Call: 9152987821 (iCall)
            - Call: 1860-2662-345 (Vandrevala Foundation)
            - Go to nearest hospital
            
            **You matter. Your baby needs you. Help is available.**
            """)

# ============================================
# FOOTER
# ============================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Made with ❤️ for Rural India**

Team Members:
- Person 1 (ML Engineer)
- Person 2 (Backend Dev)
- Person 3 (Frontend Dev)  
- Person 4 (Data Analyst)

© 2024 Maternal Health Platform
