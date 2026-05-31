import sqlite3
from datetime import date
from Login_Signup import DB_PATH


def make_year_string(start_year):
    end_year = (start_year + 1) % 100
    return f"{start_year}/{end_year:02d}"


def current_school_year():
    today = date.today()
    start = today.year if today.month >= 9 else today.year - 1
    return make_year_string(start)


def parse_start_year(year_string):
    return int(year_string.split('/')[0])



