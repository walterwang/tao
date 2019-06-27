from threading import Thread
from queue import Queue
import time

class Matcher(Thread):

    def __init__(self, game_queue, match_q):
        self.game_q = game_q
        self.match_q = match_q

    def run(self):
        while True:
            time.sleep(1)
            if self.game_q.qsize > 1:
                p1_q = self.game_q.get()
                p2_q = self.game_q.get()

                p1_q.put('found')
                p2_q.put('found')
                
                game = Queue()
                game.put(p1_q)
                game.put(p2_q)

                self.match_q.put(game)




