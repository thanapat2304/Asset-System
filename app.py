from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from backend.asset import get_as_tb_ms
from backend.detail import execute_query , calculate_depreciation , group_depreciation_data_by_year
from backend.db_connection import connect_aep_portal
from backend.dashboard import fetch_COUNT_office , fetch_COUNT_tool , fetch_COUNT_car , fetch_COUNT_Total , get_topic_data , fetch_monthly_asset_value, fetch_COUNT_add ,fetch_COUNT_tower
from backend.login_functions import login , login_required
from backend.type import get_fda_type
from backend.add import dropdown
from backend.location import get_fda_location
from backend.export import export_report
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import os
import calendar
import string
import random

UPLOAD_FOLDER = 'static/data/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.secret_key = '0000000000000000000000000'
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.template_filter('format_currency')
def format_currency(value):
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return "-"

app.jinja_env.filters['format_currency'] = format_currency

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        return login()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    current_day = datetime.now().day
    current_month_number = datetime.now().month
    current_month = calendar.month_abbr[current_month_number]
    current_year = datetime.now().year
    total__COUNT_office= fetch_COUNT_office()
    total_COUNT_tool = fetch_COUNT_tool()
    total_COUNT_car = fetch_COUNT_car()
    total_COUNT_Total = fetch_COUNT_Total()
    total_COUNT_tower = fetch_COUNT_tower()
    total_COUNT_add = fetch_COUNT_add()
    current_time = datetime.now().strftime("%d %B %Y %H:%M")
    data = get_topic_data()
    topics = [row['AS_Type'] for row in data]
    counts = [row['total_asset_value'] for row in data]

    return render_template('dashboard.html', current_time=current_time, total__COUNT_office=total__COUNT_office, total_COUNT_tool=total_COUNT_tool, fetch_COUNT_car=total_COUNT_car
                           ,total_COUNT_Total=total_COUNT_Total, current_day=current_day, current_month=current_month, current_year=current_year, topics=topics, counts=counts
                           ,total_COUNT_tower=total_COUNT_tower ,total_COUNT_add=total_COUNT_add)

@app.route('/monthly-data', methods=['GET'])
def monthly_data():
    data = fetch_monthly_asset_value()
    return jsonify(data)

@app.route('/asset')
@login_required
def asset():
    total_data = get_as_tb_ms()
    return render_template('asset.html', results=total_data)

@app.route('/detail/<int:id>')
@login_required
def detail_asset(id):
    save_time = datetime.now() - timedelta(days=random.randint(0, 1000))
    as_date = datetime.now() - timedelta(days=random.randint(0, 1000))

    data = {
        "id": id,
        "AS_Save_Time": save_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Asset_Code": f"AC{random.randint(1000,9999)}",
        "Account_Num": f"ACC{random.randint(10000,99999)}",
        "YR": random.choice([2018, 2019, 2020, 2021, 2022, 2023]),
        "AS_Type_Name": random.choice(["Type A", "Type B", "Type C"]),
        "AS_Detail": f"รายละเอียดทรัพย์สินที่ {random.randint(1, 100)}",
        "AS_Location_Name": random.choice(["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต"]),
        "Asset_Name": random.choice(["เครื่องคอมพิวเตอร์", "โต๊ะทำงาน", "เก้าอี้"]),
        "AS_Date": as_date.strftime("%Y-%m-%d"),
        "Asset_Value": round(random.uniform(1000, 50000), 2),
        "AS_Store": random.choice(["โกดัง 1", "โกดัง 2", "สำนักงาน"]),
        "AS_Note": "โน้ตเพิ่มเติมบางอย่าง",
        "Department": random.choice(["ไอที", "บัญชี", "การตลาด"]),
        "AS_User": f"user{random.randint(1,50)}",
        "AS_SerialNum": f"SN{random.randint(100000,999999)}",
        "AS_Save_Name": f"ผู้บันทึก{random.randint(1,20)}",
        "Status": random.choice(["ตัดค่าเสื่อมแล้ว", "ยังไม่ตัดค่าเสื่อม"]),
        "AS_File": f"file_{random.randint(1,10)}.pdf",
        "AS_Type": random.randint(1, 3),
    }
    
    if data:
        asset_data = data
        
        if isinstance(asset_data.get('AS_Date'), date):
            as_date = asset_data['AS_Date']
        elif asset_data.get('AS_Date'):
            try:
                as_date = datetime.strptime(asset_data['AS_Date'], "%Y-%m-%d").date()
            except ValueError:
                as_date = None
        else:
            as_date = None
        
        if as_date:
            current_date = datetime.now().date()
            delta = relativedelta(current_date, as_date)
            elapsed_time = f"{delta.years} ปี {delta.months} เดือน {delta.days} วัน"
        else:
            elapsed_time = "ข้อมูลวันที่ไม่ถูกต้อง"
        asset_data['elapsed_time'] = elapsed_time
        
        asset_value_raw = str(asset_data.get('Asset_Value', '')).strip()
        try:
            asset_value = float(asset_value_raw) if asset_value_raw else None
        except ValueError:
            asset_value = None
        
        if asset_value is not None and as_date:
            depreciation_data = calculate_depreciation(as_date, asset_value, asset_data['AS_Type'])
            grouped_depreciation_data = group_depreciation_data_by_year(depreciation_data)
            grand_total = sum(d['depreciation'] for d in depreciation_data if isinstance(d['depreciation'], (int, float)))
            grand_total = "{:,.2f}".format(grand_total)
        else:
            depreciation_data = []
            grouped_depreciation_data = {}
            grand_total = 0
    
    return render_template('detail.html', data=asset_data, depreciation_data=grouped_depreciation_data, as_date=as_date, asset_value=asset_value, grand_total=grand_total)
    
