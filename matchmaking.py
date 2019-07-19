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
                p0_id, p0_handler = self.game.popitem()
                p1_id, p1_handler = self.game.popitem()

                Game(p0_handler, p1_handler).start()

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



