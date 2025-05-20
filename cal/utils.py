from datetime import datetime, timedelta # 날짜와 시간 처리를 위한 모듈
from calendar import HTMLCalendar # 모듈에서 제공하는 html 형식의 캘린더를 생성하는 클래스
from .models import Game # 현재 모델에서 불러온 클래스 
import os
import django
import sys

# calemdar 클래스는 __init__, formatday, formatweek, formatmonth 네 가지의 내장 함수를 가짐짐
class Calendar(HTMLCalendar): # calemdar 클래스는 htmlcalendar를 상속받아 특정 연도와 월을 받아 캘린더를 생성하도록함
    def __init__(self, year = None, month=None): # __init__ 메서드에서 year와 month를 받아서 인스턴스 변수로 저장
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, games): # day 현재 날짜, contents : 현재 달의 모든 일정 데이터 
        games_per_day = games.filter(date__day = day) # 현재 날짜에 해당하는 일정만 필터링링
        d = ''
        for game in games_per_day: # 필터링된 일정들을 event로 순회하면서 html 리스트 아이템(li)로 만들어서 d에 추가 
            d += f'<li> {game.away_team} vs {game.home_team} at {game.stadium} </li> ' 
        # 필터링한 game 모델의 데이터를 games라는 인자로 받아서 해당 날짜에 대한 game 일정을 출력함함
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    
    # 달력에서 주를 형식화하는 함수로, theweek와 contents를 인자로 받아 각 날짜에 대해 formatday 함수를 호출하여 출력함
    def formatweek(self, theweek, games):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, games)
        return f'<tr> {week} </tr>'
    
    # withyear = True는 연도를 포함한 형식으로 출력함, 이 함수는 game모델의 데이터를 필터링하여 해당 월에 대한 달력을 출력하고 메서드를 호출하여 달력을 생성성
    def formatmonth(self, withyear = True):
        games = Game.objects.filter(date__year = self.year, date__month=self.month)
        cal = f'<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"calendar\">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, games)}\n'
        return cal
    
# def import_kbo_schedule_from_csv(file_path):
