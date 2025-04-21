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
    "homework": "dstKNG7XY7pAdr7LP6",
    "courses": "dstqBysSoJQWseAAfL",
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
    return list(filter(lambda l: student_rec_id in l["fields"].get("fld98SwF8tOUJ", []), response))

def get_top_ups_for_student(student_rec_id: str) -> list[dict]:
    response = get_records_from_datasheet("top_ups")
    return list(filter(lambda l: student_rec_id in l["fields"]["fld7lnHxXWYC4"], response))

def get_homework_for_student(student_rec_id: str) -> list[dict]:
    response = get_records_from_datasheet("homework")
    return list(filter(lambda h: student_rec_id in h["fields"].get("fldEp1BDv27bY", []), response))

def get_courses() -> list[dict]:
    return get_records_from_datasheet("courses")

def add_solution_file_to_homework(student_id: str, homework_id: str, file):
    print(file.name)
    url = "https://true.tabs.sale/fusion/v1/datasheets/dstKNG7XY7pAdr7LP6/attachments"
    
    headers = {
        "Authorization": f"Bearer {getenv("MWS_TABS_KEY")}",
        # "Content-Type": "multipart/form-data"
    }
    
    response = request("POST", url=url, headers=headers, files={"file": (file.name, file)})
    print(response.text)
    response = response.json()
    if not response["success"]:
        print(response)
        return

    headers["Content-Type"] = "application/json"
    url = "https://true.tabs.sale/fusion/v1/datasheets/dstKNG7XY7pAdr7LP6/records"
    print("uploaded attachment")
    print(response)
    print("attachment id:", response["data"]["id"])


    response = request("PATCH", url=url, headers=headers, data=json.dumps(
        {
            "records": [
                {
                    "recordId": homework_id,
                    "fields": {
                        "fldnGDxeNPH3s": [response["data"]]
                    }
                }
            ]
        }
    )).json()

    if not response["success"]:
        print(response)

