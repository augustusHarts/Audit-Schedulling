from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_DIR = DATA_DIR / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_DIR = DATA_DIR / 'processed'
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

MASTER_DIR = DATA_DIR / 'master'
MASTER_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = DATA_DIR / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FORMAT = (
    "%(asctime)s |"
    "%(levelname)-8s |"
    "%(name)s |"
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

FILE_NAME = ['auditors', 'holidays', 'branches', 'history', 'lat_long'] 

FILE_MAP = {
   "auditors": "listofauditors.xlsx",
   "holidays": "holidaydata.xlsx",
   "branches": "branch list for audit.xlsx",
   "history": "auditors_auditedlast5yrs.xlsx",
   "lat_long": "Lat long data.xlsx"
}

VALID_CIRCLES = {
    "AHMEDABAD",
    "AMARAVATI",
    "BENGALURU",
    "BHOPAL",
    "BHUBANESWAR",
    "CHANDIGARH",
    "CHENNAI",
    "DELHI",
    "GUWAHATI",
    "HYDERABAD",
    "JAIPUR",
    "KOLKATA",
    "LUCKNOW",
    "MUMBAI",
    "PATNA",
    "THIRUVANANTHAPURAM",
}


CIRCLE_MAPPING = {
    "HYDARABAD": "HYDERABAD",
    "AMARAVATHI": "AMARAVATI",
    "AMRAVATI": "AMARAVATI",
    "BHUBANESHWAR": "BHUBANESWAR",
    "BANGALORE": "BENGALURU",
    "CALCUTTA": "KOLKATA",
}

EXCEL_EPOCH = pd.Timestamp("1899-12-30")

QUARTER = "Q1"
FOREX_CATEGORY = ["B"]
CATEGORY = ['TRADE', 'RETAIL']

# HOLIDAY_MAPPING = {
#     "MUMBAI": "MAHARASHTRA",
#     "PUNE": "MAHARASHTRA",
#     "NAGPUR": "MAHARASHTRA",
#     "HYDERABAD": "TELANGANA",
#     "HYDARABAD": "TELANGANA",
#     'COMMERCIAL CLIENT GROUP': 'CCG',
#     'AHMEDABAD': 'GUJARAT',
#     'CHENNAI': 'TAMILNADU',
#     'NEW DELHI': 'DELHI',
#     'THIRUVANANTHAPURAM': 'KERALA',
#     'CHANDIGARH': 'CHANDIGARH',
#     'MAHARASHTRA': 'MAHARASHTRA',
#     'BENGALURU': 'KARNATAKA',
#     "BANGALORE" : 'KARNATAKA',
#     'MUMBAI METRO': 'MAHARASHTRA',
#     'AMRAVATI': 'MAHARSHATRA',
#     'LUCKNOW': 'UTTAR PRADESH',
#     'JAIPUR': 'RAJASTHAN',
#     'KOLKATA': 'WEST BENGAL',
#     'BHOPAL': 'MADHYA PRADESH',
#     'GUWAHATI': 'ASSAM',
#     'BHUBANESHWAR': 'ODISHA',
#     "BHUBANESWAR": 'ODISHA',
#     'PATNA': 'BIHAR',
#     'AMARAVATI': 'MAHARASHTRA',
#     "AMARAVATHI": "MAHARASHTRA",
# }