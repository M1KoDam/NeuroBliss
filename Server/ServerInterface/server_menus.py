class ServerMenu:
    @staticmethod
    def get_main_menu_banner():
        return """\nChoose one of the next options:
----------
1. Generate music
2. Users info
3  Music info
4. Options (Changing options will stop server)
----------
0. Off server"""

    @staticmethod
    def get_music_info_menu_banner():
        return f"""\nUsers info
----------
1. Show music
2. Delete music
3. Delete all music
----------
0. Back"""

    @staticmethod
    def get_user_info_menu_banner():
        return f"""\nUsers info
----------
1. Show users
2. Delete user
3. Delete all users
----------
0. Back"""
