from Client.Application.client_api import get_music_by_id
dict_emotion = {'Happy': ['c9862f5d-26a9-43bb-ac76-c6591fa40b12', 'b89a91ba-23b7-4fea-92f0-a2244836a712', '86273f6a-bbe8-47a9-9708-623268367e42', 'c60ada0a-86fd-4fc1-b593-34822ff89958', '285b1f6f-1577-4470-b3aa-5078e96f905d', '0203985d-01ac-4d4a-83fd-8f895e70dbca', '70c4ffef-42b7-4d38-96ad-225eb4ef2e88', '0e9cbbc2-11e1-4484-b39c-26d00e1f9ed7', 'b260a248-4e03-441a-96b9-b52d48de3ac9', 'b54a5b83-5edb-47ad-a3a6-9d49b3de27e0'],
                'Sad': ['1d4f988f-b0ac-4f5b-b191-25033cff7b3e', '8d9bc158-d010-46ac-bc45-a5922a99d2a4', 'a0d2e977-d386-44d4-bb12-b2a8a0cbaec6', '31201ec9-9b0b-44d4-bc10-2c8064fa977a', 'b5f1b2c6-b998-4781-a409-d63753155527', '4b940396-372c-4101-b302-d23921e40f61', 'f62655c5-1491-4dc6-bbfb-169f76958a07', 'cca21d45-3c6f-4cc4-918a-f1ef2d2ee280', 'bb518b47-0452-46a5-a804-2b8fc3d06f8e', '11d35369-05d8-491d-a739-6d8b0b1dfad6'],
                'Calm': ['567a6e68-84c3-46f1-85d0-471016868cb1', '52d452dd-53f8-4f0b-a19c-1f1a7eab39ab', '1a93323b-dd3e-4698-85a4-a579d94d4095', '58dc0049-464b-4493-b26e-68502f44087f', 'c8409c46-f138-4175-8013-f35cda0cfc0b', '88202876-5720-4d23-b71e-0dc258572994', '9f2c07a6-40ca-4e90-aada-a85c64bf486d', '4cc218d1-5fdc-4372-b792-618064b87dad', 'd92901ff-8011-471c-a3d1-371407c236ab', '727852a6-b709-435c-8c0e-2faf86ded91f'],
                'Aggressive': ['dbfc91e2-a461-4ea5-9723-6dd5c1392f86', '08668a22-825d-45d9-bdba-ff540bd3d498', '9e81d27d-8eb0-4afc-9388-a4e4e6319859', 'e1676c13-fbbb-44f3-92ab-f4f5ff7ebefa', 'e76da7ba-a311-4b4f-a8e8-27fa5abd0880', 'cbc8bb47-77a3-4186-8e2a-c4ff00f512a4', 'e75d5aed-d0e0-4b84-8182-c53c0de3c2b3', '6ee44f43-8dec-4397-8288-e63323016cb8', '28b55310-3209-470e-b7a9-7b80dc0a589b', '6c39a356-1603-44ca-9c17-c71fbab29960'],
                'Romantic': ['25b4bf8a-b16a-4d8a-a7d5-72146d6e5a58', '9ff063ea-b1f5-46d1-be1b-e74172af35b2', '89898d5e-ee78-4dad-9668-7ec0773ec994', '8ccd9322-c336-45da-81f1-55268865f5a5', '28ade1ed-c4d7-439c-86fa-276d1be4717f', 'f6de3497-7fe6-40f0-b896-70fc5ebfd705', '4e83dcad-8401-4681-9624-8dc7809670a3', '8e250900-fd4c-4742-ba44-8b64cf0ae911', 'f36fdf24-e28a-4cca-94ee-3c391015d7a4', 'c7e1a82e-9a55-4533-9a00-9149eb910a0a'],
                'Motivating': ['42afadcb-24b3-4355-ae86-20d934591bb0', '97761b2d-c7a0-439f-b932-d35570dd6354', '7da0987d-3f43-4dc2-8d6e-2a7985a6b732', '87e94f5b-b0f1-438c-9370-0c9d91580005', '9367e065-abb8-416a-b03d-64b7e74d6d84', '60e031ff-d98a-4673-94dc-1140b9240a0d', '4f38152d-6e94-4b06-a192-861b3f5a555f', 'fbab0853-a153-4ff5-b0e8-fb7c5e370943', '7b12509d-2b71-4a8f-8360-9ec9fa96c66f', 'ffa3c416-12f4-4730-ba86-1f86e1f23e64']}

stack = list()
saved_style_music = ""


def get_music(user_id: str, style_music: str):
    global stack
    global saved_style_music
    if style_music not in dict_emotion:
        return {"status": False, "path": None, "music_id": None}
    if len(saved_style_music) == 0 or saved_style_music != style_music:
        stack = dict_emotion[style_music].copy()
        saved_style_music = style_music
    if len(stack) == 0:
        stack = dict_emotion[style_music].copy()
    music_id = stack.pop()
    return get_music_by_id(user_id=user_id, music_id=music_id)
