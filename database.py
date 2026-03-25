import sqlite3
from datetime import datetime

# ============================================
# CREATE ALL TABLES
# ============================================
def create_tables():
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            phone TEXT,
            village TEXT,
            district TEXT,
            state TEXT,
            lmp_date TEXT,
            edd_date TEXT,
            current_week INTEGER,
            trimester TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            blood_group TEXT,
            previous_pregnancies INTEGER,
            previous_complications TEXT,
            registered_on TEXT
        )
    ''')
    
    # Health logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_date TEXT,
            weight REAL,
            bp_systolic INTEGER,
            bp_diastolic INTEGER,
            hemoglobin REAL,
            blood_sugar INTEGER,
            temperature REAL,
            symptoms TEXT,
            water_intake INTEGER,
            sleep_hours INTEGER,
            mood TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Medicine logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS medicine_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_date TEXT,
            medicine_name TEXT,
            taken INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Nutrition logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_date TEXT,
            breakfast TEXT,
            lunch TEXT,
            snack TEXT,
            dinner TEXT,
            diet_score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Risk assessment logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS risk_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            assessed_on TEXT,
            risk_level TEXT,
            risk_score REAL,
            factors TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # PPD screening logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS ppd_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            screened_on TEXT,
            total_score INTEGER,
            risk_level TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("All tables created!")


# ============================================
# ADD NEW USER
# ============================================
def add_user(name, age, phone, village, district, state,
             lmp_date, edd_date, current_week, trimester,
             weight, height, bmi, blood_group,
             previous_pregnancies, previous_complications):
    
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO users 
        (name, age, phone, village, district, state,
         lmp_date, edd_date, current_week, trimester,
         weight, height, bmi, blood_group,
         previous_pregnancies, previous_complications, registered_on)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, phone, village, district, state,
          lmp_date, edd_date, current_week, trimester,
          weight, height, bmi, blood_group,
          previous_pregnancies, previous_complications,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    
    return user_id


# ============================================
# ADD HEALTH LOG
# ============================================
def add_health_log(user_id, weight, bp_sys, bp_dia, 
                   hemoglobin, blood_sugar, temperature,
                   symptoms, water_intake, sleep_hours, mood):
    
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO health_logs
        (user_id, log_date, weight, bp_systolic, bp_diastolic,
         hemoglobin, blood_sugar, temperature, symptoms,
         water_intake, sleep_hours, mood)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d"),
          weight, bp_sys, bp_dia, hemoglobin, blood_sugar,
          temperature, str(symptoms), water_intake, sleep_hours, mood))
    
    conn.commit()
    conn.close()


# ============================================
# ADD MEDICINE LOG
# ============================================
def add_medicine_log(user_id, medicine_name, taken):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO medicine_logs
        (user_id, log_date, medicine_name, taken)
        VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d"),
          medicine_name, 1 if taken else 0))
    
    conn.commit()
    conn.close()


# ============================================
# ADD NUTRITION LOG
# ============================================
def add_nutrition_log(user_id, breakfast, lunch, snack, dinner, score):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO nutrition_logs
        (user_id, log_date, breakfast, lunch, snack, dinner, diet_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d"),
          str(breakfast), str(lunch), str(snack), str(dinner), score))
    
    conn.commit()
    conn.close()


# ============================================
# ADD RISK LOG
# ============================================
def add_risk_log(user_id, risk_level, risk_score, factors):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO risk_logs
        (user_id, assessed_on, risk_level, risk_score, factors)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d"),
          risk_level, risk_score, str(factors)))
    
    conn.commit()
    conn.close()


# ============================================
# ADD PPD LOG
# ============================================
def add_ppd_log(user_id, total_score, risk_level):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO ppd_logs
        (user_id, screened_on, total_score, risk_level)
        VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d"),
          total_score, risk_level))
    
    conn.commit()
    conn.close()


# ============================================
# GET ALL USERS
# ============================================
def get_all_users():
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users


# ============================================
# GET USER BY ID
# ============================================
def get_user(user_id):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user


# ============================================
# GET HEALTH LOGS FOR USER
# ============================================
def get_health_logs(user_id):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM health_logs WHERE user_id = ? ORDER BY log_date', (user_id,))
    logs = c.fetchall()
    conn.close()
    return logs


# ============================================
# GET MEDICINE LOGS FOR USER
# ============================================
def get_medicine_logs(user_id):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM medicine_logs WHERE user_id = ? ORDER BY log_date', (user_id,))
    logs = c.fetchall()
    conn.close()
    return logs


# ============================================
# GET NUTRITION LOGS FOR USER
# ============================================
def get_nutrition_logs(user_id):
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM nutrition_logs WHERE user_id = ? ORDER BY log_date', (user_id,))
    logs = c.fetchall()
    conn.close()
    return logs


# ============================================
# GET TOTAL COUNTS (FOR DASHBOARD)
# ============================================
def get_dashboard_stats():
    conn = sqlite3.connect('maternal_health.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM health_logs')
    total_logs = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM risk_logs WHERE risk_level = 'HIGH RISK'")
    high_risk = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_logs': total_logs,
        'high_risk': high_risk
    }


# ============================================
# CREATE TABLES WHEN FILE RUNS
# ============================================
create_tables()