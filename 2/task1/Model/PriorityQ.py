class PriorityQ:
    def __init__(self):
        self.queue = []


    def __str__(self):
        return ' '.join([str(i) for i in self.queue])


    def isEmpty(self):
        return len(self.queue) == 0


    def push(self, element):
        self.queue.append(element)


    def pop(self):
        try:
            minF = 0
            for i in range(len(self.queue)):
                if(self.queue[i][0] < self.queue[minF][0]):
                    minF = i
            item = self.queue[minF]
            del self.queue[minF]
            return item
        except IndexError:
            print('Error in PQ')