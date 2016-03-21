class PageFaultFrequency:
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = []
        self.last_fault = 0
        self.current = -1
        self.mem = []

    def access(self, addr):
        self.history.append(addr)
        self.current += 1
        if len(self.history) > self.window_size + 1:
            del self.history[0]

        hit = True
        if addr not in self.mem:
            hit = False
            delta = self.current - self.last_fault
            self.last_fault = self.current

            if delta <= self.window_size:
                self.mem.append(addr)
            else:
                new_mem = []
                for i in self.mem:
                    if i in self.history:
                        new_mem.append(i)
                self.mem = new_mem
                self.mem.append(addr)
        self.printInfo(addr, hit)

    def printInfo(self, addr, hit):
        if hit:
            print("access " + str(addr) + " (H) " + ":"),
        else:
            print("access " + str(addr) + " (M) " + ":"),
        for i in self.mem:
            print(i),
        print("")


class WorkingSet:
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = []
        self.time = -1

    def access(self, addr):
        self.time += 1
        hit = False
        for i in range(len(self.history)):
            if self.history[i][0] == addr:
                del self.history[i]
                hit = True
                break
        self.history.append([addr, self.time])
        while self.time - self.history[0][1] >= self.window_size:
            del self.history[0]
        self.printInfo(addr, hit)

    def printInfo(self, addr, hit):
        if hit:
            print("access " + str(addr) + " (H) " + ":"),
        else:
            print("access " + str(addr) + " (M) " + ":"),
        for i in self.history:
            print(i[0]),
        print("")

if __name__ == '__main__':
    visit_seq = ['a', 'd', 'e', 'c', 'c', 'd', 'b', 'c', 'e', 'c', 'e', 'a', 'd']
    print("------- Page Fault Frequency -------")
    pff = PageFaultFrequency(2)
    for index in visit_seq:
        pff.access(index)
    print("------- Woring Set -------")
    ws = WorkingSet(3)
    for addr in visit_seq:
        ws.access(addr)
