#!/usr/bin/python
import threading
import Queue


class MyQueue(Queue.Queue, object):
    def __init__(self):
        """
        MyQueue is stuck which collecting
        items and count how match items is in
        """
        super(MyQueue, self).__init__()
        self.q_sem = threading.Semaphore()
        self.len = 0

    def enq(self, item=None):
        """
        push item into stuck
        and increasing len
        :return: <ok> if ok else <ERROR:item-is-None>
        """
        if item:
            self.q_sem.acquire()
            self.put(item)
            self.q_sem.release()
            self.len += 1
            return '<OK>'
        else:
            return '<ERROR:item-is-None>'

    def deq(self):
        """
        pop iten from stuck reducing len
        :return: item if ok else <ERROR:QUEUE-IS-EMPTY>
        """
        item = '<ERROR:QUEUE-IS-EMPTY>'
        self.q_sem.acquire()
        if not self.empty():
            item = self.get()
            self.len -= 1
        self.q_sem.release()
        return item

    def status(self):
        """
        how match item in stuck
        :return: len
        """
        self.q_sem.acquire()
        l = self.len
        self.q_sem.release()
        return str(l)
