from werkzeug.security import check_password_hash

from flask import (
    Flask,
    render_template,
    jsonify,
    send_file,
    redirect,
    url_for,
    request,
    session
)

from modules.report import (
    generate_excel,
    generate_csv,
    generate_pdf
)
from modules.analytics import (
    get_analytics,
    get_event_distribution,
    get_top_users_chart
)

from modules.alerts import get_alerts

from modules.auth import authenticate

from modules.settings import get_settings

from modules.users import (
    get_all_users,
    get_user,
    get_user_by_username,
    add_user,
    update_user,
    delete_user,
    count_admins,
    change_password
)

from modules.audit import (
    log_action,
    get_audit_logs
)



import sqlite3
import os

app = Flask(__name__)

app.secret_key = "secure_monitoring_secret_key"

DATABASE = "database/filemonitor.db"


# -------------------------------------------------
# Database Connection
# -------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------------------------
# Fetch All Events
# -------------------------------------------------
def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM file_events
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows

# -------------------------------------------------
# Top Active Users
# -------------------------------------------------

def get_top_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            username,

            COUNT(*) as total

        FROM file_events

        GROUP BY username

        ORDER BY total DESC

        LIMIT 5

    """)

    users = cursor.fetchall()

    conn.close()

    return users

# -------------------------------------------------
# Get All Users
# -------------------------------------------------




# -------------------------------------------------
# Dashboard Statistics
# -------------------------------------------------
def get_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # -------------------------
    # Total Events
    # -------------------------
    cursor.execute("SELECT COUNT(*) FROM file_events")
    stats["total_events"] = cursor.fetchone()[0]

    # -------------------------
    # Event Types
    # -------------------------
    event_types = ["Created", "Modified", "Deleted", "Moved"]

    for event in event_types:

        cursor.execute(
            "SELECT COUNT(*) FROM file_events WHERE event_type=?",
            (event,)
        )

        stats[event.lower()] = cursor.fetchone()[0]

    # -------------------------
    # Sensitive Files
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE sensitive='Yes'
    """)

    stats["sensitive"] = cursor.fetchone()[0]

    # -------------------------
    # Authorized
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE authorized='Yes'
    """)

    stats["authorized"] = cursor.fetchone()[0]

    # -------------------------
    # Unauthorized
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE authorized='No'
    """)

    stats["unauthorized"] = cursor.fetchone()[0]

    # -------------------------
    # Integrity Verified
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE integrity_status='Verified'
    """)

    stats["verified"] = cursor.fetchone()[0]

    # -------------------------
    # Integrity Failed
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE integrity_status!='Verified'
    """)

    stats["failed"] = cursor.fetchone()[0]

    # -------------------------
    # Today's Events
    # -------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE DATE(timestamp)=DATE('now')
    """)

    stats["today_events"] = cursor.fetchone()[0]

    # -------------------------
    # Latest Event
    # -------------------------
    cursor.execute("""
        SELECT *
        FROM file_events
        ORDER BY id DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()

    if latest:

        stats["latest_event"] = dict(latest)

    else:

        stats["latest_event"] = None

    conn.close()

    return stats


# -------------------------------------------------
# Home Page
# -------------------------------------------------

@app.route("/")
def home():

    if not session.get("logged_in"):

        return redirect("/login")

    events = get_all_events()

    stats = get_statistics()

    top_users = get_top_users()

    return render_template(
        "index.html",
        data=events,
        stats=stats,
        top_users=top_users,
        chart_data={
            "created": stats["created"],
            "modified": stats["modified"],
            "deleted": stats["deleted"],
            "moved": stats["moved"]
        }
    )


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):

        return redirect("/login")

    events = get_all_events()

    stats = get_statistics()

    top_users = get_top_users()

    return render_template(
        "index.html",
        data=events,
        stats=stats,
        top_users=top_users,
        chart_data={
            "created": stats["created"],
            "modified": stats["modified"],
            "deleted": stats["deleted"],
            "moved": stats["moved"]
        }
    )


# -------------------------------------------------
# Analytics Page
# -------------------------------------------------

