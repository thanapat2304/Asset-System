from backend.db_connection import connect_aep_portal
import random

def get_fda_type():
    sample_data = []
    type_names = ["ครุภัณฑ์สำนักงาน", "อุปกรณ์อิเล็กทรอนิกส์", "เครื่องจักร", "ยานพาหนะ", "เฟอร์นิเจอร์"]

    selected_types = random.sample(type_names, k=min(5, len(type_names)))  # สุ่มไม่ซ้ำ

    for i, type_name in enumerate(selected_types, start=1):
        row = {
            "Account_code": f"ACC{random.randint(100, 999)}",
            "AS_Name_type": type_name,
            "Percent": random.choice([10, 15, 20, 25, 30]),
            "Depreciation_rate": random.choice([3, 5, 7, 10])
        }
        sample_data.append(row)

    return sample_data