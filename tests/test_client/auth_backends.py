from hibee.contrib.auth.backends import ModelBackend


class TestClientBackend(ModelBackend):
    pass


class BackendWithoutGetUserMethod:
    pass
