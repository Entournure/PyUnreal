import unreal


def is_actor_floating(actor, distance_threshold=10.0):
    # 현재 월드를 가져오기
    current_world = get_current_world()

    # 액터의 위치와 크기를 가져오기
    actor_location = actor.get_actor_location()
    actor_bounds = actor.get_actor_bounds(False)
    origin, box_extent = actor_bounds[0], actor_bounds[1]

    # 액터의 바닥 위치 계산 (액터의 중심에서 하단까지의 거리만큼 뺌)
    start = unreal.Vector(actor_location.x, actor_location.y, actor_location.z)
    end = unreal.Vector(actor_location.x, actor_location.y, actor_location.z - box_extent.z - distance_threshold)

    # 충돌 체크 수행
    hit_result = unreal.SystemLibrary.line_trace_single(
        current_world,
        start,
        end,
        unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
        False,  # 간단한 충돌 체크 사용 여부
        [],  # 무시할 액터 목록
        unreal.DrawDebugTrace.FOR_DURATION,  # 디버깅 설정
        True,  # 자기 자신 무시 여부
        unreal.LinearColor.GREEN,
        unreal.LinearColor.RED,
        5.0
    )

    # 충돌 결과 확인
    if hit_result:
        return False  # 충돌이 있으면 액터는 지면에 닿아 있음
    return True  # 충돌이 없으면 액터는 공중에 떠 있음

# 액터의 이름 얻기
def get_actor_name(actor):
    actor_name = actor.get_name()
    return actor_name

# 액터의 위치 확인
def get_actor_location(actor):
    actor_location = actor.get_actor_location()
    return actor_location

# 클래스 정보 가져오기
def get_actor_class(actor):
    actor_class = actor.get_class()
    return actor_class

# 클래스 이름 가져오기
def get_actor_class_name(actor_class):
    actor_class_name = actor_class.get_name()
    return actor_class_name

def get_current_world():
    # 언리얼 에디터 서브시스템을 통해 에디터 월드 가져오기
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    current_world = editor_subsystem.get_game_world()

    if current_world:
        return current_world

    current_world = editor_subsystem.get_editor_world()
    if current_world:
        return current_world

    try:
        # 게임 플레이 모드에서 현재 월드 가져오기
        game_instance = unreal.GameplayStatics.get_game_instance(unreal.EditorLevelLibrary.get_editor_world())
        if game_instance:
            return game_instance.get_world()
    except Exception as e:
        unreal.log_error(f"Failed to get the game world: {e}")

    return None

def read_csv_file(file_path):
    data_csv = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        headers_csv = next(csv_reader)  # 첫 번째 행은 헤더로 읽기
        for row in csv_reader:
            data_csv.append(row)
    return headers_csv, data_csv

def check_actor():
    current_world = get_current_world()
    if current_world:
        # 로드된 모든 액터 목록 가져오기
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(current_world, unreal.Actor)

        if all_actors:
            for actor in all_actors:
                actor_name = get_actor_name(actor)
                actor_location = get_actor_location(actor)
                actor_class = get_actor_class(actor)
                actor_class_name = get_actor_class_name(actor_class)
                # 특정 클래스의 액터들이 공중에 떠있는지 확인
                if actor_class_name == "":
                    if is_actor_floating(actor):
                        print(f"{actor_name}, {actor_location}")

check_actor()
