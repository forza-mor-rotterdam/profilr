import importlib


def get_service_class(service_class_str: str):
    lib = importlib.import_module(service_class_str.rsplit(".", 1)[0])
    return getattr(lib, service_class_str.rsplit(".", 1)[1])
