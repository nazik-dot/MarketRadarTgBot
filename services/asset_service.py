USER_ASSETS = {}


def get_user_assets(user_id: int):
    return USER_ASSETS.get(user_id, [])


def add_asset(user_id: int, asset: dict):
    if user_id not in USER_ASSETS:
        USER_ASSETS[user_id] = []

    USER_ASSETS[user_id].append(asset)
    return True


def delete_asset(user_id: int, asset_id: str):
    assets = USER_ASSETS.get(user_id, [])

    USER_ASSETS[user_id] = [
        a for a in assets if a.get("id") != asset_id
    ]

    return True