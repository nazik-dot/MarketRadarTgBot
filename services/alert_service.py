ALERTS = {}


def add_alert(user_id: int, asset_id: str, target_price: float, direction: str):
    """
    direction: 'up' або 'down'
    """
    if user_id not in ALERTS:
        ALERTS[user_id] = []

    ALERTS[user_id].append({
        "asset_id": asset_id,
        "target_price": target_price,
        "direction": direction
    })


def get_user_alerts(user_id: int):
    return ALERTS.get(user_id, [])


def delete_alert(user_id: int, alert_index: int) -> bool:
    """
    Видаляє алерт за індексом.
    Повертає True, якщо успішно видалено, False - якщо не знайдено.
    """
    if user_id not in ALERTS:
        return False
    
    alerts = ALERTS[user_id]
    if 0 <= alert_index < len(alerts):
        deleted = alerts.pop(alert_index)
        return True
    return False


def clear_user_alerts(user_id: int):
    """Видаляє всі алерти користувача"""
    if user_id in ALERTS:
        ALERTS[user_id] = []


def check_alerts(price_map: dict):
    """
    price_map = {
        "btc": 67000,
        "eth": 3200
    }
    """
    triggered = []

    for user_id, alerts in ALERTS.items():
        for alert in alerts:
            asset_id = alert["asset_id"]
            target = alert["target_price"]
            direction = alert["direction"]

            current_price = price_map.get(asset_id)
            if current_price is None:
                continue

            if direction == "up" and current_price >= target:
                triggered.append((user_id, alert, current_price))

            elif direction == "down" and current_price <= target:
                triggered.append((user_id, alert, current_price))

    return triggered