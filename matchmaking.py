from threading import Thread
from queue import Queue
from gamestate import Game
import time

class Matcher(Thread):

    def __init__(self, game):
        super().__init__()
        self.game = game
        # self.match_q = match_q
        
    def run(self):
        while True:
            if len(self.game) > 1:
                print('game found')
                p0 = self.game.popitem()
                p1 = self.game.popitem()

                Game(p0[1], p1[1]).start()

            time.sleep(1)
if __name__ == '__main__':
    p1q = Queue()
    p2q = Queue()

    gq = Queue()
    mq = Queue()
 
    gq.put(p1q)
    gq.put(p2q)
    match = Matcher(gq)
    match.start()



