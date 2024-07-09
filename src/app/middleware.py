class MiddlewareChain:
    def __init__(self):
        self.middlewares = []
        self.__user_middlewares = []

    def add_user_middleware(self, middleware):
        self.__user_middlewares.append(middleware)
