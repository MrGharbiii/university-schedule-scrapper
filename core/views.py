from concurrent.futures import ThreadPoolExecutor
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Class
from .forms import ChooseScheduleForm, CheckAvailableClassroomsForm
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
import os

# a schedules_list view where it displays a dropdown box contains list of class and a submit button
# and send the form to schedule_list.html
def schedules_list(request):
    form = ChooseScheduleForm()
    return render(request, 'schedules_list.html', {'form': form})

# a schedule view where it displays the schedule of the selected class and a back button
# and send the schedule to schedule.html
def schedule(request):
    if request.method == 'POST':
        selected_class = request.POST.get('classes')
        try:
            schedule_html = Class.objects.get(name=selected_class).schedule_html
            return HttpResponse(f'<a href="/"><button>Back</button></a><br><br>{schedule_html}')
        except Class.DoesNotExist:
            return render(request, 'error.html')

def get_schedule(selected_class):
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    headers = {
        "Authorization" : TOKEN
    }
    print("Getting schedule of " + selected_class)
    try:
        response = requests.get(f'https://issatso.rnu.tn/bo/public/api/student/timetable/{selected_class}', headers=headers)
        json_response = response.json()
        schedule = json_response['html']
        return schedule
    except ConnectionError:
        return None

# check_available_classrooms view
def check_available_classrooms(request):
    available_classrooms = [
                      'Amphi: GOLLI Salem',  'Amphi: LAATIRI Mokhtar', 'B08-A', 'B09', 'B10',
                      'B16', 'F01', 'F02', 'F03', 'F05', 'G01', 'G02', 'G03', 'G04', 'G05',
                      'G06', 'G07', 'G08', 'G10', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17',
                      'G18', 'G19', 'G20', 'G21', 'H01', 'H02', 'H03', 'H04', 'H05', 'H06',
                      'H07', 'H08', 'H09', 'H10', 'H11', 'H12', 'H13', 'H14', 'I-02', 'I-03',
                      'I-04', 'I-05', 'I-06', 'I-07', 'I-08', 'I-09', 'I-10', 'I-11', 'I-12',
                      'I-13', 'I-14', 'I-15', 'I-16', 'I-17', 'I-18', 'I-19', 'J05', 'J06', 'J07',
                      'J08', 'J09', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K09',
                      'K10', 'K11', 'K12', 'K13', 'L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'M01',
                      'M01-1', 'M01-2', 'M01-3', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08',
                      'M09', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18-1', 'M18-2'
                    ]
    
    weekday = request.GET.get('weekday')
    session = request.GET.get('session')

    if session == "S4'":
        if weekday != "6-Samedi":
            return HttpResponse("<center><h2>S4' is only available on Saturday</h2></center><a href='check_available_classrooms_form'><button>Back</button></a>")
    departments = {}
    total = 0
    classes = Class.objects.all()
    for class_ in classes:
        occupied_classrooms = class_.occupied_classrooms.replace("'", '"').replace("\"S4\"\"", "\"S4'\"")
        occupied_classrooms = json.loads(occupied_classrooms)
        if weekday in occupied_classrooms and session in occupied_classrooms[weekday]:
            total += 1
            for occupied_classroom in occupied_classrooms[weekday][session]:
                if occupied_classroom in available_classrooms:
                    available_classrooms.remove(occupied_classroom)
    for classroom in sorted(available_classrooms):
        if classroom[0] in departments:
            departments[classroom[0]].append(classroom)
        else:
            departments[classroom[0]] = [classroom]
    html_table = "<table border=1><tr><th>Department</th><th>Classrooms</th></tr>"
    for department in departments:
        html_table += f"<tr><td>{department}</td><td>{', '.join(departments[department])}</td></tr>"
    html_table += "</table>"
    return HttpResponse(f'<a href="/check_available_classrooms_form"><button>Back</button></a> \
        <br><br><center><h3> A total of {total}/{len(classes)} group studies in "{weekday[2:]}" {session} </h3><br>{html_table}</center>')

# check_available_classrooms form
def check_available_classrooms_form(request):
    form = CheckAvailableClassroomsForm()
    return render(request, 'check_available_classrooms_form.html', {'form': form})

