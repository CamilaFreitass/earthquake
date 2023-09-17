from decouple import config


banco = 'terremoto.db'
directory_temp = "temp"


if config('environment', cast=bool, default=False):
    CONN = f"sqlite:///{directory_temp}/{banco}"
else:
    CONN = f"sqlite:///{directory_temp}/{banco}"

