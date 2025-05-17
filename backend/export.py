from flask import render_template, request
from backend.db_connection import connect_aep_portal
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

def get_branch():
    branch_names = ["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต", "สาขาขอนแก่น", "สาขาหาดใหญ่"]
    
    branches = [
        {"id": f"BR{idx}", "AS_Name_Branch": name}
        for idx, name in enumerate(branch_names, start=1)
    ]
    
    branches.insert(0, {"id": "ทั้งหมด", "AS_Name_Branch": "ทั้งหมด"})

    return branches

def get_type():
    type_names = ["ครุภัณฑ์สำนักงาน", "อุปกรณ์อิเล็กทรอนิกส์", "เครื่องจักร", "ยานพาหนะ", "เฟอร์นิเจอร์"]
    
    types = [
        {"id": f"T{i}", "AS_Name_type": name}
        for i, name in enumerate(type_names, start=1)
    ]
    
    types.insert(0, {"id": "ทั้งหมด", "AS_Name_type": "ทั้งหมด"})
    
    return types

def get_years():
    current_year = datetime.now().year
    start_year = 2024
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(start_year, current_year + 1)]
    years.insert(0, {'id': 'ทั้งหมด', 'AS_Name_year': 'ทั้งหมด'})
    return years

def execute_export_query(selected_branchr, selected_type, selected_year):
    branches = {
        "BR1": "สาขากรุงเทพ",
        "BR2": "สาขาเชียงใหม่",
        "BR3": "สาขาภูเก็ต",
        "BR4": "สาขาขอนแก่น",
        "BR5": "สาขาหาดใหญ่",
    }
    
    types = {
        "T1": "ครุภัณฑ์สำนักงาน",
        "T2": "อุปกรณ์อิเล็กทรอนิกส์",
        "T3": "เครื่องจักร",
        "T4": "ยานพาหนะ",
        "T5": "เฟอร์นิเจอร์",
    }
    
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    sample_results = []
    
    for _ in range(20):
        branch_id = random.choice(list(branches.keys()))
        type_id = random.choice(list(types.keys()))
        yr = random.choice(years)
        
        as_date = datetime.now().date() - timedelta(days=random.randint(0, 1000))
        save_time = datetime.now() - timedelta(days=random.randint(0, 1000))
        
        row = (
            save_time.strftime("%Y-%m-%d %H:%M:%S"),   # AS_Save_Time
            f"AC{random.randint(1000,9999)}",          # Asset_Code
            yr,                                        # YR
            f"ACC{random.randint(10000,99999)}",       # Account_Num
            types[type_id],                            # AS_Type_Name
            branches[branch_id],                       # AS_Location_Name
            random.choice(["เครื่องคอมพิวเตอร์", "โต๊ะทำงาน", "เก้าอี้"]),  # Asset_Name
            f"รายละเอียดทรัพย์สินที่ {random.randint(1, 100)}",            # AS_Detail
            as_date,                                  # AS_Date (date object)
            round(random.uniform(1000, 50000), 2),   # Asset_Value
            random.choice(["โกดัง 1", "โกดัง 2", "สำนักงาน"]),            # AS_Store
            "โน้ตเพิ่มเติมบางอย่าง",                  # AS_Note
            random.choice(["ไอที", "บัญชี", "การตลาด"]),                 # Department
            f"user{random.randint(1,50)}",             # AS_User
            f"SN{random.randint(100000,999999)}",      # AS_SerialNum
            f"ผู้บันทึก{random.randint(1,20)}",       # AS_Save_Name
            random.choice(["ตัดค่าเสื่อมแล้ว", "ยังไม่ตัดค่าเสื่อม"])      # Status
        )
        sample_results.append(row)
    
    sample_results.sort(key=lambda x: x[8], reverse=True)
    
    formatted_results = []
    for row in sample_results:
        purchase_date = row[8]
        if isinstance(purchase_date, date):
            today = date.today()
            difference = relativedelta(today, purchase_date)
            age_str = f"{difference.years} ปี {difference.months} เดือน {difference.days} วัน"
        else:
            age_str = "ไม่ทราบวันที่"
        formatted_results.append(row + (age_str,))
    
    return formatted_results

def get_selected_branch_info(selected_branch):
    branches = {
        "BR1": "สาขากรุงเทพ",
        "BR2": "สาขาเชียงใหม่",
        "BR3": "สาขาภูเก็ต",
        "BR4": "สาขาขอนแก่น",
        "BR5": "สาขาหาดใหญ่",
        "ทั้งหมด": "ทั้งหมด"
    }
    
    return branches.get(selected_branch)

def get_selected_type_info(selected_type):
    types = {
        "T1": "ครุภัณฑ์สำนักงาน",
        "T2": "อุปกรณ์อิเล็กทรอนิกส์",
        "T3": "เครื่องจักร",
        "T4": "ยานพาหนะ",
        "T5": "เฟอร์นิเจอร์",
        "ทั้งหมด": "ทั้งหมด"
    }
    
    return types.get(selected_type)

def export_report():
    branch = get_branch()
    type = get_type()
    year = get_years()

    results = None
    selected_branch = None
    selected_type = None
    selected_year = None
    selected_branch_info = None
    selected_type_info = None
    formatted_total_count = "0"
    formatted_total_sum = "0.00"

    if request.method == 'POST':
        selected_branch = request.form['branch']
        selected_type = request.form['type']
        selected_year = request.form['year']
        results = execute_export_query(selected_branch, selected_type, selected_year)
        selected_branch_info = get_selected_branch_info(selected_branch)
        selected_type_info = get_selected_type_info(selected_type)

        total_count = len(results) if results else 0
        formatted_total_count = "{:,}".format(total_count)

        total_sum = sum(row[9] for row in results if row[9] is not None)
        formatted_total_sum = "{:,.2f}".format(total_sum)

    return render_template(
        'export.html',
        branch=branch,
        type=type,
        year=year,
        results=results,
        selected_branch=selected_branch,
        selected_type=selected_type,
        selected_year=selected_year,
        formatted_total_count=formatted_total_count,
        formatted_total_sum=formatted_total_sum,
        selected_branch_info=selected_branch_info,
        selected_type_info=selected_type_info
    )