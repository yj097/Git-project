import datetime
from collections import defaultdict
import platform
import matplotlib.pyplot as plt
import user_settings # user_info를 가져오기 위해 import

LANG = {
    "ko": {
        "menu_title": "지출관리 메뉴",
        "input_date": "지출 날짜를 입력하세요. (YYYY-MM-DD, Enter시 오늘, q 입력시 이전 메뉴): ",
        "multi_input_hint": "한 번에 여러 건 입력 (예: 식사 8000)\n엔터만 치면 종료 / 'q' 입력 시 이전 메뉴로 돌아감",
        "category_amount": "카테고리 금액: ",
        "saved": "{} {}원 저장됨.",
        "complete": "✅ {date} 지출 입력 완료!\n",
        "weekly_view": "이번 주 지출 내역",
        "confirm_prompt": "확인하려면 Enter, 이전 메뉴로 가려면 q 입력: ",
        "total": "총합: {total}원",
        "budget": "예산: {budget}원",
        "over": "⚠️ 예산 초과! 과소비 중이에요😥\n{diff:,}원 초과했어요.",
        "within": "👍 예산 내에서 잘 쓰고 있어요! ({diff:,}원 남았어요.)",
        "report_title": "[지출 리포트]",
        "no_expenses": "지출 내역이 없습니다.",
        "total_exp": "총 지출: {total}원",
        "by_category": "카테고리별 합계:",
        "invalid_input": "입력 형식이 잘못됐어요! 예시처럼 '식사 8000' 입력하세요.",
        "invalid_menu": "잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.",
        "menu": "\n===== {title} =====",
        "cancel_expense": "◀ 지출 입력 취소, 메뉴로 돌아갑니다.\n",
        "cancel_while_entering": "◀ 지출 입력 중단, 메뉴로 돌아갑니다.\n",
        "wrong_date": "❌ 날짜 형식이 잘못됐어요!YYYY-MM-DD 형식으로 다시 입력해주세요.",
        "set_budget_title": "주간 예산 설정",
        "budget_prompt": "주간 예산을 입력하세요(원). (이전 메뉴로 가려면 q 입력): ",
        "budget_success": "✅ 주간 예산이 {budget:,}원으로 설정되었습니다.\n",
        "invalid_number": "❌ 숫자로 입력해주세요.",
        "cancel_budget": "◀ 예산 설정 취소, 메뉴로 돌아갑니다.\n",
        "cancel_show": "◀ 지출 보기 취소, 메뉴로 돌아갑니다.\n",
        "invalid_confirm": "❌ 잘못된 입력입니다. Enter 또는 q만 입력하세요.",
        "no_week_data": "📢 이번 주 지출이 없습니다!",
        "no_expense_data": "지출 내역이 없습니다.",
        "weekly_chart_title": "[주간 지출 추이 그래프 📈]",
        "not_enough_data": "주간 지출 데이터가 부족합니다.",
        "weekly_chart": "주간 지출 추이",
        "weekly_label": "주차 시작일",
        "weekly_amount": "지출 금액",
    },
    "en": {
        "menu_title": "Expense Manager Menu",
        "input_date": "Enter the expense date (YYYY-MM-DD, press Enter for today, 'q' to quit): ",
        "multi_input_hint": "Enter multiple items (e.g., food 8000)\nPress Enter to finish / 'q' to go back",
        "category_amount": "Category and amount: ",
        "saved": "{} {} saved.",
        "complete": "✅ Expenses for {date} recorded!\n",
        "weekly_view": "This Week's Expenses",
        "confirm_prompt": "Press Enter to confirm or 'q' to go back: ",
        "total": "Total: {total}",
        "budget": "Budget: {budget}",
        "over": "⚠️ Over budget! You overspent by {diff:,}.",
        "within": "👍 You're within budget! ({diff:,} left.)",
        "report_title": "[Expense Report]",
        "no_expenses": "No expenses recorded.",
        "total_exp": "Total Expense: {total}",
        "by_category": "Total by Category:",
        "invalid_input": "Invalid format! Use format like 'food 8000'.",
        "invalid_menu": "Invalid input. Please enter a number between 1 and 4.",
        "menu": "\n===== {title} =====",
        "cancel_expense": "◀ Expense entry cancelled. Returning to menu.\n",
        "cancel_while_entering": "◀ Input stopped. Returning to menu.\n",
        "wrong_date": "❌ Invalid date format! Please useYYYY-MM-DD.",
        "set_budget_title": "Set Weekly Budget",
        "budget_prompt": "Enter your weekly budget (in won). ('q' to cancel): ",
        "budget_success": "✅ Weekly budget set to {budget:,}.\n",
        "invalid_number": "❌ Please enter a valid number.",
        "cancel_budget": "◀ Budget setup cancelled. Returning to menu.\n",
        "cancel_show": "◀ Expense view cancelled. Returning to menu.\n",
        "invalid_confirm": "❌ Invalid input. Only Enter or 'q' allowed.",
        "no_week_data": "📢 No expenses for this week!",
        "no_expense_data": "No expense data available.",
        "weekly_chart_title": "[Weekly Spending Trend 📈]",
        "not_enough_data": "Not enough data to show trend.",
        "weekly_chart": "Weekly Expense Trend",
        "weekly_label": "Week Start",
        "weekly_amount": "Amount Spent",
    }
}

expenses = []
weekly_budget = None

def reset_expenses_data():
    global expenses, weekly_budget
    expenses.clear()
    weekly_budget = None