def execute_query(query, params=None):
    connection = connect_aep_portal()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    if query.strip().upper().startswith("SELECT"):
        result = cursor.fetchall()
    else:
        connection.commit()
        result = None
    cursor.close()
    connection.close()
    return result

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    types = [
        {"id": i, "AS_Name_type": random.choice(["Type A", "Type B", "Type C", "Type D", "Type E"])}
        for i in range(1, 6)
    ]

    branches = [
        {"id": i, "AS_Name_Branch": name}
        for i, name in enumerate(["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต", "สาขาขอนแก่น", "สาขาหาดใหญ่"], start=1)
    ]

    save_time = datetime.now() - timedelta(days=random.randint(0, 1000))
    as_date = datetime.now() - timedelta(days=random.randint(0, 1000))

    asset_data = {
        "id": id,
        "AS_Save_Time": save_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Asset_Code": f"AC{random.randint(1000,9999)}",
        "Account_Num": f"ACC{random.randint(10000,99999)}",
        "YR": random.choice([2018, 2019, 2020, 2021, 2022, 2023]),
        "AS_Type_Name": random.choice(["Type A", "Type B", "Type C"]),
        "AS_Detail": f"รายละเอียดทรัพย์สินที่ {random.randint(1, 100)}",
        "AS_Location_Name": random.choice(["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต"]),
        "Asset_Name": random.choice(["เครื่องคอมพิวเตอร์", "โต๊ะทำงาน", "เก้าอี้"]),
        "AS_Date": as_date.strftime("%Y-%m-%d"),
        "Asset_Value": round(random.uniform(1000, 50000), 2),
        "AS_Store": random.choice(["โกดัง 1", "โกดัง 2", "สำนักงาน"]),
        "AS_Note": "โน้ตเพิ่มเติมบางอย่าง",
        "Department": random.choice(["ไอที", "บัญชี", "การตลาด"]),
        "AS_User": f"user{random.randint(1,50)}",
        "AS_SerialNum": f"SN{random.randint(100000,999999)}",
        "AS_Save_Name": f"ผู้บันทึก{random.randint(1,20)}",
        "Status": random.choice(["ตัดค่าเสื่อมแล้ว", "ยังไม่ตัดค่าเสื่อม"]),
        "AS_File": f"file_{random.randint(1,10)}.pdf",
        "AS_Type": random.randint(1, 3),
    }

    if request.method == 'POST':
        return redirect(url_for('detail_asset', id=id))

    dropdown_one = dropdown()
    return render_template('edit.html', asset=asset_data, types=types, branches=branches, dropdown_one=dropdown_one)

@app.route('/delete_asset/<int:id>', methods=['POST'])
def delete_record(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tb_demo WHERE id = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        conn.close()
    return redirect(url_for('asset'))

@app.route('/add_asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    types = [
        {"id": i, "AS_Name_type": random.choice(["Type A", "Type B", "Type C", "Type D", "Type E"])}
        for i in range(1, 6)
    ]

    branches = [
        {"id": i, "AS_Name_Branch": name}
        for i, name in enumerate(["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต", "สาขาขอนแก่น", "สาขาหาดใหญ่"], start=1)
    ]

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        return redirect(url_for('asset'))

    dropdown_one = dropdown()
    return render_template('add.html', types=types, branches=branches, current_datetime=current_datetime, dropdown_one=dropdown_one)

@app.route('/add_type', methods=['GET', 'POST'])
def add_type():
    if request.method == 'POST':
        return jsonify({'message': 'Data successfully added!'}), 200

    total_data = get_fda_type()
    return render_template('type.html', results=total_data)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        return jsonify({'message': 'Data successfully added!'}), 200
        
    total_data = get_fda_location()
    return render_template('location.html', results=total_data)

def get_next_char(last_char):
    """สร้าง id ถัดไปจากตัวอักษรที่ให้"""
    if last_char in string.ascii_uppercase:
        return chr(ord(last_char) + 1)
    return 'A'

@app.route('/export', methods=['GET', 'POST'])
@login_required
def export():
    return export_report()

if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0', port=8080)