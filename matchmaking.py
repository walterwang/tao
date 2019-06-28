from threading import Thread
from queue import Queue
import time

class Matcher(Thread):

    def __init__(self, game_q, match_q):
        super().__init__()
        self.game_q = game_q
        self.match_q = match_q

    def run(self):
        while True:
            if self.game_q.qsize() > 1:
                print('game found')
                p1_q = self.game_q.get()
                p2_q = self.game_q.get()

                p1_q.put('found')
                p2_q.put('found')
                
                game = Queue()
                game.put(p1_q)
                game.put(p2_q)

                self.match_q.put(game)

            time.sleep(1)
if __name__ == '__main__':
    p1q = Queue()
    p2q = Queue()

    gq = Queue()
    mq = Queue()
 
    gq.put(p1q)
    gq.put(p2q)
    match = Matcher(gq, mq)
    match.start()



