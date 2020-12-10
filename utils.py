import inspect


def find_subclasses(module, clazz):
    return [
        cls
            for name, cls in inspect.getmembers(module)
                if inspect.isclass(cls) and issubclass(cls, clazz)
    ]
