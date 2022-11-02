# -*- coding: utf-8 -*-
import time
import threading

from exonutils.utils.pipe import Pipe

from .daemon import BaseDaemon
from .routine import BaseRoutine

__all__ = []


class SimpleService(BaseDaemon):

    def __init__(self, *args, **kwargs):
        super(SimpleService, self).__init__(*args, **kwargs)

        # buffers holding routines handlers
        self.routines = dict()

        # interval in sec to check for routines
        self.monitor_interval = 5
        # delay in sec to wait for routines exit
        self.exit_delay = 3

        self._rtlock = threading.Lock()

    def initialize(self):
        if self.routines:
            self.log.debug("loaded routines: %s"
                           % ', '.join(self.routines.keys()))
        else:
            self.log.warning("no routines loaded")

    def execute(self):
        self.check_routines()

        # wait monitoring interval
        self.sleep(self.monitor_interval)

    def terminate(self):
        self.log.info("stopping all routines")
        with self._rtlock:
            for rthnd in self.routines.values():
                rthnd.stop(suspend=True)

        self.sleep(0.05)

        def get_alive():
            return [
                rthnd.name for rthnd in self.routines.values()
                if rthnd.is_alive()]

        # check running status and wait termination
        ts = time.time() + self.exit_delay
        while time.time() < ts:
            with self._rtlock:
                if not get_alive():
                    return
            self.sleep(0.1)

        with self._rtlock:
            rt_alive = get_alive()
        if rt_alive:
            self.log.error(
                "failed stopping routines: %s" % ','.join(rt_alive))

    def add_routine(self, rthnd):
        if not isinstance(rthnd, BaseRoutine):
            raise RuntimeError("invalid routine handler: %s" % rthnd)

        with self._rtlock:
            if rthnd.name in self.routines:
                raise ValueError(
                    "duplicate routine name: %s" % rthnd.name)

            rthnd.parent = self
            self.routines[rthnd.name] = rthnd

        return True

    def del_routine(self, name):
        with self._rtlock:
            rthnd = self.routines.get(name)
            if not rthnd:
                return False

            rthnd.stop(cancel=True)
            self.sleep(0.1)
            if not rthnd.is_alive():
                del(self.routines[name])

        return True

    def start_routine(self, name):
        with self._rtlock:
            rthnd = self.routines.get(name)
            if not rthnd:
                return False

            if not rthnd.is_alive():
                self.log.info("starting routine: %s" % name)
                rthnd.start()

        return True

    def stop_routine(self, name, suspend=False, wait_exit=True):
        with self._rtlock:
            rthnd = self.routines.get(name)
            if not rthnd:
                return False

            if rthnd.is_alive():
                self.log.info("stopping routine: %s" % name)
            rthnd.stop(suspend=suspend)
            self.sleep(0.05)

        if not wait_exit:
            return True

        ts = time.time() + self.exit_delay
        while time.time() <= ts:
            with self._rtlock:
                rthnd = self.routines.get(name)
                if not (rthnd and rthnd.is_alive()):
                    return True
            self.sleep(0.1)

        self.log.error("failed stopping routine: %s" % name)
        return False

    def check_routines(self):
        with self._rtlock:
            for name in list(self.routines.keys()):
                try:
                    rthnd = self.routines.get(name)

                    # check if cacnelled routine
                    if rthnd.is_cancelled:
                        if rthnd.is_alive():
                            rthnd.stop(cancel=True)
                        else:
                            del(self.routines[name])
                        continue

                    # check if suspended routine
                    if rthnd.is_suspended:
                        if rthnd.is_alive():
                            rthnd.stop(suspend=True)
                        continue

                    # check routine status
                    if not rthnd.is_alive():
                        if rthnd.initial_run:
                            self.log.warning(
                                "found dead routine: %s" % rthnd.name)
                        self.log.info(
                            "starting routine: %s" % rthnd.name)
                        rthnd.start()

                except Exception as e:
                    self.log.error(str(e), exc_info=bool(self.debug >= 2))


# service with command management pipe
class ManagedService(SimpleService):

    # management pipe path
    manage_pipe = ''
    # management pipe max read block size
    manage_pipe_size = 1024

    # command handler callback function
    # function args: service instance and command to handle
    cmdhandler_callback = None

    def initialize(self):
        super(ManagedService, self).initialize()
        if not self.manage_pipe:
            return

        self._last_monitor = 0

        # open management pipe
        Pipe.open(self.manage_pipe, perm=0o666)
        self._pipe_lock = threading.Lock()

    def execute(self):
        if not self.manage_pipe:
            super(ManagedService, self).execute()
            return

        # check routines
        if not self._last_monitor or \
                (time.time() - self._last_monitor) >= self.monitor_interval:
            self.check_routines()
            self._last_monitor = time.time()

        # wait and handle commands
        command = Pipe.recv(
            self.manage_pipe,
            size=self.manage_pipe_size,
            timeout=max(int(self.monitor_interval / 2), 1),
            break_event=self.term_event).decode().strip()
        if command:
            self.handle_command(command)

    def terminate(self):
        # close management pipe
        if self.manage_pipe:
            Pipe.close(self.manage_pipe)
            self._pipe_lock = None

        super(ManagedService, self).terminate()

    def handle_command(self, command):
        self.log.info("command: %s" % command)

        if not self.cmdhandler_callback:
            if self.manage_pipe:
                Pipe.send(self.manage_pipe, b"REJECTED", wait_peer=False)
            self.log.warning("REJECTED, no command handler defined")
            return

        try:
            reply = self.cmdhandler_callback(self, command)
            if not reply:
                reply = 'DONE'
        except Exception as e:
            reply = 'INTERNAL_ERROR'
            self.log.error(e, exc_info=bool(self.debug >= 2))

        self.sleep(0.1)
        Pipe.send(self.manage_pipe, reply.encode(), wait_peer=False)
        self.log.info("reply: %s" % reply)
