# 목표 확인 메뉴
import datetime

goals = []

def goal_menu():  # 메뉴 설정
    while True:
        print("\n===== 목표 확인 메뉴 =====")
        print("1. 목표 입력")
        print("2. 달성 체크")
        print("3. 달성률 분석")

        sel = input("번호 선택: ")
        if sel == '1':
            input_goal()
        elif sel == '2':
            check_goal()
        elif sel == '3':
            analyze_goal()
        else:
            print("잘못된 입력입니다. 1~3 중에서 선택해주세요.")

def input_goal():  # 목표 여러 개 입력
    print("\n[목표 입력] (q 입력 시 이전 메뉴로, Enter만 입력 시 종료)\n")

    while True:
        goal = input("목표 내용: ")
        if goal.strip().lower() == 'q':
            print("◀ 목표 입력 취소\n")
            return
        if goal.strip() == '':
            print("✅ 목표 입력 완료\n")
            return
        
        due_str = input("마감일 (YYYY-MM-DD): ")
        if due_str.strip().lower() == 'q':
            print("◀ 목표 입력 취소\n")
            return
        try:
            due = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ 날짜 형식이 잘못됐습니다! YYYY-MM-DD 형식으로 다시 입력해주세요.\n")
            continue

        goals.append({'goal': goal, 'due': due, 'done': False})
        print(f"✅ 목표 '{goal}' 등록 완료\n")

def check_goal():  # 달성 체크
    print("\n[달성 체크] (이전 메뉴로 가려면 q 입력)")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    for i, g in enumerate(goals, 1):
        status = '✅ 달성됨' if g['done'] else '❌ 아직 미달성'
        print(f"{i}. {g['goal']} (마감: {g['due']}) / 상태: {status}")
    sel = input("달성한 목표 번호(Enter: 취소): ")
    if sel.strip().lower() == 'q':
        print("◀ 체크 취소\n")
        return
    if sel.strip() == '':
        return
    try:
        indices = [int(s.strip()) - 1 for s in sel.split(',')]
        for idx in indices:
            if 0 <= idx < len(goals):
                goals[idx]['done'] = True
        print("✅ 선택한 목표들에 대해 달성 체크 완료!")
    except ValueError:
        print("❌ 숫자 형식이 잘못됐습니다.")

def analyze_goal():  # 달성률 분석
    print("\n[달성률 분석]")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    done_cnt = sum(1 for g in goals if g['done'])
    print(f"전체 목표: {len(goals)}, 달성: {done_cnt}")
    print(f"달성률: {done_cnt / len(goals) * 100:.1f}%")
    input("Enter를 누르면 메뉴로 돌아갑니다: ")

if __name__ == "__main__":
    goal_menu()

# --------------------------------------------------------
# 4번에서의 목표 달성 리포트
def report_goals():
    print("\n[목표 달성 리포트]")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    for g in goals:
        status = '✅ 달성됨' if g['done'] else '❌ 아직 미달성'
        print(f"- {g['goal']} (마감: {g['due']}) : {status}")
    done = sum(1 for g in goals if g['done'])
    print(f"달성률: {done}/{len(goals)} ({done / len(goals) * 100:.1f}%)")
