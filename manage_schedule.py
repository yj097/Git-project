from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import platform # 폰트 설정을 위해 추가
import user_settings # user_info를 가져오기 위해 import

schedules = []

# reset_data 함수는 user_settings.py에서 schedules.clear()를 호출하도록 사용됩니다.
# 이 파일 자체에는 새로운 초기화 함수가 필요 없습니다.


def add_schedule(language):
    print("\n[일정 추가]" if language == "ko" else "\n[Add Schedule]")
    date_str = input("날짜 (예: 2025-06-15): " if language == "ko" else "Date (YYYY-MM-DD): ")
    content = input("일정 내용: " if language == "ko" else "Schedule content: ")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        schedules.append({"date": str(date), "content": content, "done": False})
        print("일정이 추가되었습니다." if language == "ko" else "Schedule added.")
    except ValueError:
        print("날짜 형식이 잘못되었습니다." if language == "ko" else "Invalid date format.")

def mark_schedule_done(language):
    print("\n[일정 완료/미완료 표시]" if language == "ko" else "\n[Mark Schedule Done/Undone]")
    if not schedules: # 일정이 없을 때 처리 추가
        print("등록된 일정이 없습니다." if language == "ko" else "No schedules registered.")
        return
    for i, s in enumerate(schedules, start=1):
        status = ("완료" if s["done"] else "미완료") if language == "ko" else ("Done" if s["done"] else "Not Done")
        print(f"{i}. {s['date']} - {s['content']} [{status}]")

    try:
        index = int(input("변경할 일정 번호 입력: " if language == "ko" else "Enter schedule number to toggle status: ")) - 1
        if 0 <= index < len(schedules):
            schedules[index]["done"] = not schedules[index]["done"]
            print("상태가 변경되었습니다." if language == "ko" else "Status updated.")
        else:
            print("유효하지 않은 번호입니다." if language == "ko" else "Invalid number.")
    except ValueError:
        print("숫자를 입력해주세요." if language == "ko" else "Please enter a valid number.")

def view_today_schedule(language):
    today = datetime.now().date()
    print("\n[오늘의 일정]" if language == "ko" else "\n[Today's Schedule]")
    found = False
    for s in schedules:
        if s["date"] == str(today):
            status = "✅" if s["done"] else "❌"
            print(f"- {s['content']} [{status}]")
            found = True
    if not found:
        print("오늘은 일정이 없습니다." if language == "ko" else "No schedule for today.")

def view_week_schedule(language):
    today = datetime.now().date()
    one_week_later = today + timedelta(days=6)

    print("\n[이번 주 일정]" if language == "ko" else "\n[This Week's Schedule]")
    found = False # 이번 주 일정이 있는지 확인하는 플래그 추가
    for s in schedules:
        try:
            date = datetime.strptime(s["date"], "%Y-%m-%d").date()
            if today <= date <= one_week_later:
                status = "✅" if s["done"] else "❌"
                print(f"{s['date']}: {s['content']} [{status}]")
                found = True
        except ValueError:
            continue
    if not found: # 이번 주 일정이 없을 때 메시지 출력
        print("이번 주 일정이 없습니다." if language == "ko" else "No schedules for this week.")


def show_all_schedules_table(language):
    print("\n[전체 일정 요약]" if language == "ko" else "\n[All Schedule Summary]")
    if not schedules:
        print("일정이 없습니다." if language == "ko" else "No schedules.")
        return

    headers = ["날짜", "내용", "상태"] if language == "ko" else ["Date", "Content", "Status"]
    table_data = []
    for s in schedules:
        status = ("완료" if s["done"] else "미완료") if language == "ko" else ("Done" if s["done"] else "Not Done")
        table_data.append([s["date"], s["content"], status])

    # 폰트 설정
    system = platform.system()
    if system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

    # 글씨 크기 설정 (user_settings.user_info에서 가져옴)
    # 기본 폰트 크기를 기준으로 비율 조정
    base_font_size = 12
    current_font_size = user_settings.user_info.get("font_size", base_font_size)
    font_scale_factor = current_font_size / base_font_size

    # 테이블의 세로 크기 조절
    # 행의 개수와 폰트 크기에 비례하여 figure 높이 조정
    fig_height = (0.6 * (len(table_data) + 2)) * font_scale_factor
    fig, ax = plt.subplots(figsize=(10 * font_scale_factor, fig_height)) # 가로 크기도 폰트 크기에 비례하여 조정
    ax.axis('off')
    table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='left')

    table.auto_set_font_size(False)
    # 셀의 글씨 크기를 사용자 설정 폰트 크기에 맞춤
    table.set_fontsize(current_font_size * 0.8)

    # 셀의 높이(y_scale)를 폰트 크기에 비례하여 조정
    # 기본 비율 1.5에 폰트 스케일 팩터를 곱하여 조절
    table.scale(1, 1.5 * font_scale_factor)

    plt.title("전체 일정 요약" if language == "ko" else "All Schedule Summary",
              fontsize=current_font_size * 1.2, pad=20) # 제목 크기 조절
    plt.tight_layout()
    plt.show()

    # 요일별 일정 수 출력 로직 제거
    # day_count = Counter()
    # for s in schedules:
    #     try:
    #         weekday = datetime.strptime(s["date"], "%Y-%m-%d").strftime('%a' if language == "en" else '%a요일')
    #         day_count[weekday] += 1
    #     except ValueError:
    #         continue

    # print("\n[요일별 일정 수]" if language == "ko" else "\n[Schedule Count by Weekday]")
    # days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] if language == "en" else ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    # for day in days:
    #     print(f"{day}: {day_count.get(day, 0)}")

def manage_schedule(language):
    while True:
        print("\n=== 일정 관리 메뉴 ===" if language == "ko" else "\n=== Schedule Management Menu ===")
        print("1. 일정 추가" if language == "ko" else "1. Add Schedule")
        print("2. 오늘 일정 보기" if language == "ko" else "2. View Today's Schedule")
        print("3. 이번 주 일정 보기" if language == "ko" else "3. View This Week's Schedule")
        print("4. 전체 일정 보기 (표 형식)" if language == "ko" else "4. View All Schedules (Figure Table)")
        print("5. 일정 완료/미완료 표시" if language == "ko" else "5. Mark Schedule Done/Undone")
        print("6. 이전 메뉴로" if language == "ko" else "6. Back to Previous Menu")

        choice = input("선택: " if language == "ko" else "Select: ")

        if choice == '1':
            add_schedule(language)
        elif choice == '2':
            view_today_schedule(language)
        elif choice == '3':
            view_week_schedule(language)
        elif choice == '4':
            show_all_schedules_table(language)
        elif choice == '5':
            mark_schedule_done(language)
        elif choice == '6':
            print("\n[이전 메뉴로 돌아가기]" if language == "ko" else "\n[Back to previous menu]")
            break
        else:
            print("잘못된 입력입니다. 1~6 사이의 숫자를 입력해주세요." if language == "ko"
                                     else "Invalid input. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    # manage_schedule.py를 직접 실행할 때 폰트 설정 (없으면 한글 깨짐)
    system = platform.system()
    if system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

    manage_schedule("ko")