@app.route("/analytics")
def analytics():

    if not session.get("logged_in"):

        return redirect("/login")

    analytics_data = get_analytics()

    chart_data = get_event_distribution()

    users_chart = get_top_users_chart()

    return render_template(
        "analytics.html",
        analytics=analytics_data,
        chart_data=chart_data,
        users_chart=users_chart
    )


# -------------------------------------------------
# Alert Center
# -------------------------------------------------

@app.route("/alerts")
def alerts():

    if not session.get("logged_in"):

        return redirect("/login")

    alert_data = get_alerts()

    return render_template(
        "alerts.html",
        alerts=alert_data
    )


# -------------------------------------------------
# Events Page
# -------------------------------------------------
@app.route("/events")
def events():

    if not session.get("logged_in"):

        return redirect("/login")

    events = get_all_events()

    return render_template(
        "events.html",
        data=events
    )


# -------------------------------------------------
# JSON API
# -------------------------------------------------

@app.route("/api/events")
def api_events():

    if not session.get("logged_in"):

        return redirect("/login")

    events = get_all_events()

    result = []

    for row in events:
        result.append(dict(row))

    return jsonify(result)


# -------------------------------------------------
# Export Excel Report
# -------------------------------------------------

@app.route("/export/excel")
def export_excel():

    if not session.get("logged_in"):

        return redirect("/login")

    filepath = generate_excel()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Secure_File_Monitor_Report.xlsx"
    )


# -------------------------------------------------
# Export CSV Report
# -------------------------------------------------

@app.route("/export/csv")
def export_csv():

    if not session.get("logged_in"):

        return redirect("/login")

    filepath = generate_csv()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Secure_File_Monitor_Report.csv"
    )

# -------------------------------------------------
# Export PDF Report
# -------------------------------------------------

@app.route("/export/pdf")
def export_pdf():

    if not session.get("logged_in"):

        return redirect("/login")

    filepath = generate_pdf()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Secure_File_Monitor_Report.pdf"
    )

# -------------------------------------------------
# Error Handling
# -------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


# -------------------------------------------------
# Login
# -------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if session.get("logged_in"):
        return redirect("/")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Authenticate from database
        user = authenticate(username, password)

        if user:

            session["logged_in"] = True
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]

            log_action(
                session["username"],
                "LOGIN",
                "User logged into the system"
            )

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html",
        error=None
    )


# -------------------------------------------------
# Logout
# -------------------------------------------------

@app.route("/logout")
def logout():

    if session.get("logged_in"):

        log_action(
            session["username"],
            "LOGOUT",
            "User logged out"
        )

    session.clear()

    return redirect("/login")


# -------------------------------------------------
# Reports Page
# -------------------------------------------------

@app.route("/reports")
def reports():

    if not session.get("logged_in"):

        return redirect("/login")

    stats = get_statistics()

    return render_template(
        "reports.html",
        stats=stats
    )


# -------------------------------------------------
# Settings Page
# -------------------------------------------------

@app.route("/settings")
def settings():

    if not session.get("logged_in"):

        return redirect("/login")

    settings_data = get_settings()

    return render_template(
        "settings.html",
        settings=settings_data
    )

# -------------------------------------------------
# User Management
# -------------------------------------------------

@app.route("/users")
def users():

    if not session.get("logged_in"):
        return redirect("/login")

    if session.get("role") != "Administrator":
        return "Access Denied", 403

    user_list = get_all_users()


    for user in user_list:

    return render_template(
        "users.html",
        users=user_list
    )


# -------------------------------------------------
# Add User
# -------------------------------------------------

@app.route("/users/add", methods=["GET", "POST"])
def add_new_user():

    if not session.get("logged_in"):
        return redirect("/login")

    if session.get("role") != "Administrator":
        return "Access Denied", 403

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"]
        role = request.form["role"]
        status = "Active"

        # Check if username already exists
        users = get_all_users()

        for user in users:
            if user["username"] == username:
                return render_template(
                    "add_user.html",
                    error="Username already exists."
                )

        add_user(
            username=username,
            password=password,
            full_name=full_name,
            role=role,
            status=status
        )

        log_action(
            session["username"],
            "CREATE USER",
            f"Created user: {username}"
        )


        return redirect("/users")

    return render_template(
        "add_user.html",
        error=None
    )