def input_day_expenses(current_lang):
    global expenses
    lang = LANG[current_lang]
    while True:
        date_str = input(lang["input_date"])
        if date_str.strip().lower() == 'q':
            print(lang["cancel_expense"])
            return
        if date_str.strip() == '':
            date = datetime.date.today()
            break
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print(lang["wrong_date"])

    print(lang["multi_input_hint"])
    while True:
        line = input(lang["category_amount"])
        if line.strip().lower() == 'q':
            print(lang["cancel_while_entering"])
            return
        if line.strip() == '':
            break
        try:
            category, amount = line.split()
            amount = int(amount)
            expenses.append({'amount': amount, 'category': category, 'date': date})
            print(lang["saved"].format(category, amount))
        except ValueError:
            print(lang["invalid_input"])

    print(lang["complete"].format(date=date))

def set_budget(current_lang):
    global weekly_budget
    lang = LANG[current_lang]
    print(lang["set_budget_title"])
    while True:
        budget_input = input(lang["budget_prompt"])
        if budget_input.strip().lower() == 'q':
            print(lang["cancel_budget"])
            return
        try:
            weekly_budget = int(budget_input)
            print(lang["budget_success"].format(budget=weekly_budget))
            break
        except ValueError:
            print(lang["invalid_number"])

def show_weekly_expenses(current_lang):
    lang = LANG[current_lang]
    print(lang["weekly_view"])
    while True:
        confirm = input(lang["confirm_prompt"])
        if confirm.strip().lower() == 'q':
            print(lang["cancel_show"])
            return
        elif confirm.strip() != '':
            print(lang["invalid_confirm"])
            continue
        break

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    this_week_exp = [e for e in expenses if start_of_week <= e['date'] <= today]
    total = sum(e['amount'] for e in this_week_exp)

    if not this_week_exp:
        print(lang["no_week_data"])
        return

    for e in this_week_exp:
        print(f"{e['date']} | {e['category']} | {e['amount']}원")
    print(lang["total"].format(total=total))
    if weekly_budget:
        print(lang["budget"].format(budget=weekly_budget))
        remain = weekly_budget - total
        if total > weekly_budget:
            print(lang["over"].format(diff=abs(remain)))
        else:
            print(lang["within"].format(diff=remain))

def get_weekly_expense(expenses):
    weekly_sum = defaultdict(int)
    for e in expenses:
        if isinstance(e['date'], str):
            e['date'] = datetime.datetime.strptime(e['date'], "%Y-%m-%d").date()
        week_start = e['date'] - datetime.timedelta(days=e['date'].weekday())
        weekly_sum[week_start] += e['amount']
    sorted_weeks = sorted(weekly_sum.items())
    if not sorted_weeks:
        return [], []
    weeks, amounts = zip(*sorted_weeks)
    return weeks, amounts

def draw_weekly_total_trend(current_lang):
    lang = LANG[current_lang]
    print("\n" + lang["weekly_chart_title"])

    if not expenses:
        print(lang["no_expense_data"])
        return

    weeks, amounts = get_weekly_expense(expenses)
    if not weeks:
        print(lang["not_enough_data"])
        return

    x_labels = [f"{w.month}/{w.day}" for w in weeks]
    y_values = list(amounts)

    # 폰트 설정
    system = platform.system()
    if system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

    # 글씨 크기 설정 (user_settings.user_info에서 가져옴)
    plt.rcParams['font.size'] = user_settings.user_info.get("font_size", 12)


    fig, ax = plt.subplots()
    ax.plot(x_labels, y_values, marker='o', linewidth=2, label=lang["weekly_chart"])

    ax.set_title(lang["weekly_chart"])
    ax.set_xlabel(lang["weekly_label"])
    ax.set_ylabel(lang["weekly_amount"])
    ax.tick_params(axis='x', rotation=30)
    ax.grid(True)

    for x, y in zip(x_labels, y_values):
        ax.text(x, y + 3, f"{y:,}원", ha='center', va='bottom', fontsize=plt.rcParams['font.size'] * 0.8) # 텍스트 크기도 조절

    if weekly_budget:
        ax.axhline(weekly_budget, color='red', linestyle='--', linewidth=1.5, label=f"{lang['budget'].split(':')[0]} ({weekly_budget:,}원)")

    ax.legend()
    fig.tight_layout()
    plt.show()

def menu(current_lang):
    lang = LANG[current_lang]
    while True:
        print(lang["menu"].format(title=lang["menu_title"]))
        print("1. " + ("지출 입력" if current_lang == "ko" else "Add Expenses"))
        print("2. " + ("이번 주 지출 보기" if current_lang == "ko" else "Show This Week"))
        print("3. " + ("예산 설정" if current_lang == "ko" else "Set Budget"))
        print("4. " + ("주간 지출 그래프 보기" if current_lang == "ko" else "Show Weekly Chart"))
        print("5. " + ("이전 메뉴로" if current_lang == "ko" else "Back to Main Menu"))

        sel = input("번호 선택: " if current_lang == "ko" else "Select number: ")
        if sel == '1':
            input_day_expenses(current_lang)
        elif sel == '2':
            show_weekly_expenses(current_lang)
        elif sel == '3':
            set_budget(current_lang)
        elif sel == '4':
            draw_weekly_total_trend(current_lang)
        elif sel == '5':
            return
        else:
            print(lang["invalid_menu"])

if __name__ == "__main__":
    # expenses.py를 직접 실행할 때 폰트 설정 (없으면 한글 깨짐)
    system = platform.system()
    if system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    
    menu("ko")