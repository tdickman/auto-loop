from threading import Thread
import sys
import os

class DeadlyThread(Thread):
    def run(self):
        try:
            super(DeadlyThread, self).run()
        except Exception as e:
            print("error:", e, file=sys.stderr)
            os._exit(1)