def html_parse(schedule_html):
    weekdays = ["1-Lundi", "2-Mardi", "3-Mercredi", "4-Jeudi", "5-Vendredi", "6-Samedi"]
    sessions = ["S1", "S2", "S3", "S4", "S4'", "S5", "S6"]
    occupied_classrooms = {}
    soup = BeautifulSoup(schedule_html, features="html5lib")
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            classroom = cells[6].text
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
    
# a view to update the schedules in the database
def update_schedules(request):
    classes = ["ING-A1-01","ING-A1-02","ING-A1-03","ING-A1-04",
                  "ING-A1-05","ING-A2-GL-01","ING-A2-GL-02","ING-A2-GL-03",
                  "ING-A2-GL-04","ING-A3-GL-AL-01","ING-A3-GL-AL-02","ING-A3-GL-AL-03",
                  "ING-A3-GL-AL-04","LEEA-A1-01","LEEA-A1-02","LEEA-A1-03","LEEA-A1-04",
                  "LEEA-A1-05","LEEA-A1-06","LEEA-A1-07","LEEA-A2-AII-01","LEEA-A2-EI-01",
                  "LEEA-A2-SE-01","LEEA-A2-SE-02","LEEA-A2-SE-03","LEEA-A3-AII-01","LEEA-A3-EI-01",
                  "LEEA-A3-SE-01","LEEA-A3-SE-02","LEM-A1-01","LEM-A1-02","LEM-A1-03","LEM-A1-04",
                  "LEM-A2-MA-01","LEM-A2-MA-02","LEM-A2-MI-01","LEM-A3-MA-01","LEM-A3-MA-02",
                  "LEM-A3-MI-01","LGC-A1-01","LGC-A1-02","LGC-A1-03","LGC-A1-04","LGC-A2-BAT-01",
                  "LGC-A2-BAT-02","LGC-A2-PC-01","LGC-A2-PC-02","LGC-A3-BAT-01","LGC-A3-BAT-02",
                  "LGC-A3-PC-01","LGEnerg-A1-01","LGEnerg-A1-02","LGEnerg-A1-03","LGEnerg-A2-01",
                  "LGEnerg-A2-02","LGEnerg-A3-01","LGEnerg-A3-02","LGEnerg-A3-03","LGM-A1-01",
                  "LGM-A1-02","LGM-A1-03","LGM-A2-CPI-01","LGM-A2-CPI-02","LGM-A2-PROD-01",
                  "LGM-A3-PROD-01","LGM-A3-CPI-01","LGM-A3-CPI-02","LISI-A1-01","LISI-A1-02",
                  "LISI-A1-03","LISI-A2-01","LISI-A2-02","LISI-A3-01","LISI-A3-02","LSI-A1-01",
                  "LSI-A1-02","LSI-A2-01","LSI-A2-02","LSI-A3-01","LSI-A3-02","MP-MERE-A1-01",
                  "MP-ENG-A2-01","MP-GM-A1-01","MP-GM-A2-GPPM-01","MR-GM-A1-01","MR-GM-A2-MM-01",
                  "MR-GM-A2-SM-01","MR-SPI-A1-01","MR-SPI-A2-01","MR-MDEP-A2-01","MR-A1-MSEE-SEE-01",
                  "MR-A1-MSEE-MSE-01","MR-A1-MSEE-MDEP-01","MR-SEE-A2-01","Prepa-A1-01",
                  "Prepa-A1-02","Prepa-A1-03","Prepa-A1-04","Prepa-A2-01","Prepa-A2-02",
                  "Prepa-A2-03","Prepa-A2-04","MP-MERE-A1-01","MP-ENG-A1-01"
                ]
    with ThreadPoolExecutor(max_workers=len(classes)) as executor:
        executor.map(store_schedule, classes)
    return HttpResponse("<h1>Schedules Updated!</h1> <br><br><a href='/'><button>Back</button></a>")

def store_schedule(_class):
    schedule_html = get_schedule(_class)
    if schedule_html != None:
        if Class.objects.filter(name=_class).exists():
            _class = Class.objects.get(name=_class)
            _class.schedule_html = schedule_html
            _class.occupied_classrooms = html_parse(schedule_html)
            _class.save()
        else:
            Class(name=_class, schedule_html=schedule_html, occupied_classrooms=html_parse(schedule_html)).save()
