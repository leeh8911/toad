class BaseRegistry(type):
    """
    BaseRegistry 클래스는 클래스를 등록하고, 이름을 통해 해당 클래스를 인스턴스화할 수 있는 기능을 제공합니다.

    기본적인 사용 예제:
    >>> class TempRegistry(metaclass=BaseRegistry):
    ...     pass

    >>> @TempRegistry.register
    ... class MyClass:
    ...     def __init__(self, *args, **kwargs):
    ...         self.value = kwargs.get("value", 0)
    ...     def run(self):
    ...         return self.value

    >>> instance = TempRegistry.build({"name": "MyClass", "value": 42})
    >>> isinstance(instance, MyClass)
    True
    >>> instance.run()
    42
    """

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        # 각 클래스의 고유한 REGISTRY 생성
        if not hasattr(new_cls, "REGISTRY"):
            new_cls.REGISTRY = {}

        # register 메서드를 각 클래스에 바인딩
        def register(cls, tgt):
            cls.REGISTRY[tgt.__name__] = tgt
            return tgt

        def build(cls, cfg):
            name = cfg.get("name")
            assert name in cls.REGISTRY
            return cls.REGISTRY[name](**cfg)

        new_cls.register = classmethod(register)
        new_cls.build = classmethod(build)

        return new_cls


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
