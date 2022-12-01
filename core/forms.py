from django import forms

class ChooseScheduleForm(forms.Form):
    classes = [(_class, _class) for _class in ["ING-A1-01","ING-A1-02","ING-A1-03","ING-A1-04",
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
                ]]
    classes = forms.ChoiceField(choices=classes)

class CheckAvailableClassroomsForm(forms.Form):
  weekdays = [weekday for weekday in [("1-Lundi", "Lundi"), ("2-Mardi", "Mardi"), ("3-Mercredi", "Mercredi"),
                ("4-Jeudi", "Jeudi"), ("5-Vendredi", "Vendredi"), ("6-Samedi", "Samedi")]]
  weekday = forms.ChoiceField(choices=weekdays)
  sessions = [session for session in [("S1", "S1"), ("S2", "S2"), ("S3", "S3"), ("S4", "S4"), ("S4'", "S4'"), ("S5", "S5"), ("S6", "S6")]]
  session = forms.ChoiceField(choices=sessions)

class CheckClassroomAvailabilityForm(forms.Form):
  classrooms = [(_classroom, _classroom) for _classroom in [
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
                    ]]
  classroom = forms.ChoiceField(choices=classrooms)
  


