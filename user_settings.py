import json
import expenses
import goals
import manage_schedule
import matplotlib.pyplot as plt

user_info = {
    "name": "",
    "age": None,
    "job": "",
    "font_size": 12, # 기본 폰트 크기
    "language": "ko"
}

def save_user_info():
    """사용자 정보를 파일에 저장하는 함수"""
    try:
        with open("user_info.json", "w", encoding="utf-8") as file:
            json.dump(user_info, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"저장 중 오류 발생: {e}")

def load_user_info():
    """저장된 사용자 정보를 파일에서 불러오는 함수"""
    global user_info
    try:
        with open("user_info.json", "r", encoding="utf-8") as file:
            user_info = json.load(file)
    except FileNotFoundError:
        print("저장된 사용자 정보가 없습니다.")
    except json.JSONDecodeError:
        print("사용자 정보 파일이 손상되었습니다.")

def register_user():
    """사용자 정보를 등록하는 함수"""
    print("\n[사용자 정보 등록]" if user_info['language'] == "ko" else "\n[Register User Info]")
    user_info["name"] = input("이름을 입력하세요: " if user_info['language'] == "ko" else "Enter name: ")
    while True:
        try:
            age_input = input("나이를 입력하세요: " if user_info['language'] == "ko" else "Enter age: ")
            user_info["age"] = int(age_input)
            break
        except ValueError:
            print("숫자로 입력해주세요." if user_info['language'] == "ko" else "Please enter a number.")
    user_info["job"] = input("직업군을 입력하세요: " if user_info['language'] == "ko" else "Enter job: ")
    save_user_info()
    print("사용자 정보가 등록되었습니다." if user_info['language'] == "ko" else "User information registered.")


def update_user():
    """사용자 정보를 수정하는 함수"""
    print("\n[사용자 정보 수정]" if user_info['language'] == "ko" else "\n[Update User Info]")
    print(f"현재 이름: {user_info['name']}, 나이: {user_info['age']}, 직업군: {user_info['job']}" if user_info['language'] == "ko" else \
          f"Current Name: {user_info['name']}, Age: {user_info['age']}, Job: {user_info['job']}")

    name = input("수정할 이름 (엔터 시 유지): " if user_info['language'] == "ko" else "New name (press Enter to keep current): ").strip()
    age = input("수정할 나이 (엔터 시 유지): " if user_info['language'] == "ko" else "New age (press Enter to keep current): ").strip()
    job = input("수정할 직업군 (엔터 시 유지): " if user_info['language'] == "ko" else "New job (press Enter to keep current): ").strip()

    if name:
        user_info["name"] = name
    if age:
        try:
            user_info["age"] = int(age)
        except ValueError:
            print("잘못된 나이 입력입니다. 나이 수정하지 않음." if user_info['language'] == "ko" else "Invalid age input. Age not updated.")
    if job:
        user_info["job"] = job

    save_user_info()
    print("사용자 정보가 수정되었습니다." if user_info['language'] == "ko" else "User information updated.")

def set_font_size():
    """글씨 크기를 설정하는 함수"""
    print("\n[글씨 크기 설정]" if user_info['language'] == "ko" else "\n[Set Font Size]")
    try:
        current_font_size = user_info.get("font_size", 12)
        font_size_input = input(f"새 글씨 크기를 입력하세요 (현재: {current_font_size}, 예: 10, 14, 18): " if user_info['language'] == "ko" else \
                                f"Enter new font size (current: {current_font_size}, e.g., 10, 14, 18): ")
        new_font_size = int(font_size_input)
        
        if new_font_size > 0:
            user_info["font_size"] = new_font_size
            save_user_info()
            # matplotlib의 기본 폰트 크기 설정
            plt.rcParams['font.size'] = new_font_size
            print(f"글씨 크기가 {new_font_size}으로 설정되었습니다." if user_info['language'] == "ko" else \
                  f"Font size set to {new_font_size}.")
        else:
            print("글씨 크기는 양수로 입력해야 합니다." if user_info['language'] == "ko" else "Font size must be a positive number.")
    except ValueError:
        print("잘못된 입력입니다. 숫자를 입력해주세요. 글씨 크기 수정하지 않음." if user_info['language'] == "ko" else \
              "Invalid input. Please enter a number. Font size not updated.")


