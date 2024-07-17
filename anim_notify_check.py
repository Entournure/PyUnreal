import unreal
import os

def list_files(directory_path):
    all_files = os.listdir(directory_path)
    file_list = [os.path.splitext(f)[0] for f in all_files if os.path.isfile(os.path.join(directory_path, f))]
    return file_list

def print_notify_events(asset_path):
    # 애니메이션 몽타주 로드
    montage = unreal.load_object(None, asset_path)

    # 유효성 검사: 몽타주가 로드되었는지 확인
    if not montage or not isinstance(montage, unreal.AnimMontage):
        unreal.log_error(f"Failed to load AnimMontage at {asset_path}.")
    else:
        # 노티파이 이름 목록을 리스트에 저장
        list_notify = unreal.AnimationLibrary.get_animation_notify_event_names(montage)
        # 저장된 노티파이 이름 목록 출력
        # print(list_notify) 
        if "" in list_notify:
            notify = list_notify[list_notify.index("")]
            print(notify)
        else:
            print(unreal.log_error(f"Failed to load AnimNotify at {montage}"))

# 에셋 경로 지정 
asset_path = ""
# 파일 경로 지정
directory_path = ""
file_list = list_files(directory_path)
for file in file_list:
    asset = asset_path + file
    print_notify_events(asset)