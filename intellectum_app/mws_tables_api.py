import json
from dotenv import load_dotenv
from os import getenv
from requests import request
from .schemas import Student

load_dotenv()

DATASHEET_IDS = {
    "students": "dstgC1DwDVLzS0KryX",
    "lessons": "dstufz2x55j01KYBK2",
    "top_ups": "dstvtWEMyQSkTpykyG",
}

def add_record_to_datasheet(datasheet: str, data: list[dict]) -> dict:
    datasheet_id = DATASHEET_IDS.get(datasheet)
    if not datasheet_id:
        return {}

    url = f"https://true.tabs.sale/fusion/v1/datasheets/{datasheet_id}/records"

    headers = {
        "Authorization": f"Bearer {getenv("MWS_TABS_KEY")}",
        "Content-Type": "application/json"
    }

    print([{"fields": datum} for datum in data].__len__())
    print(data[0])
    print({"records": [{"fields": datum} for datum in data]})
    
    return request(method="POST", url=url, headers=headers, data=json.dumps({"records": [{"fields": datum} for datum in data]})).json()

def create_student(student: Student) -> dict:
    return add_record_to_datasheet("students", [student.model_dump(by_alias=True)])

def get_records_from_datasheet(datasheet: str) -> list[dict]:
    datasheet_id = DATASHEET_IDS.get(datasheet)
    if not datasheet_id:
        return []
    
    url = f"https://true.tabs.sale/fusion/v1/datasheets/{datasheet_id}/records"
    
    headers = {
        "Authorization": f"Bearer {getenv("MWS_TABS_KEY")}",
    }

    return request(method="GET", url=url, headers=headers, params={"fieldKey": "id"}).json()["data"]["records"]

def get_lessons_for_student(student_rec_id: str) -> list[dict]:
    response = get_records_from_datasheet("lessons")
    return list(filter(lambda l: student_rec_id in l["fields"]["fld98SwF8tOUJ"], response))

def get_top_ups_for_student(student_rec_id: str) -> list[dict]:
    response = get_records_from_datasheet("top_ups")
    return list(filter(lambda l: student_rec_id in l["fields"]["fld7lnHxXWYC4"], response))
