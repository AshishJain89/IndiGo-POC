# Simple dependency injection container for backend
class Container:
    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        self._services[interface] = implementation

    def resolve(self, interface, *args, **kwargs):
        impl = self._services.get(interface)
        if impl is None:
            raise ValueError(f"Service {interface} not registered")
        return impl(*args, **kwargs)

container = Container()
