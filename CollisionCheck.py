import unreal


def get_current_world():
    # 언리얼 에디터 서브시스템을 통해 에디터 월드 가져오기
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    current_world = editor_subsystem.get_game_world()

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


# 액터의 이름 얻기
def get_actor_name(actor):
    actor_name = actor.get_name()
    # print(f"Actor Name: {actor_name}")

    return actor_name


# 액터의 위치 확인
def get_actor_location(actor):
    actor_location = actor.get_actor_location()
    # print(location)

    return actor_location


# 클래스 정보 가져오기
def get_actor_class(actor):
    actor_class = actor.get_class()
    # print(actor_class)

    return actor_class


# 클래스 이름 가져오기
def get_actor_class_name(actor_class):
    actor_class_name = actor_class.get_name()  # 클래스 이름 가져오기
    # print(f"Actor Class: {class_name}")

    return actor_class_name


# StaticMeshComponent에서 콜리전 프로필 확인
def get_collision_profile_name(component):
    body_instance = component.body_instance
    collision_profile_name = body_instance.get_editor_property('collision_profile_name')

    return collision_profile_name


# 콜리전 프리셋별 처리
def check_collision(collision_profile_name, actor_location):
    # 콜리전 프리셋이 'NoCollision' 일 경우 처리
    if collision_profile_name == "NoCollision":
        print(f"NoCollision found: {actor_location}")


def print_level_info():
    current_world = get_current_world()
    if current_world:
        # 현재 레벨에서 모든 액터 가져오기
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(current_world, unreal.Actor)

        if all_actors:
            for actor in all_actors:
                actor_name = get_actor_name(actor)  # 액터의 이름 얻기
                actor_location = get_actor_location(actor)  # 액터의 위치 확인
                actor_class = get_actor_class(actor)  # 클래스 정보 가져오기
                actor_class_name = get_actor_class_name(actor_class)  # 클래스 이름 가져오기

                # StaticMeshActor 클래스일 경우 처리
                if actor_class == unreal.StaticMeshActor.static_class():
                    components = actor.get_components_by_class(unreal.StaticMeshComponent)
                    for component in components:
                        # StaticMeshComponent에서 콜리전 프로필 확인
                        collision_profile_name = get_collision_profile_name(component)
                    # print(f"Actor {actor_name}, Component {component.get_name()}, Collision Profile: {collision_profile_name}")
                    # 콜리전 프리셋별 처리
                    check_collision(collision_profile_name, actor_location)
        else:
            unreal.log_warning("No actors found in the current world.")
    else:
        unreal.log_error("Failed to get the current world.")


print_level_info()