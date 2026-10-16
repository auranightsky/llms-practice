import copy


DEFAULT_SPEAKER_STATE = {
    "model": "Music Studio 7 (HW-LS7*)",
    "power": True,
    "volume": 20,
    "muted": False,
    "microphone": True,
    "led": "white",
    "wifi": True,
    "bluetooth_connected": False,
    "connected_bluetooth_device": None,
    "pairing_mode": False,
    "night_mode": False,
    "sound_mode": "standard",
    "needs_service": False,
}

speaker_state = copy.deepcopy(DEFAULT_SPEAKER_STATE)