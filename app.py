import re
from flask import Flask, request, jsonify, session, render_template, abort, redirect
import os

from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from datetime import datetime, timedelta, date
import random
from flask_mail import Mail, Message

from flask_cors import CORS

#Include your headers here
# ==========================================================
# ✅ APP INIT
# ==========================================================
app = Flask(__name__, template_folder='ResidueSafeWeb', static_folder='ResidueSafeWeb', static_url_path='')
CORS(app) # Allow cross-origin requests from the browser
app.secret_key = "supersecretkey"

# ==========================================================
# ✅ MAIL CONFIG
# ==========================================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'gvennela1105@gmail.com'
app.config['MAIL_PASSWORD'] = 'dufatkzheqttmqwo'
mail = Mail(app)

# ==========================================================
# ✅ DATABASE CONNECTION (DB NAME: animal_medicines)
# ==========================================================
def get_db_connection():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="animal_medicines",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("❌ Error while connecting to MySQL:", e)
        return None

# ==========================================================
# ✅ SAFE INT HELPER
# ==========================================================
def _to_int(v, default=None):
    try:
        return int(v)
    except:
        return default

# ==========================================================
# ✅ PASSWORD VALIDATOR
# ==========================================================
def validate_password(password):
    missing = []
    if len(password) < 6:
        missing.append("at least 6 characters")
    if not any(c.islower() for c in password):
        missing.append("one lowercase letter")
    if not any(c.isupper() for c in password):
        missing.append("one uppercase letter")
    if not any(c.isdigit() for c in password):
        missing.append("one numerical digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        missing.append("one special character")
    return missing

# ==========================================================
# ✅ BASIC TEST ROUTE
# ==========================================================
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "success", "message": "animal_medicines backend running ✅"}), 200

# =========================================================
# RENDORS
# ==========================================================

@app.route("/index", methods=["GET"])
def index_view():
    return render_template("index.html")

@app.route("/role", methods=["GET"])
def role_view():
    return render_template("role.html")

@app.route("/login", methods=["GET"])
def login_view():
    return render_template("login.html")

@app.route("/signup", methods=["GET"])
def signup_view():
    return render_template("signup.html")

@app.route("/about", methods=["GET"])
def about_view():
    return render_template("about.html")

@app.route("/add_animals", methods=["GET"])
def add_animals_view():
    return render_template("add_animals.html")

@app.route("/add_new_animal", methods=["GET"])
def add_new_animal_view():
    return render_template("add_new_animal.html")

@app.route("/add_treatment", methods=["GET"])
def add_treatment_view():
    return render_template("add_treatment.html")

@app.route("/admin_change_password", methods=["GET"])
def admin_change_password_view():
    return render_template("admin_change_password.html")

@app.route("/admin_dashboard", methods=["GET"])
def admin_dashboard_view():
    return render_template("admin_dashboard.html")

@app.route("/admin_drugs", methods=["GET"])
def admin_drugs_view():
    return render_template("admin_drugs.html")

@app.route("/admin_edit_profile", methods=["GET"])
def admin_edit_profile_view():
    return render_template("admin_edit_profile.html")

@app.route("/admin_farm_details", methods=["GET"])
def admin_farm_details_view():
    return render_template("admin_farm_details.html")

@app.route("/admin_forgot_password", methods=["GET"])
def admin_forgot_password_view():
    return render_template("admin_forgot_password.html")

@app.route("/admin_login", methods=["GET"])
def admin_login_view():
    return render_template("admin_login.html")

@app.route("/admin_logout", methods=["GET"])
def admin_logout_view():
    return render_template("admin_logout.html")

@app.route("/admin_otp_verification", methods=["GET"])
def admin_otp_verification_view():
    return render_template("admin_otp_verification.html")

@app.route("/admin_profile", methods=["GET"])
def admin_profile_view():
    return render_template("admin_profile.html")

@app.route("/admin_reset_password", methods=["GET"])
def admin_reset_password_view():
    return render_template("admin_reset_password.html")

@app.route("/admin_reset_success", methods=["GET"])
def admin_reset_success_view():
    return render_template("admin_reset_success.html")

@app.route("/admin_total_farms", methods=["GET"])
def admin_total_farms_view():
    return render_template("admin_total_farms.html")

@app.route("/alerts", methods=["GET"])
def alerts_view():
    return render_template("alerts.html")

