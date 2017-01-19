"""

Created by: Nathan Starkweather
Created on: 03/11/2016
Created in: PyCharm Community Edition


"""
import threading
import itertools
import asyncio
__author__ = 'Nathan Starkweather'

import logging
logger = logging.getLogger(__name__)
_h = logging.StreamHandler()
_f = logging.Formatter("%(created)s %(name)s %(levelname)s (%(lineno)s): %(message)s")
_h.setFormatter(_f)
logger.addHandler(_h)
logger.propagate = False
logger.setLevel(logging.DEBUG)


class _Shutdown(Exception):
    """ Internal shutdown signal """


class AbstractEventLoop():
    _loop_id_counter = itertools.count(0)

    def __init__(self):

        self._loop_id = next(self._loop_id_counter)
        self._name = "%s id:%d" % (self.__class__.__name__, self._loop_id)
        self._stop = False
        logger.debug("Initializing Event Loop: %s", self._name)
        self._init()

    def _init(self):
        """ Optional Hook """

    def set_name(self, name):
        self._name = name

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def setup_event_loop(self):
        raise NotImplementedError

    def add_worker(self, worker):
        raise NotImplementedError


class SimpleThreadedEventLoop(AbstractEventLoop):

    # number of seconds to wait for thread to finish
    # upon killing it with join()
    thread_kill_timeout = 10.0

    def __init__(self, worker=None):
        super().__init__()
        self._worker = worker
        self.extract_worker_attrs()

    def start(self):
        self._stop = False
        self.thread = self.setup_event_loop()
        self.thread.start()

    def setup_event_loop(self):
        self.thread = threading.Thread(None, self._mainloop)
        self.thread.daemon = True
        return self.thread

    def stop(self, join=True, timeout=None):
        """
        :param join: If True, call thread's join() method after stopping.
        :type join: bool
        :param timeout: timeout argument to threading.Thread.join()
        :type timeout: int | float | None
        """
        self._stop = True
        if self.thread.is_alive():
            self._worker.should_stop = True
            self.thread.join(timeout or self.thread_kill_timeout)

    def _mainloop(self):
        """ Run the protocol's work function forever. """
        while not self._stop:
            try:
                self._worker.work_forever()
            except OSError:
                logger.exception("Unknown OS Error")
                raise

    def set_worker(self, worker):
        if self.thread.is_alive():
            logger.warning("Hotswapping worker thread while running")
            logger.warning("Thread automatically stopped: restart manually with `start()`")
            self.stop()
        self._worker = worker
        self.extract_worker_attrs()

    def add_worker(self, worker):
        logger.error("SimpleThreadedEventLoop does not support running multiple protocols")
        raise NotImplementedError

    def get_worker(self):
        return self._worker

    worker = property(get_worker)

    def extract_worker_attrs(self):
        """
        Extract attributes from worker to expose publicly.
        """
        self.drain = self._worker.drain
        self.queue = self._worker.queue


class AsyncioEventLoop(AbstractEventLoop):

    def __init__(self, loop=None, protos=()):
        super().__init__()
        self.loop = loop
        self.protos = list(protos or ())
        self.tasks = []
        self.waiter = None

    def add_worker(self, worker):
        self.protos.append(worker)
        task = self.loop.create_task(worker.work_forever_coro())
        self.tasks.append(task)

    def stop(self):
        self.loop.stop()

    @asyncio.coroutine
    def run_all_tasks(self):
        done = pending = set()

        # no need to check stop signals - just cancel self.waiter if needed
        while self.tasks:
            done, pending = yield from asyncio.wait(self.tasks)

            # mutate the task list in place. Important! to allow self
            # to reference the active task list from anywhere.
            self.tasks[:] = [t for t in self.tasks if not t.done()]

            logger.info("run_all_tasks Update:")
            logger.info("Done: %d", len(done))
            logger.info("Pending: %d", len(pending))
            logger.info("Tasks left: %d", len(self.tasks))
        return done, pending

    def start(self):
        self.waiter = asyncio.wait(self.run_all_tasks())
        self.loop.run_until_complete(self.waiter)

    def setup_event_loop(self):
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        tasks = [self.loop.create_task(p.work_forever_coro()) for p in self.protos]
        tasks.extend(self.tasks)
        self.tasks = list(set(tasks))


