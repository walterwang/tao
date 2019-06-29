from threading import Thread
from queue import Queue
from gamestate import Game
import time

class Matcher(Thread):

    def __init__(self, game, match_q):
        super().__init__()
        self.game = game
        self.match_q = matddch_q

    def run(self):
        while True:
            if len(self.game) > 1:
                print('game found')
                p0 = self.game.popitem()
                p1 = self.game.popitem()
                p0.begn = True
                p1.begn = True

                p0.game_start('game state')
                p1.game_start('game state') 


                g = Game(p0, p1)

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



