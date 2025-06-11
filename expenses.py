# 지출 관리 메뉴
import datetime
from collections import defaultdict
import platform
import matplotlib.pyplot as plt

expenses = []
weekly_budget = None

def input_day_expenses():
    global expenses
    while True:
        date_str = input("지출 날짜를 입력하세요. (YYYY-MM-DD, Enter시 오늘): ")
        if date_str.strip() == '':
            date = datetime.date.today()
            break
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ 날짜 형식이 잘못됐어요! YYYY-MM-DD 형식으로 다시 입력해주세요.")

    print("한 번에 여러 건 입력 (예: 식사 8000)")
    print("엔터만 치면 종료")

    while True:
        line = input("카테고리 금액: ")
        if line.strip() == '':
            break
        try:
            category, amount = line.split()
            amount = int(amount)
            expenses.append({'amount': amount, 'category': category, 'date': date})
            print(f"{category} {amount}원 저장됨.")
        except ValueError:
            print("입력 형식이 잘못됐어요! 예시처럼 '식사 8000' 입력하세요.")
    print(f"✅{date} 지출 입력 완료!\n")

def show_weekly_expenses(): # 이번 주 지출 보기
    print("이번 주 지출 내역")
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())  # 월요일
    this_week_exp = [e for e in expenses if start_of_week <= e['date'] <= today]
    total = sum(e['amount'] for e in this_week_exp)
    for e in this_week_exp:
        print(f"{e['date']} | {e['category']} | {e['amount']}원")
    print(f"총합: {total}원")
    if weekly_budget:
        print(f"예산: {weekly_budget}원")
        remain = weekly_budget - total
        if total > weekly_budget:
            print(f"⚠️ 예산 초과! 과소비 중이에요😥\n{abs(remain):,}원 초과했어요.") #abs = absolute value
        else:
            print(f"👍 예산 내에서 잘 쓰고 있어요! ({remain:,}원 남았어요.)")

def set_budget(): # 예산 설정
    global weekly_budget
    print("주간 예산 설정")
    try:
        weekly_budget = int(input("주간 예산을 입력하세요(원): "))
        print(f"주간 예산이 {weekly_budget:,}원으로 설정되었습니다.\n")
    except ValueError:
        print("숫자로 입력해주세요.")

def menu(): # 메뉴 설정
    while True:
        print("\n===== 지출관리 메뉴 =====")
        print("1. 지출 입력")
        print("2. 이번 주 지출 보기")
        print("3. 예산 설정")
        print("4. 지출 추이 그래프 보기")
        print("5. 이전 메뉴로")
        
        sel = input("번호 선택: ")
        if sel == '5':
            print("이전 메뉴로 돌아갑니다.")
            continue  # 메뉴판 다시 뜨게 하기
        elif sel == '1':
            input_day_expenses()
        elif sel == '2':
            show_weekly_expenses()
        elif sel == '3':
            set_budget()
        elif sel == '4':
            draw_weekly_trend()
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    menu()

#--------------------------------------------------------
# 지출 리포트 (통계)
def report_expenses():
    print("\n[지출 리포트]")
    if not expenses:
        print("지출 내역이 없습니다.")
        return
    total = sum(e['amount'] for e in expenses)
    print(f"총 지출: {total}원")
    by_category = {}
    for e in expenses:
        by_category.setdefault(e['category'], 0)
        by_category[e['category']] += e['amount']
    print("카테고리별 합계:")
    for cat, amt in by_category.items():
        print(f"- {cat}: {amt}원")

# 지출 통계 그래프화
system = platform.system()

if system == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif system == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux, 기타
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False


def get_weekly_expense(expenses):
    weekly_sum = defaultdict(int)
    for e in expenses:
        week_start = e['date'] - datetime.timedelta(days=e['date'].weekday())
        weekly_sum[week_start] += e['amount']

    sorted_weeks = sorted(weekly_sum.items())

    if not sorted_weeks:
        print("📢 이번 주 지출이 없습니다!")
        return [], [] # 비어있을 때 안전하게 처리
    
    weeks, amounts = zip(*sorted_weeks)
    return weeks, amounts

def draw_weekly_trend():
    weeks, amounts = get_weekly_expense(expenses)
    
    if not weeks:
        return  # 지출이 없으면 그래프 안 그림

    trend = []
    for i in range(1, len(amounts)):
        if amounts[i] > amounts[i-1]:
            trend.append("↑")
        elif amounts[i] < amounts[i-1]:
            trend.append("↓")
        else:
            trend.append("→")

    fig, ax = plt.subplots()
    ax.plot(weeks, amounts, marker='o', linewidth=2)
    for i in range(1, len(weeks)):
        ax.text(weeks[i], amounts[i], trend[i-1], color='red', fontsize=14, ha='center')

    ax.set_title('주간 소비 변화 추이')
    ax.set_xlabel('주차')
    ax.set_ylabel('지출 금액')
    ax.tick_params(axis='x', rotation=45)  # x축 레이블 회전
    fig.tight_layout()  # 레이아웃 자동 정리
    plt.show()