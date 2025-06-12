# 목표 확인 메뉴
import datetime

goals = []

# ✅ 추가된 함수: 목표 데이터 초기화
def reset_goals_data():
    global goals
    goals.clear()
    # 이 함수는 user_settings.py에서 호출되므로, 해당 파일의 언어 설정을 따르지 않고 독립적으로 출력.
    # user_settings.py에서 reset_data() 호출 시 최종 메시지를 통일성 있게 출력할 수 있음.
    # print("목표 데이터가 초기화되었습니다." if LANGUAGES["ko"] else "Goal data has been reset.")


LANGUAGES = {
    "ko": {
        "menu_title": "목표 확인 메뉴",
        "option_1": "목표 입력",
        "option_2": "달성 체크",
        "option_3": "달성률 분석",
        "select_prompt": "번호 선택: ",
        "invalid_input": "잘못된 입력입니다. 1~3 중에서 선택해주세요.",
        "input_goal_title": "[목표 입력] (q 입력 시 이전 메뉴로, Enter만 입력 시 종료)\n",
        "cancel_msg": "◀ 목표 입력 취소\n",
        "goal_done": "✅ 목표 입력 완료\n",
        "date_format_error": "❌ 날짜 형식이 잘못됐습니다!YYYY-MM-DD 형식으로 다시 입력해주세요.\n",
        "goal_registered": "✅ 목표 '{}' 등록 완료\n",
        "check_title": "[달성 체크] (이전 메뉴로 가려면 q 입력)",
        "no_goals": "등록된 목표가 없습니다.",
        "check_cancel": "◀ 체크 취소\n",
        "check_complete": "✅ 선택한 목표들에 대해 달성 체크 완료!",
        "analyze_title": "[달성률 분석]",
        "press_enter": "Enter를 누르면 메뉴로 돌아갑니다: ",
    },
    "en": {
        "menu_title": "Check Goals Menu",
        "option_1": "Input Goals",
        "option_2": "Check Achievement",
        "option_3": "Analyze Achievement Rate",
        "select_prompt": "Select number: ",
        "invalid_input": "Invalid input. Please select 1~3.",
        "input_goal_title": "[Input Goals] (Enter 'q' to return to previous menu, Enter only to finish)\n",
        "cancel_msg": "◀ Goal input canceled\n",
        "goal_done": "✅ Goal input completed\n",
        "date_format_error": "❌ Wrong date format! Please enter YYYY-MM-DD.\n",
        "goal_registered": "✅ Goal '{}' registered\n",
        "check_title": "[Check Achievement] (Enter 'q' to return to previous menu)",
        "no_goals": "No registered goals.",
        "check_cancel": "◀ Check canceled\n",
        "check_complete": "✅ Selected goals marked as achieved!",
        "analyze_title": "[Achievement Rate Analysis]",
        "press_enter": "Press Enter to return to menu: ",
    }
}

def goal_menu(lang_code):
    lang = LANGUAGES.get(lang_code, LANGUAGES["ko"])
    while True:
        print(f"\n===== {lang['menu_title']} =====")
        print(f"1. {lang['option_1']}")
        print(f"2. {lang['option_2']}")
        print(f"3. {lang['option_3']}")
        print("4. 이전 메뉴로 가기" if lang_code == "ko" else "4. Return to Previous Menu")

        sel = input(lang['select_prompt'])
        if sel == '1':
            input_goal(lang)
        elif sel == '2':
            check_goal(lang)
        elif sel == '3':
            analyze_goal(lang)
        elif sel == '4':
            print("◀ 이전 메뉴로 돌아갑니다." if lang_code == "ko" else "◀ Returning to previous menu.")
            break  # 반복문 종료 → 메인 메뉴로 복귀
        else:
            print(lang['invalid_input'])

def input_goal(lang):
    print(f"\n{lang['input_goal_title']}")
    while True:
        goal = input("Goal content: " if lang == LANGUAGES["en"] else "목표 내용: ")
        if goal.strip().lower() == 'q':
            print(lang['cancel_msg'])
            return
        if goal.strip() == '':
            print(lang['goal_done'])
            return
        
        due_str = input("Due date (YYYY-MM-DD): " if lang == LANGUAGES["en"] else "마감일 (YYYY-MM-DD): ")
        if due_str.strip().lower() == 'q':
            print(lang['cancel_msg'])
            return
        try:
            due = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
        except ValueError:
            print(lang['date_format_error'])
            continue

        goals.append({'goal': goal, 'due': due, 'done': False})
        print(lang['goal_registered'].format(goal))

def check_goal(lang):
    print(f"\n{lang['check_title']}")
    if not goals:
        print(lang['no_goals'])
        return
    for i, g in enumerate(goals, 1):
        status = '✅ Achieved' if g['done'] else '❌ Not achieved'
        if lang == LANGUAGES["ko"]:
            print(f"{i}. {g['goal']} (마감: {g['due']}) / 상태: {'✅ 달성됨' if g['done'] else '❌ 아직 미달성'}")
        else:
            print(f"{i}. {g['goal']} (Due: {g['due']}) / Status: {status}")

    sel = input("Select achieved goal numbers (Enter to cancel): " if lang == LANGUAGES["en"] else "달성한 목표 번호(Enter: 취소): ")
    if sel.strip().lower() == 'q':
        print(lang['check_cancel'])
        return
    if sel.strip() == '':
        return
    try:
        indices = [int(s.strip()) - 1 for s in sel.split(',')]
        for idx in indices:
            if 0 <= idx < len(goals):
                goals[idx]['done'] = True
        print(lang['check_complete'])
    except ValueError:
        print(lang['invalid_input'])

def analyze_goal(lang):
    print(f"\n{lang['analyze_title']}")
    if not goals:
        print(lang['no_goals'])
        return
    done_cnt = sum(1 for g in goals if g['done'])
    print(f"Total goals: {len(goals)}, Achieved: {done_cnt}" if lang == LANGUAGES["en"] else f"전체 목표: {len(goals)}, 달성: {done_cnt}")
    print(f"Achievement rate: {done_cnt / len(goals) * 100:.1f}%" if lang == LANGUAGES["en"] else f"달성률: {done_cnt / len(goals) * 100:.1f}%")
    input(lang['press_enter'])

if __name__ == "__main__":
    goal_menu("ko")