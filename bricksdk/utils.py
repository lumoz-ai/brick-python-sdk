from abc import ABCMeta


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ABCSingleton(ABCMeta, Singleton):
    pass


class Environments:
    DEBUG_ENV = "debug"
    STAGING_ENV = "staging"
    PROD_ENV = "production"
