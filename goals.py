# 목표 확인 메뉴
import datetime

goals = []

def goal_menu(): # 메뉴 설정
    while True:
        print("\n===== 목표 확인 메뉴 =====")
        print("1. 목표 입력")
        print("2. 달성 체크")
        print("3. 달성률 분석")
        print("4. 이전 메뉴로")
        sel = input("번호 선택: ")
        if sel == '4':
            print("이전 메뉴로 돌아갑니다.")
            continue  # 루프 계속, 메뉴판 다시 뜨게 하기
        elif sel == '1':
            input_goal()
        elif sel == '2':
            check_goal()
        elif sel == '3':
            analyze_goal()
        else:
            print("잘못된 입력입니다.")

def input_goal(): # 목표 입력
    print("\n[목표 입력]")
    goal = input("목표 내용: ")
    due_str = input("마감일 (YYYY-MM-DD): ")
    try:
        due = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ 날짜 형식이 잘못됐습니다! YYYY-MM-DD 형식으로 다시 입력해주세요.")
        return
    goals.append({'goal': goal, 'due': due, 'done': False})
    print("목표가 등록되었습니다.")

def check_goal(): # 달성 체크
    print("\n[달성 체크]")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    for i, g in enumerate(goals, 1):
        status = 'O' if g['done'] else 'X'
        print(f"{i}. {g['goal']} (마감: {g['due']}) / 달성: {status}")
    sel = input("달성한 목표 번호(Enter: 취소): ")
    if sel.strip() == '':
        return
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(goals):
            goals[idx]['done'] = True
            print("달성 체크 완료!")
        else:
            print("❌ 해당 번호의 목표가 없습니다.")
    except ValueError:
        print("❌ 숫자를 정확히 입력해주세요.")

def analyze_goal(): # 달성률 분석
    print("\n[달성률 분석]")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    done_cnt = sum(1 for g in goals if g['done'])
    print(f"전체 목표: {len(goals)}, 달성: {done_cnt}")
    print(f"달성률: {done_cnt / len(goals) * 100:.1f}%")

if __name__ == "__main__":
    goal_menu()

#--------------------------------------------------------
#--------------------------------------------------------
# 목표 달성 리포트
def report_goals():
    print("\n[목표 달성 리포트]")
    if not goals:
        print("등록된 목표가 없습니다.")
        return
    for g in goals:
        status = '달성' if g['done'] else '미달성'
        print(f"- {g['goal']} (마감: {g['due']}) : {status}")
    done = sum(1 for g in goals if g['done'])
    print(f"달성률: {done}/{len(goals)} ({done / len(goals) * 100:.1f}%)")
