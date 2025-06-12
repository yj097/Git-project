from expenses import menu as expense_menu
from goals import goal_menu
from manage_schedule import manage_schedule, schedules as all_schedules
from user_settings import user_settings, user_info
import json

LANGUAGES = {
    "ko": {
        "menu_title": "하루 도우미 메인 메뉴",
        "option_1": "지출 관리",
        "option_2": "목표 확인",
        "option_3": "일정/알림 관리",
        "option_4": "사용자 설정",
        "option_5": "종료",
        "select_prompt": "선택:",
        "exit_message": "프로그램을 종료합니다. 좋은 하루 되세요!",
        "invalid_input": "잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요."
    },
    "en": {
        "menu_title": "Daily Helper Main Menu",
        "option_1": "Manage Expenses",
        "option_2": "Check Goals",
        "option_3": "Manage Schedule/Reminders",
        "option_4": "User Settings",
        "option_5": "Exit",
        "select_prompt": "Select:",
        "exit_message": "Exiting program. Have a great day!",
        "invalid_input": "Invalid input. Please enter a number between 1 and 5."
    }
}

current_lang = "ko"

def main():
    global current_lang
    current_lang = user_info.get("language", "ko")

    while True:
        lang = LANGUAGES[current_lang]

        print(f"\n=== {lang['menu_title']} ===")
        print(f"1. {lang['option_1']}")
        print(f"2. {lang['option_2']}")
        print(f"3. {lang['option_3']}")
        print(f"4. {lang['option_4']}")
        print(f"5. {lang['option_5']}")

        choice = input(lang['select_prompt'] + " ")

        if choice == '1':
            expense_menu(current_lang)
        elif choice == '2':
            goal_menu(current_lang)
        elif choice == '3':
            manage_schedule(current_lang)
        elif choice == '4':
            current_lang = user_settings(current_lang, all_schedules)
        elif choice == '5':
            print(f"\n{lang['exit_message']}")
            break
        else:
            print(lang['invalid_input'])

if __name__ == "__main__":
    main()
