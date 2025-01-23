#오후 쉬는시간 알리미 

import time
import datetime
import winsound
from tkinter import *
from tkinter import ttk

class DailyTimer:
    def __init__(self):
        self.window = Tk()
        self.window.title("Study Timer")
        self.window.geometry("400x650")
        self.window.configure(bg='#1e1e2e')
        
        # 색상 테마
        self.colors = {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'accent': '#89b4fa',
            'warning': '#f38ba8',
            'success': '#a6e3a1',
            'surface': '#313244',
            'button': '#45475a',
            'button_active': '#585b70'
        }
        
        # 타이머 상태
        self.is_running = True
        
        self.create_widgets()
        self.check_time()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # 상단 시계 프레임
        clock_frame = Frame(main_frame, bg=self.colors['surface'], height=150)
        clock_frame.pack(fill='x', pady=(0, 20))
        clock_frame.pack_propagate(False)
        
        # 현재 시간 표시
        self.time_label = Label(
            clock_frame,
            font=("Helvetica", 48, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['fg']
        )
        self.time_label.pack(expand=True)
        
        # 날짜 표시
        self.date_label = Label(
            clock_frame,
            font=("Helvetica", 12),
            bg=self.colors['surface'],
            fg=self.colors['accent']
        )
        self.date_label.pack(pady=(0, 20))
        
        # 구분선
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=20)
        
        # 상태 프레임
        status_frame = Frame(main_frame, bg=self.colors['surface'], height=150)
        status_frame.pack(fill='x', pady=(0, 20))
        status_frame.pack_propagate(False)
        
        # 상태 표시
        self.status_label = Label(
            status_frame,
            text="대기 중",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['success']
        )
        self.status_label.pack(expand=True)
        
        # 다음 알림 시간 표시
        self.next_alarm_label = Label(
            status_frame,
            font=("Helvetica", 14),
            bg=self.colors['surface'],
            fg=self.colors['accent']
        )
        self.next_alarm_label.pack(pady=(0, 20))
        
        # 정보 프레임
        info_frame = Frame(main_frame, bg=self.colors['surface'])
        info_frame.pack(fill='x', pady=(0, 20))
        
        # 운영시간 정보
        Label(
            info_frame,
            text="운영 시간",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['fg']
        ).pack(pady=(20, 5))
        
        Label(
            info_frame,
            text="13:00 - 18:00",
            font=("Helvetica", 20),
            bg=self.colors['surface'],
            fg=self.colors['accent']
        ).pack(pady=(0, 20))
        
        # 간격 정보
        Label(
            info_frame,
            text="알림 간격",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['fg']
        ).pack(pady=(5, 5))
        
        Label(
            info_frame,
            text="50분",
            font=("Helvetica", 20),
            bg=self.colors['surface'],
            fg=self.colors['accent']
        ).pack(pady=(0, 20))
        
        # 버튼 프레임 추가 (info_frame 다음에 추가)
        button_frame = Frame(main_frame, bg=self.colors['surface'])
        button_frame.pack(fill='x', pady=(0, 20))
        
        # 중지/시작 버튼
        self.toggle_button = Button(
            button_frame,
            text="타이머 중지",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['button'],
            fg=self.colors['fg'],
            activebackground=self.colors['button_active'],
            activeforeground=self.colors['fg'],
            relief='flat',
            command=self.toggle_timer,
            width=20,
            height=2
        )
        self.toggle_button.pack(pady=20)
    
    def is_working_hours(self, time):
        return 13 <= time.hour < 18
    
    def get_next_alarm_time(self):
        now = datetime.datetime.now()
        
        # 13시 이전이면 13시 50분으로 설정
        if now.hour < 13:
            return now.replace(hour=13, minute=50, second=0, microsecond=0)
        
        # 18시 이후면 다음날 13시 50분으로 설정
        if now.hour >= 18:
            tomorrow = now + datetime.timedelta(days=1)
            return tomorrow.replace(hour=13, minute=50, second=0, microsecond=0)
        
        # 현재 시각이 속한 시간의 50분을 지났으면 다음 시간의 50분으로 설정
        current_alarm = now.replace(minute=50, second=0, microsecond=0)
        if now >= current_alarm:
            if now.hour == 17:  # 17시 50분 이후라면 다음날 13시 50분
                tomorrow = now + datetime.timedelta(days=1)
                return tomorrow.replace(hour=13, minute=50, second=0, microsecond=0)
            else:
                return now.replace(hour=now.hour + 1, minute=50, second=0, microsecond=0)
        
        return current_alarm
    
    def play_alarm(self):
        for _ in range(3):
            winsound.Beep(1000, 500)
            time.sleep(0.2)
    
    def toggle_timer(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.toggle_button.config(text="타이머 중지")
            self.status_label.config(text="알림 실행 중")
        else:
            self.toggle_button.config(text="타이머 시작")
            self.status_label.config(text="일시 중지됨", fg=self.colors['warning'])
    
    def check_time(self):
        now = datetime.datetime.now()
        
        # 현재 시간 업데이트
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%Y년 %m월 %d일"))
        
        next_alarm = self.get_next_alarm_time()
        
        # 상태 업데이트
        if not self.is_running:
            self.status_label.config(
                text="일시 중지됨",
                fg=self.colors['warning']
            )
        elif 13 <= now.hour < 18:
            self.status_label.config(
                text="알림 실행 중",
                fg=self.colors['success']
            )
            self.next_alarm_label.config(
                text=f"다음 알림: {next_alarm.strftime('%H:%M')}",
                fg=self.colors['accent']
            )
        else:
            if now.hour < 13:
                self.status_label.config(
                    text="13시에 시작됩니다",
                    fg=self.colors['warning']
                )
            else:
                self.status_label.config(
                    text="오늘 알림 종료",
                    fg=self.colors['warning']
                )
            self.next_alarm_label.config(
                text="다음 알림: 다음날 13:50",
                fg=self.colors['accent']
            )
        
        # 알림 체크 (타이머가 실행 중일 때만)
        if self.is_running and 13 <= now.hour < 18 and now.minute == 50 and now.second == 0:
            self.play_alarm()
        
        self.window.after(1000, self.check_time)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DailyTimer()
    app.run()

