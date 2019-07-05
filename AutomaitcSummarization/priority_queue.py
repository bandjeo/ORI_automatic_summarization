# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        # index of existing elements, key = sentence position
        self.idx = {}

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # check if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # insert an element in the queue
    # if element already exists, keep the one with higher priority
    def insert(self, data, priority):
        if data[0].position in self.idx:
            if priority < self.idx[data[0].position].priority:
                self.idx[data[0].position].data = data
                self.idx[data[0].position].priority = priority
        else:
            elem = Element(data, priority)
            self.queue.append(elem)
            self.idx[data[0].position] = elem

    # pop an element based on Priority
    def pop(self):
        m = min(self.queue, key=lambda x: x.priority)
        self.idx.pop(m.data[0].position)
        return self.queue.pop(self.queue.index(m))

class Element(object):

    def __init__(self, data, priority):
        self.data = data
        self.priority = priority