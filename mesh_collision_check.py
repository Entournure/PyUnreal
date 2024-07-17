import unreal
import re


# 네비게이션 시스템에서 특정 위치로의 이동 가능 여부를 확인하는 함수
def can_move_to_location(start_location, target_location):
    current_world = get_current_world()
    nav_system = unreal.NavigationSystemV1.get_navigation_system(current_world)

    if nav_system:
        # 네비게이션 경로를 계산
        nav_path = nav_system.find_path_to_location_synchronously(current_world, start_location, target_location)

        if nav_path and nav_path.is_valid():
            # 실제로 경로가 유효한지 확인
            path_length = nav_path.get_path_length()
            if path_length > 0:
                return True
                '''
                path_points = nav_path.get_editor_property('path_points')
                start_ray = path_points[-1] + unreal.Vector(0, 0, 20)
                res = nav_system.navigation_raycast(current_world, start_ray, target_location)
                if res:
                    return False
                else:
                    return True
                '''
    return False

# 액터 위치 표기 형식 변경
def change_actor_location(actor_location):
    # 정규식을 사용하여 숫자값 추출
    numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", str(actor_location))
    x = float(numbers[-3])
    y = float(numbers[-2])
    z = float(numbers[-1])

    # 결과 문자열 생성
    result = f"(X={x:.5f}, Y={y:.5f}, Z={z:.5f})"
    return result

# 콜리전 프리셋별 처리
def check_collision(collision_profile_name, actor_name, actor_location):
    # 이동 가능 여부 확인
    player_start_location = unreal.Vector(13471.000000,-845371.000000,2946.323833)  # 예시: 플레이어 시작 위치 설정
    changed_actor_location = change_actor_location(actor_location)
    check_list = is_location_in_ignore_list(changed_actor_location)
    if not check_list:
        if collision_profile_name == "NoCollision":
            if can_move_to_location(player_start_location, actor_location):
                print(f"NoCollision found: {actor_name}, {changed_actor_location}")
            #else:
                #unreal.log_warning(f"Cannot move to: {actor_name}, {changed_actor_location}")
        elif collision_profile_name == "Custom":
            if can_move_to_location(player_start_location, actor_location):
                print(f"Custom Collision found: {actor_name}, {changed_actor_location}")
            #else:
                #unreal.log_warning(f"Cannot move to: {actor_name}, {changed_actor_location}")

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

# StaticMeshComponent에서 콜리전 프로필 확인
def get_collision_profile_name(body_instance):
    collision_profile_name = body_instance.get_editor_property('collision_profile_name')
    return collision_profile_name

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

# StaticMesh의 BodyInstance 가져오기
def get_staticmesh_body_instance(component):
    static_mesh = component.static_mesh
    body_setup = static_mesh.get_editor_property('body_setup')
    body_instance = body_setup.get_editor_property('default_instance')
    return body_instance

# StaticMesh의 콜리전 프로필 확인
def get_staticmesh_collision_profile_name(body_instance):
    mesh_collision_profile_name = body_instance.get_editor_property('collision_profile_name')
    return mesh_collision_profile_name

# LOD의 디테일 모드 확인
def get_lod_detail_mode(component):
    detail_mode = component.get_editor_property('detail_mode')
    return detail_mode

# 데이터 레이어가 없는지 확인
def has_no_data_layers(actor):
    if hasattr(actor, 'get_editor_property'):
        data_layers = actor.get_editor_property('DataLayerAssets')
        if not data_layers or len(data_layers) == 0:
            return True
    return False

def is_actor_floating(actor, distance_threshold=100.0):
    current_world = get_current_world()
    actor_location = get_actor_location(actor)
    start = unreal.Vector(actor_location.x, actor_location.y, actor_location.z)
    end = unreal.Vector(actor_location.x, actor_location.y, actor_location.z - distance_threshold)

    hit_result = unreal.SystemLibrary.line_trace_single(
        current_world, start, end, unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
        False, [], unreal.DrawDebugTrace.NONE, False, unreal.LinearColor.RED, unreal.LinearColor.GREEN, 5.0)

    if hit_result:
        return False  # Ground detected within the threshold
    return True  # No ground detected within the threshold

def is_actor_hidden_in_game(actor):
    # Check if the actor is hidden in game
    return actor.get_editor_property('hidden')

def is_location_in_ignore_list(actor_location):
    try:
        with open("D:/IgnoreList.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.find(str(actor_location)) != -1:
                    return True
    except Exception as e:
        unreal.log_error(f"Failed to read ignore list: {e}")
    return False

# 월드파티션 런타임그리드가 MainGrid인지 확인
def is_main_runtime_grid(actor):
    if hasattr(actor, 'get_editor_property'):
        runtime_grid = actor.get_editor_property('RuntimeGrid')
        if runtime_grid == 'MainGrid':
            return True
    return False

def print_level_info():
    # 게임 플레이 모드에서 현재 월드 가져오기
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

                # 액터 클래스가 스태틱매시 액터인지 확인
                if actor_class == unreal.StaticMeshActor.static_class():
                    # RuntimeGrid가 MainGrid이고 데이터 레이어가 없는지 확인
                    if is_main_runtime_grid(actor) and has_no_data_layers(actor) and not is_actor_floating(actor):
                        # 컴포넌트 가져오기
                        components = actor.get_components_by_class(unreal.StaticMeshComponent)
                        component = components[0]
                        # 콜리전 프리셋이 Default인지 체크 / True일 경우 Default 체크 / False일 경우 Default 프리셋 미체크
                        # True일 경우 콜리전 프리셋이 Default일 경우에도 다른 콜리전 프리셋으로 검출될 수 있으므로 False일 경우만 확인
                        check_default_collision = component.get_editor_property('use_default_collision')
                        # 각 컴포넌트의 속성 확인
                        detail_mode = get_lod_detail_mode(component)  # 컴포넌트의 LOD 디테일 모드 확인
                        # Detail Mode가 Low인 경우에만 출력 (DetailMode 값 0 = LOW / 1 = MEDIUM / 2 = HIGH
                        if detail_mode == 0 and not check_default_collision:
                            hidden_in_game = is_actor_hidden_in_game(actor)
                            if not hidden_in_game:
                                body_instance = get_staticmesh_body_instance(component)
                                mesh_collision_profile_name = get_staticmesh_collision_profile_name(body_instance)
                                # StaticMeshActor의 StaticMesh 콜리전 프리셋이 NoCollision이 아닐 경우만 확인
                                if mesh_collision_profile_name != "NoCollision":
                                    body_instance = component.body_instance
                                    collision_profile_name = get_collision_profile_name(body_instance)  # 컴포넌트의 콜리전 프로파일 이름 저장
                                    check_collision(collision_profile_name, actor_name, actor_location)  # 컴포넌트의 콜리전 프리셋 확인

        else:
            unreal.log_warning("No actors found in the current world.")
    else:
        unreal.log_error("Failed to get the current world.")


print_level_info()