@app.route("/change_password", methods=["GET"])
def change_password_view():
    return render_template("change_password.html")

@app.route("/edit_profile", methods=["GET"])
def edit_profile_view():
    return render_template("edit_profile.html")

@app.route("/farmer_dashboard", methods=["GET"])
def farmer_dashboard_view():
    return render_template("farmer_dashboard.html")

@app.route("/forgot_password", methods=["GET"])
def forgot_password_view():
    return render_template("forgot_password.html")

@app.route("/otp_verification", methods=["GET"])
def otp_verification_view():
    return render_template("otp_verification.html")

@app.route("/privacy", methods=["GET"])
def privacy_view():
    return render_template("privacy.html")

@app.route("/profile_settings", methods=["GET"])
def profile_settings_view():
    return render_template("profile_settings.html")

@app.route("/reset_password", methods=["GET"])
def reset_password_view():
    return render_template("reset_password.html")

@app.route("/reset_success", methods=["GET"])
def reset_success_view():
    return render_template("reset_success.html")

@app.route("/treatment_history", methods=["GET"])
def treatment_history_view():
    return render_template("treatment_history.html")

@app.route("/withdrawal_status", methods=["GET"])
def withdrawal_status_view():
    return render_template("withdrawal_status.html")

# ========================================================
# ✅ REGISTER (Updated to save farm_name)
# ==========================================================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    farm_name = data.get("farm_name") # Extracted from request

    # Validation
    if not all([full_name, email, password, confirm_password, farm_name]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    if not re.match(r"^[A-Za-z\s]+$", full_name):
        return jsonify({"status": "error", "message": "Full name must contain only letters and spaces"}), 400

    if not re.match(r"^[A-Za-z\s]+$", farm_name):
        return jsonify({"status": "error", "message": "Farm name must contain only letters and spaces"}), 400
    
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({"status": "error", "message": "Invalid email format"}), 400

    missing_requirements = validate_password(password)
    if missing_requirements:
        return jsonify({"status": "error", "message": f"Password must contain: {', '.join(missing_requirements)}"}), 400

    if password != confirm_password:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM register WHERE email=%s", (email,))
            if cursor.fetchone():
                return jsonify({"status": "error", "message": "Mail already registered"}), 409

            hashed_password = generate_password_hash(password)

            # Updated SQL: Added farm_name to columns and values
            cursor.execute(
                "INSERT INTO register (full_name, email, password, farm_name) VALUES (%s, %s, %s, %s)",
                (full_name, email, hashed_password, farm_name)
            )
            conn.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201
    finally:
        conn.close()

# ==========================================================
# ✅ LOGIN (Updated to return farm_name)
# ==========================================================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM register WHERE email=%s", (email,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"status": "error", "message": "Email is not registered."}), 404

            if not check_password_hash(user["password"], password):
                return jsonify({"status": "error", "message": "Incorrect password."}), 401

            return jsonify({
                "status": "success",
                "message": "Login successful",
                "user": {
                    "id": user["id"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "farm_name": user["farm_name"] # Now returned to frontend
                }
            }), 200
    finally:
        conn.close()

# ==========================================================
# ✅ FORGOT PASSWORD (SEND OTP)
# ==========================================================
@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Check register table (Farmer)
            cursor.execute("SELECT id FROM register WHERE email=%s", (email,))
            user = cursor.fetchone()
            table = "register"

            # Check admin_users table (Admin) if not found in register
            if not user:
                cursor.execute("SELECT id FROM admin_users WHERE email=%s", (email,))
                user = cursor.fetchone()
                table = "admin_users"

            if not user:
                return jsonify({"status": "error", "message": "Email not registered"}), 404

            otp = str(random.randint(1000, 9999))

            # Update the correct table
            cursor.execute(
                f"UPDATE {table} SET otp=%s, otp_expiry=DATE_ADD(NOW(), INTERVAL 2 MINUTE) WHERE id=%s",
                (otp, user["id"])
            )
            conn.commit()

        try:
            import smtplib
            from email.message import EmailMessage
            msg = EmailMessage()
            msg.set_content(f"Your Reset Password OTP is: {otp}. It is valid for 2 minutes.")
            msg['Subject'] = "Password Reset OTP"
            msg['From'] = "gvennela1105@gmail.com"
            msg['To'] = email

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("gvennela1105@gmail.com", "dufatkzheqttmqwo")
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Mail Error:", e)
            return jsonify({"status": "error", "message": f"Failed to send OTP: {str(e)}"}), 500

        return jsonify({"status": "success", "message": "OTP sent to registered email"}), 200
    finally:
        conn.close()

# ==========================================================
# ✅ VERIFY OTP
# ==========================================================
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    otp = (data.get("otp") or "").strip()

    if not email or not otp:
        return jsonify({"status": "error", "message": "Email and OTP required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Check register table first
            cursor.execute("SELECT otp, (otp_expiry > NOW()) as is_valid FROM register WHERE email=%s", (email,))
            user = cursor.fetchone()
            
            # If not in register, check admin_users
            if not user:
                cursor.execute("SELECT otp, (otp_expiry > NOW()) as is_valid FROM admin_users WHERE email=%s", (email,))
                user = cursor.fetchone()

            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404

            db_otp = str(user.get("otp") or "").strip()
            if db_otp != otp:
                return jsonify({"status": "error", "message": "Invalid OTP"}), 400

            if not user.get("is_valid"):
                return jsonify({"status": "error", "message": "OTP expired"}), 400

        return jsonify({"status": "success", "message": "OTP verified. Ready to reset password."}), 200
    finally:
        conn.close()

# ==========================================================
# ✅ RESET PASSWORD
# ==========================================================
@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not email or not new_password or not confirm_password:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    if new_password != confirm_password:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400

    missing_requirements = validate_password(new_password)
    if missing_requirements:
        return jsonify({"status": "error", "message": f"Password must contain: {', '.join(missing_requirements)}"}), 400

    hashed_password = generate_password_hash(new_password)

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Determine which table to update
            cursor.execute("SELECT id FROM register WHERE email=%s", (email,))
            is_farmer = cursor.fetchone() is not None
            table = "register" if is_farmer else "admin_users"

            # If not farmer, double check it's an admin
            if not is_farmer:
                cursor.execute("SELECT id FROM admin_users WHERE email=%s", (email,))
                if not cursor.fetchone():
                    return jsonify({"status": "error", "message": "User not found"}), 404

            # Update password based on role (Farmer is hashed, Admin is plain text but snippet uses hashed?)
            # Wait, the user's admin login used plain text! 
            # sql = "SELECT id, password FROM admin_users WHERE email = %s"
            # if admin["password"] != password: 
            # So admin passwords are currently plain text in this app's database.
            # I'll stick to plain text for admin if that's what's currently used.
            
            password_to_store = hashed_password if is_farmer else new_password

            cursor.execute(
                f"UPDATE {table} SET password=%s, otp=NULL, otp_expiry=NULL WHERE email=%s",
                (password_to_store, email)
            )
            conn.commit()

        return jsonify({"status": "success", "message": "Password reset successfully"}), 200
    finally:
        conn.close()

# ==========================================================
# ADD ANIMAL
# ==========================================================
@app.route("/add-animal", methods=["POST"])
def add_animal():
    data = request.get_json(silent=True) or {}
    
    # Required fields based on your frontend UI
    user_id = data.get("user_id")
    species = data.get("species")
    tag_id = data.get("tag_id")
    dob_str = data.get("dob") # Format: "dd/MM/yyyy"
    gender = data.get("gender")
    weight = data.get("weight")
    
    # Optional fields
    animal_name = data.get("animal_name", "")
    breed = data.get("breed", "")

    if not all([user_id, species, tag_id, dob_str, gender, weight]):
        return jsonify({"status": "error", "message": "Missing required animal fields"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        # Convert date string to SQL date format
        formatted_dob = datetime.strptime(dob_str, "%d/%m/%Y").date()

        with conn.cursor() as cursor:
            # Check if tag_id already exists for this farmer
            cursor.execute("SELECT id FROM animals WHERE user_id=%s AND tag_id=%s", (user_id, tag_id))
            if cursor.fetchone():
                return jsonify({"status": "error", "message": "Animal with this Tag ID already registered"}), 409

            sql = """
                INSERT INTO animals (user_id, species, tag_id, animal_name, dob, gender, weight_kg, breed)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, species, tag_id, animal_name, formatted_dob, gender, weight, breed))
            conn.commit()

        return jsonify({"status": "success", "message": f"Animal {tag_id} registered successfully!"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# ==========================================================
# ADD TREATMENT
# ==========================================================
@app.route("/add-treatment", methods=["POST"])
def add_treatment():
    data = request.get_json(silent=True) or {}
    
    user_id = data.get("user_id")
    tag_id = data.get("animal_id")
    animal_type = data.get("animal_type")
    drug_name = data.get("drug_name")
    dosage = data.get("dosage")
    date_str = data.get("treatment_date")
    notes = data.get("notes", "")

    if not all([user_id, tag_id, drug_name, date_str]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        treatment_date = datetime.strptime(date_str, "%d/%m/%Y").date()

        with conn.cursor() as cursor:
            # Check database for drug rules
            cursor.execute("""
                SELECT `COL 3`, `COL 4`, `COL 5` 
                FROM withdrawlstatus 
                WHERE LOWER(`COL 1`) = LOWER(%s) AND LOWER(`COL 2`) = LOWER(%s)
            """, (animal_type, drug_name))
            
            rules = cursor.fetchone()

            if rules:
                # 1. Drug FOUND in table
                meat_days = _to_int(rules['COL 3'], 0)
                milk_days = _to_int(rules['COL 4'], 0)
                egg_days = _to_int(rules['COL 5'], 0)
            else:
                # 2. Drug NOT FOUND (or "Others" selected)
                # Apply Statutory Minimums (28 days meat, 7 days milk/eggs)
                meat_days = 28
                milk_days = 7
                egg_days = 7
                notes = (notes + " [Statutory Minimum Applied]").strip()

            meat_safe = treatment_date + timedelta(days=meat_days)
            milk_safe = treatment_date + timedelta(days=milk_days)
            egg_safe = treatment_date + timedelta(days=egg_days)

            sql = """
                INSERT INTO treatments 
                (user_id, animal_tag_id, animal_type, drug_name, dosage, treatment_date, 
                 meat_safe_date, milk_safe_date, egg_safe_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, tag_id, animal_type, drug_name, dosage, 
                                 treatment_date, meat_safe, milk_safe, egg_safe, notes))
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Treatment recorded successfully",
            "applied_rule": "Database" if rules else "Statutory Minimum (Others)",
            "withdrawal_summary": {
                "meat_safe_on": meat_safe.strftime("%d/%m/%Y"),
                "milk_safe_on": milk_safe.strftime("%d/%m/%Y"),
                "egg_safe_on": egg_safe.strftime("%d/%m/%Y")
            }
        }), 201

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# All Animals

@app.route("/all-animals/<user_id>", methods=["GET"]) # Remove the 'int:' for now to be safe
def get_all_animals(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Change %d to %s here. %s is safer for pymysql.
            sql = """
                SELECT tag_id, animal_name, species, breed, weight_kg, 
                DATE_FORMAT(dob, '%%d/%%m/%%Y') as dob, gender 
                FROM animals WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            animals = cursor.fetchall()
            
            return jsonify({"status": "success", "data": animals}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

#withdrawal status

@app.route("/withdrawal-status/<int:user_id>", methods=["GET"])
def get_withdrawal_status(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Fetch all treatments for this user
            sql = """
                SELECT 
                    animal_tag_id, animal_type, drug_name, 
                    DATE_FORMAT(treatment_date, '%%b %%d, %%Y') as treatedDate,
                    DATE_FORMAT(meat_safe_date, '%%b %%d, %%Y') as safeDateMeat,
                    DATE_FORMAT(milk_safe_date, '%%b %%d, %%Y') as safeDateMilk,
                    DATE_FORMAT(egg_safe_date, '%%b %%d, %%Y') as safeDateEggs,
                    meat_safe_date, milk_safe_date, egg_safe_date
                FROM treatments 
                WHERE user_id = %s
                ORDER BY treatment_date DESC
            """
            cursor.execute(sql, (user_id,))
            records = cursor.fetchall()

            results = []
            today = date.today()
            active_count = 0
            safe_count = 0

            for r in records:
                # Find the furthest safe date to calculate overall days remaining
                # We filter out None values in case some medicines don't have milk/egg withdrawal
                dates = [r['meat_safe_date'], r['milk_safe_date'], r['egg_safe_date']]
                valid_dates = [d for d in dates if d is not None]
                
                max_safe_date = max(valid_dates) if valid_dates else today
                diff = (max_safe_date - today).days
                days_left = max(0, diff)

                is_active = days_left > 0
                if is_active: active_count += 1 
                else: safe_count += 1

                results.append({
                    "id": r['animal_tag_id'],
                    "type": r['animal_type'],
                    "drug": r['drug_name'],
                    "treatedDate": r['treatedDate'],
                    "safeDateMeat": r['safeDateMeat'],
                    "safeDateMilk": r['safeDateMilk'],
                    "safeDateEggs": r['safeDateEggs'],
                    "daysRemaining": days_left,
                    "isActive": is_active
                })

        return jsonify({
            "status": "success",
            "active_withdrawals": active_count,
            "safe_to_sell": safe_count,
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# Treatment History

@app.route("/treatment-history/<int:user_id>", methods=["GET"])
def get_treatment_history(user_id):
    # Get optional filter from URL parameters: ?type=Cow
    animal_type = request.args.get('type')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # Base Query
            sql = """
                SELECT 
                    animal_tag_id as id, animal_type as type, drug_name as drug, 
                    dosage, notes,
                    DATE_FORMAT(treatment_date, '%%b %%d, %%Y') as date,
                    DATE_FORMAT(milk_safe_date, '%%b %%d') as safeDateMilk,
                    DATE_FORMAT(meat_safe_date, '%%b %%d') as safeDateMeat,
                    DATE_FORMAT(egg_safe_date, '%%b %%d') as safeDateEggs,
                    meat_safe_date
                FROM treatments 
                WHERE user_id = %s
            """
            
            # If farmer clicked a filter chip (like 'Cow'), add it to the SQL
            if animal_type and animal_type != "All":
                sql += " AND animal_type = %s"
                cursor.execute(sql + " ORDER BY treatment_date DESC", (user_id, animal_type))
            else:
                cursor.execute(sql + " ORDER BY treatment_date DESC", (user_id,))

            rows = cursor.fetchall()
            today = date.today()

            for row in rows:
                # Calculate status: If meat_safe_date is in the future, it's 'Inprogress'
                if row['meat_safe_date'] > today:
                    row['status'] = "Inprogress"
                else:
                    row['status'] = "Completed"
                
                # Clean up: remove the raw date object before sending JSON
                del row['meat_safe_date']

        return jsonify({"status": "success", "data": rows}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()
        
# ==========================================================
# ✅ SMART ALERTS API (Robust Version)
# ==========================================================
@app.route("/get-alerts/<int:user_id>", methods=["GET"])
def get_alerts(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # TARGET TIME FOR CLEARANCE: 6:20 PM
        target_hour = 18
        target_minute = 20
        is_clearance_time = current_hour > target_hour or (current_hour == target_hour and current_minute >= target_minute)

        with conn.cursor() as cursor:
            # We fetch everything to check tomorrow's status carefully
            sql = """
                SELECT animal_tag_id, animal_type, 
                       DATEDIFF(meat_safe_date, CURDATE()) as days_to_meat,
                       DATEDIFF(milk_safe_date, CURDATE()) as days_to_milk,
                       DATEDIFF(egg_safe_date, CURDATE()) as days_to_eggs
                FROM treatments 
                WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            records = cursor.fetchall()

            alerts = []
            
            # 1. ALWAYS ADD TOMORROW'S ALERTS
            for r in records:
                tag = r['animal_tag_id']
                species = (r['animal_type'] or '').lower()
                
                # Robust species mapping
                has_milk = species in ["cow", "buffalo", "goat", "sheep"]
                has_eggs = species in ["hen", "chicken", "poultry", "bird"]
                
                m_days = r['days_to_meat']
                l_days = r['days_to_milk']
                e_days = r['days_to_eggs']

                # UPCOMING (Tomorrow)
                ending_tomorrow = []
                # Check for strictly day 1 (tomorrow)
                if m_days == 1: ending_tomorrow.append("Meat")
                if has_milk and l_days == 1: ending_tomorrow.append("Milk")
                if has_eggs and e_days == 1: ending_tomorrow.append("Eggs")

                if ending_tomorrow:
                    prod_str = " and ".join(ending_tomorrow)
                    alerts.append({
                        "title": "Withdrawal Ending Tomorrow",
                        "message": f"Advance Warning: {prod_str} withdrawal for {tag} ({r['animal_type']}) ends tomorrow. Monitor for final clearance.",
                        "animalId": tag,
                        "timeAgo": "Tomorrow",
                        "type": "WARNING",
                        "isUnread": True
                    })

                # 2. ADD CLEARANCE ALERTS (Only after 6:20 PM)
                if is_clearance_time:
                    safe_today = []
                    if m_days == 0: safe_today.append("Meat")
                    if has_milk and l_days == 0: safe_today.append("Milk")
                    if has_eggs and e_days == 0: safe_today.append("Eggs")

                    if safe_today:
                        prod_str = " and ".join(safe_today)
                        alerts.append({
                            "title": "Product Safe & Cleared",
                            "message": f"Confirmed: {prod_str} from {tag} is now officially safe to sell/market.",
                            "animalId": tag,
                            "timeAgo": "Just Now",
                            "type": "SUCCESS",
                            "isUnread": True
                        })

            # 3. ADD INFO ALERT IF ACTIVE
            if is_clearance_time:
                alerts.insert(0, {
                    "title": "Compliance Check Complete",
                    "message": "Today's safety clearance check is finished. Valid for market entry.",
                    "animalId": "SYSTEM",
                    "timeAgo": "6:20 PM",
                    "type": "INFO",
                    "isUnread": False
                })

        return jsonify({"status": "success", "data": alerts}), 200

    except Exception as e:
        print(f"❌ Alert Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()


#Farmer Dashboard

@app.route("/dashboard-summary/<int:user_id>", methods=["GET"])
def get_dashboard_summary(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # 1. Fetch User Name for the Header
            cursor.execute("SELECT full_name FROM register WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            user_name = user['full_name'] if user else "Farmer"

            # 2. Fetch Top 3 Recent Activities
            sql_activity = """
                SELECT animal_tag_id, drug_name, 
                       DATE_FORMAT(treatment_date, '%%b %%d') as date
                FROM treatments 
                WHERE user_id = %s 
                ORDER BY treatment_date DESC 
                LIMIT 3
            """
            cursor.execute(sql_activity, (user_id,))
            activities = cursor.fetchall()

        return jsonify({
            "status": "success",
            "user_name": user_name,
            "recent_activity": activities
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- FARMER: UPDATE PROFILE ---
@app.route("/farmer/update-profile", methods=["POST"])
def update_farmer_profile():
    data = request.get_json(silent=True) or {}
    
    # Identification field
    current_email = data.get("current_email") 
    
    # Updateable fields from your Kotlin EditProfileScreen
    new_name = data.get("full_name")
    new_email = data.get("email")
    phone = data.get("phone_number")
    farm = data.get("farm_name")

    if not current_email:
        return jsonify({"status": "error", "message": "Missing current email identifier"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We update the 'register' table which holds farmer data
            # Note: Ensure these columns (phone_number, farm_name) exist in your DB
            sql = """
                UPDATE register 
                SET full_name = %s, email = %s, phone_number = %s, farm_name = %s 
                WHERE email = %s
            """
            cursor.execute(sql, (new_name, new_email, phone, farm, current_email))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"status": "error", "message": "User not found or no changes made"}), 404

            return jsonify({
                "status": "success", 
                "message": "Profile updated successfully"
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- FARMER: DELETE ACCOUNT ---
@app.route("/farmer/delete-account", methods=["DELETE"]) # Using DELETE method for safety
def delete_farmer_account():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    confirmation = data.get("confirmation")

    # 1. Validation
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    
    if confirmation != "DELETE":
        return jsonify({"status": "error", "message": "Confirmation text must be 'DELETE'"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 2. Delete the record from the 'register' table
            sql = "DELETE FROM register WHERE email = %s"
            cursor.execute(sql, (email,))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"status": "error", "message": "Account not found"}), 404

            return jsonify({
                "status": "success", 
                "message": "Account has been permanently deleted"
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

#Admin Login
@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    # 1. Check if the user sent both fields
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 2. Only fetch the password and id from the admin_users table
            sql = "SELECT id, password FROM admin_users WHERE email = %s"
            cursor.execute(sql, (email,))
            admin = cursor.fetchone()

            # 3. If email doesn't exist
            if not admin:
                return jsonify({"status": "error", "message": "Admin account not found"}), 401

            # 4. Plain Text Password Check
            # We compare the input password directly to the one in the database
            if admin["password"] != password:
                return jsonify({"status": "error", "message": "Incorrect password"}), 401

            # 5. Success
            return jsonify({
                "status": "success",
                "message": "Welcome to the Administrator Portal",
                "data": {
                    "admin_id": admin["id"],
                    "email": email
                }
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()
    
# --- FARMER: CHANGE PASSWORD ---
@app.route("/farmer/change-password", methods=["POST"])
def farmer_change_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email") # The farmer's email
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    # 1. Basic Validation
    if not all([email, current_password, new_password, confirm_password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    if new_password != confirm_password:
        return jsonify({"status": "error", "message": "New passwords do not match"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 2. Verify farmer exists and check current password
            # Using your 'register' table for farmers
            sql_select = "SELECT password FROM register WHERE email = %s"
            cursor.execute(sql_select, (email,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"status": "error", "message": "Farmer account not found"}), 404

            # Check if the plain text 'current_password' matches the hash in DB
            if not check_password_hash(user["password"], current_password):
                return jsonify({"status": "error", "message": "Current password is incorrect"}), 401

            # 3. Hash the new password and update
            new_hashed_password = generate_password_hash(new_password)
            sql_update = "UPDATE register SET password = %s WHERE email = %s"
            cursor.execute(sql_update, (new_hashed_password, email))
            conn.commit()

            return jsonify({"status": "success", "message": "Password updated successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- 1. GET ALL DRUGS (For the List Screen) ---
@app.route("/admin/drugs", methods=["GET"])
def api_get_all_drugs():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Using backticks for columns with spaces
            sql = "SELECT `COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5` FROM withdrawlstatus"
            cursor.execute(sql)
            drugs = cursor.fetchall()
            
            # Formatting to match your Kotlin DrugData class
            formatted = []
            for d in drugs:
                formatted.append({
                    "name": d.get('COL 2', 'N/A'),
                    "species": d.get('COL 1', 'N/A'),
                    "meatWithdrawal": f"Meat: {d.get('COL 3', 0)} days",
                    "milkWithdrawal": f"Milk: {d.get('COL 4', 0)} days",
                    "eggsWithdrawal": f"Eggs: {d.get('COL 5', 'NA')}"
                })
            return jsonify({"status": "success", "data": formatted}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- ADD NEW DRUG (POST) ---
@app.route("/admin/add-drug", methods=["POST"])
def add_new_drug_to_db():
    data = request.get_json(silent=True) or {}
    
    # We use .get(key, default) to prevent NULLs
    # This checks for both naming styles just in case
    species = data.get('species', 'N/A')
    name = data.get('name', 'Unknown Drug')
    
    # If 'meat' is missing, it looks for 'meat_withdrawal'. If both missing, 0.
    meat = data.get('meat') or data.get('meat_withdrawal') or "0"
    milk = data.get('milk') or data.get('milk_withdrawal') or "0"
    eggs = data.get('eggs') or data.get('eggs_withdrawal') or "NA"

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Table: withdrawlstatus | Columns: COL 1 to COL 5
            sql = "INSERT INTO withdrawlstatus (`COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (species, name, meat, milk, eggs))
            conn.commit()
            return jsonify({"status": "success", "message": f"Added {name} successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- 3. EDIT DRUG (For the Edit Dialog) ---
@app.route("/admin/edit-drug", methods=["PUT"])
def api_edit_drug_withdrawal():
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We find the drug by its name (COL 2) and update its periods
            sql = """
                UPDATE withdrawlstatus 
                SET `COL 1` = %s, `COL 3` = %s, `COL 4` = %s, `COL 5` = %s 
                WHERE `COL 2` = %s
            """
            cursor.execute(sql, (
                data.get('species'),
                data.get('meat'),
                data.get('milk'),
                data.get('eggs'),
                data.get('name') # The name is the identifier
            ))
            conn.commit()
            return jsonify({"status": "success", "message": "Withdrawal periods updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- ADMIN: GET ALL FARMS (With Search Support) ---
@app.route("/admin/all-farms", methods=["GET"])
def get_all_farms_list():
    # Optional search parameter: /admin/all-farms?search=Green
    search_query = request.args.get('search', '')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB connection failed"}), 500
        
    try:
        with conn.cursor() as cursor:
            # SQL to fetch farm details and count their animals
            # We filter by role='farmer' if you have a role column, 
            # or just fetch all from register if they are all farmers.
            # In your existing code, 'register' seems to be only farmers.
            sql = """
                SELECT 
                    r.id, 
                    r.full_name, 
                    r.farm_name,
                    (SELECT COUNT(*) FROM animals a WHERE a.user_id = r.id) as animal_count
                FROM register r
                WHERE (r.farm_name LIKE %s OR r.full_name LIKE %s)
                ORDER BY r.farm_name ASC
            """
            like_pattern = f"%{search_query}%"
            cursor.execute(sql, (like_pattern, like_pattern))
            farms = cursor.fetchall()

            formatted_farms = []
            for f in farms:
                formatted_farms.append({
                    "name": f['farm_name'] if f['farm_name'] else f"{f['full_name']}'s Farm",
                    "animals": f"{f['animal_count']} Animals",
                    "owner": f['full_name'],
                    "region": "Registered"
                })

            return jsonify({
                "status": "success",
                "count": len(formatted_farms),
                "data": formatted_farms
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- ADMIN: DASHBOARD SUMMARY & RECENT FARMS ---
@app.route("/admin/dashboard", methods=["GET"])
def get_admin_dashboard_data():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Fetch Stats
            # Count farmers
            cursor.execute("SELECT COUNT(*) as total FROM register WHERE role = 'farmer'")
            total_farms = cursor.fetchone()['total']

            # Count total animals
            cursor.execute("SELECT COUNT(*) as total FROM animals")
            total_animals = cursor.fetchone()['total']

            # Count active treatments (where current date is within withdrawal period)
            # This is a placeholder query; adjust based on your specific treatment table name
            cursor.execute("SELECT COUNT(*) as total FROM treatments WHERE status = 'Active'")
            active_treatments = cursor.fetchone().get('total', 0)

            # 2. Fetch Recent Farms (Last 8 registered)
            # We map database columns to your Kotlin FarmData class
            sql_recent = """
                SELECT 
                    r.full_name, 
                    r.farm_name,
                    (SELECT COUNT(*) FROM animals a WHERE a.user_id = r.id) as animal_count
                FROM register r
                WHERE r.role = 'farmer'
                ORDER BY r.id DESC
                LIMIT 8
            """
            cursor.execute(sql_recent)
            recent_farms = cursor.fetchall()

            # Format the list for the LazyColumn
            farms_list = []
            for farm in recent_farms:
                farms_list.append({
                    "name": farm['farm_name'] if farm['farm_name'] else f"{farm['full_name']}'s Farm",
                    "animals": f"{farm['animal_count']} Animals",
                    "owner": farm['full_name'],
                    "region": "Registered" # Or use a real location column if available
                })

            return jsonify({
                "status": "success",
                "stats": {
                    "total_farms": str(total_farms),
                    "total_animals": "{:,}".format(total_animals), # Adds commas (e.g., 1,245)
                    "active_treatments": str(active_treatments)
                },
                "recent_farms": farms_list
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# --- ADMIN: FULL PROFILE UPDATE ---
@app.route("/admin/update-profile-full", methods=["POST"])
def update_admin_profile_full():
    data = request.get_json(silent=True) or {}
    
    # Identifier (The email the admin is currently logged in with)
    current_email = data.get("current_email")
    
    # New values from the Edit Profile Screen
    new_name = data.get("full_name")
    new_email = data.get("email")
    phone = data.get("phone")
    org = data.get("organization")
    pos = data.get("position")
    loc = data.get("location")

    if not current_email:
        return jsonify({"status": "error", "message": "Admin email identifier missing"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We update the 'admin_users' table
            sql = """
                UPDATE admin_users 
                SET username = %s, email = %s, phone_number = %s, 
                    organization = %s, position = %s, location = %s 
                WHERE email = %s
            """
            cursor.execute(sql, (new_name, new_email, phone, org, pos, loc, current_email))
            conn.commit()

            return jsonify({
                "status": "success", 
                "message": "Admin profile updated successfully"
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()



# ==========================================================
# ✅ PAGE RENDERING & REDIRECTS
# ==========================================================

@app.before_request
def clear_trailing_html():
    # Only redirect GET requests that end in .html
    if request.method == 'GET' and request.path.endswith('.html'):
        new_url = request.path[:-5]
        if request.query_string:
            new_url += '?' + request.query_string.decode('utf-8')
        return redirect(new_url, code=301)

@app.route("/", methods=["GET"])
def home_root():
    return render_template("index.html")

# ==========================================================
# Run Server
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug = True)