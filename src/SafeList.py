from threading import Lock


class SafeList():
    def __init__(self):
        self.data = []
        self.lock = Lock()

    def put(self, item):
        self.lock.acquire()
        self.data.append(item)
        self.lock.release()

    def get_all(self) -> list:
        self.lock.acquire()
        data_copy = self.data.copy()
        self.data.clear()
        self.lock.release()
        return data_copy

    def size(self) -> int:
        return len(self.data)