# -------------------------------------------------
# Edit User
# -------------------------------------------------

@app.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user_page(user_id):

    if not session.get("logged_in"):
        return redirect("/login")

    if session.get("role") != "Administrator":
        return "Access Denied", 403

    user = get_user(user_id)

    if user is None:
        return "User not found", 404

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"]
        role = request.form["role"]
        status = request.form["status"]
        changes = []

        if user["full_name"] != full_name:
            changes.append(
                f"Full Name: '{user['full_name']}' → '{full_name}'"
            )

        if user["username"] != username:
            changes.append(
                f"Username: '{user['username']}' → '{username}'"
            )

        if user["role"] != role:
            changes.append(
                f"Role: '{user['role']}' → '{role}'"
            )

        if user["status"] != status:
            changes.append(
                f"Status: '{user['status']}' → '{status}'"
            )

        if password and not check_password_hash(user["password"], password):
            changes.append("Password was changed")





        # Prevent administrator from deactivating their own account
        if (
            user_id == session.get("user_id")
            and status == "Inactive"
        ):
            return "You cannot deactivate your own account.", 400

        update_user(
            user_id=user_id,
            username=username,
            password=password,
            full_name=full_name,
            role=role,
            status=status
        )

        details = "; ".join(changes)

        if not details:
            details = "No changes made."
        else:
            details = f"Updated user '{username}': {details}"


        log_action(
            session["username"],
            "UPDATE USER",
            details
        )


        return redirect("/users")

    return render_template(
        "edit_user.html",
        user=user,
        error=None
    )


# -------------------------------------------------
# Delete User
# -------------------------------------------------

@app.route("/users/delete/<int:user_id>")
def delete_existing_user(user_id):

    if not session.get("logged_in"):
        return redirect("/login")

    if session.get("role") != "Administrator":
        return "Access Denied", 403

    user = get_user(user_id)

    if not user:
        return "User not found", 404

    # Prevent deleting yourself
    if user["username"] == session["username"]:
        return "You cannot delete your own account."

    # Prevent deleting the last Administrator
    if user["role"] == "Administrator":
        if count_admins() <= 1:
            return "Cannot delete the last Administrator."

    deleted_username = user["username"]

    delete_user(user_id)

    log_action(
        session["username"],
        "DELETE USER",
        f"Deleted user: {deleted_username}"
    )

    return redirect("/users")


# ------------------------------------------------
# Temporary Profile
# ------------------------------------------------

@app.route("/profile")
def profile():

    if not session.get("logged_in"):
        return redirect("/login")

    user = get_user_by_username(session["username"])

    return render_template(
        "profile.html",
        user=user
    )


# -------------------------------------------------
# Change Password 
#--------------------------------------------------

@app.route("/change-password", methods=["GET", "POST"])
def change_password_page():

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Get logged in user
        user = get_user(session["user_id"])

        # Verify current password
        if not check_password_hash(user["password"], current_password):

            return render_template(
                "change_password.html",
                error="Current password is incorrect."
            )

        # New passwords match
        if new_password != confirm_password:

            return render_template(
                "change_password.html",
                error="New passwords do not match."
            )

        # Prevent same password
        if new_password == current_password:

            return render_template(
                "change_password.html",
                error="New password must be different from current password."
            )

        # Update password
        change_password(session["user_id"], new_password)

        log_action(
            session["username"],
            "CHANGE PASSWORD",
            "Password changed successfully"
        )

        return render_template(
            "change_password.html",
            success="Password changed successfully."
        )

    return render_template(
        "change_password.html"
    )



# --------------------------------------------------
# Audit Logs
# --------------------------------------------------


@app.route("/audit-logs")
def audit_logs():

    if not session.get("logged_in"):
        return redirect("/login")

    if session.get("role") != "Administrator":
        return "Access Denied", 403

    logs = get_audit_logs()

    return render_template(
        "audit_logs.html",
        logs=logs
    )



# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":

    os.makedirs("database", exist_ok=True)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
