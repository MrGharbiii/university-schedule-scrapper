from bs4 import BeautifulSoup
from .models import Class
import requests
import json
import os


def get_schedule(url, selected_class):
    TOKEN = os.getenv('TOKEN')
    headers = {
        "Authorization" : TOKEN
    }
    print("Getting schedule of " + selected_class)
    try:
        response = requests.get(f'{url}{selected_class}', headers=headers)
        json_response = response.json()
        schedule = json_response['html']
        return schedule
    except ConnectionError:
        return None

def html_parse(schedule_html):
    weekdays = ["1-Lundi", "2-Mardi", "3-Mercredi", "4-Jeudi", "5-Vendredi", "6-Samedi"]
    sessions = ["S1", "S2", "S3", "S4", "S4'", "S5", "S6"]
    occupied_classrooms = {}
    soup = BeautifulSoup(schedule_html, features="html5lib")
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        try:
            classroom = cells[6].text
        except:
            continue
        for cell in cells:
            if cell.text in weekdays and not cell.text in occupied_classrooms:
                weekday = cell.text
                occupied_classrooms[weekday] = {}
                break
            elif cell.text in sessions:
                session = cell.text
                if session in occupied_classrooms[weekday]: 
                    occupied_classrooms[weekday][session] += [classroom]
                else:
                    occupied_classrooms[weekday][session] = [classroom]
                    break
    return occupied_classrooms

def rattrapage_html_parse(schedule_html):
    weekdays = {
        "Lundi" : "1-Lundi",
        "Mardi" : "2-Mardi",
        "Mercredi": "3-Mercredi",
        "Jeudi": "4-Jeudi",
        "Vendredi": "5-Vendredi",
        "Samedi": "6-Samedi"
    }
    sessions = ["S1", "S2", "S3", "S4", "S4'", "S5", "S6"]
    rattrapage_occupied_classrooms = {}
    soup = BeautifulSoup(schedule_html, features="html5lib")
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        try:
            classroom = cells[5].text
        except:
            continue
        for cell in cells:
            if cell.text in weekdays and not cell.text in rattrapage_occupied_classrooms:
                weekday = weekdays[cell.text]
                rattrapage_occupied_classrooms[weekday] = {}
            elif cell.text in sessions:
                session = cell.text
                if session in rattrapage_occupied_classrooms[weekday]: 
                    rattrapage_occupied_classrooms[weekday][session] += [classroom]
                else:
                    rattrapage_occupied_classrooms[weekday][session] = [classroom]
    return rattrapage_occupied_classrooms

def parse_str_occupied_classrooms_to_json(occupied_classrooms_str):
    occupied_classrooms = occupied_classrooms_str.replace("'", '"').replace("\"S4\"\"", "\"S4'\"")
    occupied_classrooms = json.loads(occupied_classrooms)
    return occupied_classrooms

def classroom_availability_in_the_week(classroom):
    classes = Class.objects.all()
    classroom_availability = {}
    for _class in classes:
        occupied_classrooms = parse_str_occupied_classrooms_to_json(_class.occupied_classrooms)
        if occupied_classrooms:
            for weekday in occupied_classrooms:
                if weekday not in classroom_availability:
                    classroom_availability[weekday] = {}
                for session in occupied_classrooms[weekday]:
                    if session not in classroom_availability[weekday]:
                        classroom_availability[weekday][session] = "Free"
                    if classroom in occupied_classrooms[weekday][session]:
                        classroom_availability[weekday][session] = "Occupied"
    return classroom_availability

def store_schedule(_class):
    schedule_html = get_schedule(os.getenv("SCHEDULE_URL"), _class)
    rattrapage_html = get_schedule(os.getenv("RATTRAPAGE_URL"), _class)
    if schedule_html != None or rattrapage_html != None:
        if Class.objects.filter(name=_class).exists():
            _class = Class.objects.get(name=_class)
            _class.schedule_html = schedule_html
            _class.occupied_classrooms = merge_schedules_and_their_rattrapage(
                html_parse(schedule_html),
                rattrapage_html_parse(rattrapage_html)
            )
            _class.save()
        else:
            Class(name=_class, schedule_html=schedule_html, occupied_classrooms=merge_schedules_and_their_rattrapage(html_parse(schedule_html), rattrapage_html_parse(rattrapage_html))).save()


def merge_schedules_and_their_rattrapage(occupied_classrooms, rattrapage_occupied_classrooms):
    if rattrapage_occupied_classrooms:
        for rattrapage_weekday in rattrapage_occupied_classrooms:
            if rattrapage_weekday in occupied_classrooms:
                for rattrapage_session in rattrapage_occupied_classrooms[rattrapage_weekday]:
                    if rattrapage_session in occupied_classrooms[rattrapage_weekday]:
                         occupied_classrooms[rattrapage_weekday][rattrapage_session] += rattrapage_occupied_classrooms[rattrapage_weekday][rattrapage_session]
                    else:
                         occupied_classrooms[rattrapage_weekday][rattrapage_session] = rattrapage_occupied_classrooms[rattrapage_weekday][rattrapage_session]
            else:
                occupied_classrooms[rattrapage_weekday] = rattrapage_occupied_classrooms[rattrapage_weekday]
    return occupied_classrooms