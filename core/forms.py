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

class CheckUnavailableClassroomsForm(forms.Form):
  weekdays = [weekday for weekday in [("1-Lundi", "Lundi"), ("2-Mardi", "Mardi"), ("3-Mercredi", "Mercredi"),
                ("4-Jeudi", "Jeudi"), ("5-Vendredi", "Vendredi"), ("6-Samedi", "Samedi")]]
  weekday = forms.ChoiceField(choices=weekdays)
  sessions = [session for session in [("S1", "S1"), ("S2", "S2"), ("S3", "S3"), ("S4", "S4"), ("S4'", "S4'"), ("S5", "S5"), ("S6", "S6")]]
  session = forms.ChoiceField(choices=sessions)


