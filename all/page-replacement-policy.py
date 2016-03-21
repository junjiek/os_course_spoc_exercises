class WorkingSet:
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = []
        self.time = 0

    def access(self, index):
        for i in range(len(self.history)):
            if self.history[i][0] == index:
                del self.history[i]
                break

        self.history.append([index, self.time])
        while self.time - self.history[0][1] >= self.window_size:
            del self.history[0]

        print("Access " + str(index) + ":"),
        for item in self.history:
            print(item[0]),
        print("")
        self.time += 1


class PageFaultFrequency:
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = []
        self.last_fault = 0
        self.current = -1
        self.mem = []

    def access(self, index):
        self.history.append(index)
        self.current += 1
        if len(self.history) > self.window_size + 1:
            del self.history[0]

        if index not in self.mem:
            delta = self.current - self.last_fault
            self.last_fault = self.current

            if delta <= self.window_size:
                self.mem.append(index)
            else:
                new_mem = []
                for item in self.mem:
                    if item in self.history:
                        new_mem.append(item)
                self.mem = new_mem
                self.mem.append(index)

        print("Access " + str(index) + ":"),
        for item in self.mem:
            print(item),
        print("")


if __name__ == '__main__':
    print("------- Woring Set -------")
    working_set = WorkingSet(3)
    visit_seq = ['a', 'd', 'e', 'c', 'c', 'd', 'b', 'c', 'e', 'c', 'e', 'a', 'd']
    for index in visit_seq:
        working_set.access(index)
    print("------- Page Fault Frequency -------")
    pff = PageFaultFrequency(2)
    for index in visit_seq:
        pff.access(index)