def set_language(current_lang):
    """언어 설정 함수 - 현재 언어 상태 받고 변경 후 반환"""
    print("\n[언어 설정]" if current_lang == "ko" else "\n[Set Language]")
    print("언어를 선택하세요 (ko: 한국어, en: 영어)" if current_lang == "ko" else "Select language (ko: Korean, en: English)")
    lang_input = input("선택: " if current_lang == "ko" else "Select: ").strip().lower()
    if lang_input in ("ko", "한국어", "korean", "kor"):
        user_info["language"] = "ko"
        save_user_info()
        print("언어가 한국어로 설정되었습니다.")
        return "ko"
    elif lang_input in ("en", "영어", "english", "eng"):
        user_info["language"] = "en"
        save_user_info()
        print("Language set to English.")
        return "en"
    else:
        print("지원하지 않는 언어입니다. 변경하지 않습니다." if current_lang == "ko" else "Unsupported language. Not changed.")
        return current_lang

def reset_data():
    """사용자 정보와 모든 데이터 (지출, 목표, 일정)를 초기화하는 함수"""
    global user_info
    
    # 현재 언어 설정을 유지한 채로 사용자 정보 초기화
    # (font_size도 현재 설정된 것을 유지)
    current_language_setting = user_info.get("language", "ko")
    current_font_size_setting = user_info.get("font_size", 12)

    user_info = {
        "name": "",
        "age": None,
        "job": "",
        "font_size": current_font_size_setting, # 초기화 시 폰트 크기는 유지
        "language": current_language_setting # 초기화 시 언어도 유지
    }
    
    # 각 모듈의 데이터 초기화 함수 호출
    expenses.reset_expenses_data()
    goals.reset_goals_data()
    manage_schedule.schedules.clear()
    
    save_user_info()
    print("모든 데이터가 초기화되었습니다." if user_info['language'] == "ko" else "All data has been reset.")


def user_settings(current_lang, schedules_ref): 
    """사용자 설정 메뉴 - current_lang 입력받아 변경 시 반환"""
    
    while True:
        print("\n=== 사용자 설정 메뉴 ===" if current_lang == "ko" else "\n=== User Settings Menu ===")
        if current_lang == "ko":
            print("1. 이름, 나이, 직업군 등록")
            print("2. 이름, 나이, 직업군 수정")
            print("3. 통계 글씨 크기 설정")
            print("4. 언어 설정")
            print("5. 데이터 초기화")
            print("6. 이전 메뉴로")
            choice = input("선택: ")
        else:
            print("1. Register Name, Age, Job")
            print("2. Update Name, Age, Job")
            print("3. Set Font Size")
            print("4. Set Language")
            print("5. Reset Data")
            print("6. Back to Previous Menu")
            choice = input("Select: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            update_user()
        elif choice == '3':
            set_font_size()
        elif choice == '4':
            current_lang = set_language(current_lang)
        elif choice == '5':
            reset_data() 
            # 데이터 초기화 후 user_info에 저장된 'language' 값을 다시 가져와 current_lang을 업데이트
            current_lang = user_info['language'] 
        elif choice == '6':
            if current_lang == "ko":
                print("\n[이전 메뉴로 돌아가기]")
            else:
                print("\n[Back to previous menu]")
            break
        else:
            if current_lang == "ko":
                print("잘못된 입력입니다. 1~6 사이의 숫자를 입력해주세요.")
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
    return current_lang

# 초기 로드 시 사용자 정보를 불러옴
load_user_info()