#!/usr/bin/env python3

import select
import subprocess
import time
import threading
import traceback

class DMesgSubscriber(object):
    def __init__(self, callback):
        self.callback = callback
        self.process = None
        threading.Thread(target = self.start, daemon = True).start()

    def __del__(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def unregister(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def start(self):
        try:
            self.process = subprocess.Popen(['dmesg', '--follow'], stdout=subprocess.PIPE)
            p = select.poll()
            p.register(self.process.stdout, select.POLLIN)

            while True:
                time.sleep(0.1)

                if self.process is None:
                    break

                try:
                    lines = []
                    while p.poll(1):
                        line = self.process.stdout.readline()
                        if not line:
                            break
                        lines.append(line.decode('utf-8').strip())

                    if lines:
                        self.callback("\n".join(lines))

                except Exception:
                    traceback.print_exc()

        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    # Run test
    DMesgSubscriber(lambda msg: print("Received msg: %s" % msg))
    time.sleep(100)
