def get_client_repository():
    from Client.Application.client_repository import ClientRepository

    MUSIC_DATA_PATH = "../Application/Data/"

    return ClientRepository(data_path=MUSIC_DATA_PATH)


def get_client_cache_repository():
    from Client.Application.client_repository import ClientRepository

    MUSIC_CACHE_PATH = "../Application/Cache/"

    return ClientRepository(data_path=MUSIC_CACHE_PATH)
