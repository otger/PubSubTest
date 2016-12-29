#!/usr/bin/python
# -*- coding: utf-8 -*-
from .callback import Callbacks
from ..dealer.dealerclient import DealerClient
from threading import Thread, Lock
from queue import Empty
import abc
from .command import Command, CommandStatus

__author__ = 'otger'

class ExitValue(object):
    pass

class ModBase(object):

    def __init__(self, dealer, root_name):
        self._dc = DealerClient(dealer, root_name=root_name)
        self._cmd_index = 0
        self._root = root_name
        self.callbacks = Callbacks()
        self._exit = False
        self._queue_timeout = 1
        self._threads = []
        t = Thread(target=self._queue_worker)
        t.start()
        self._threads.append(t)
        self._subscribe_to_own_commands()
        self._pub_stats = {}

    def exit(self):
        self._exit = True
        self._dc.q.put(True)

    def _get_name(self):
        return self._root
    name = property(_get_name)

    def _get_pub_stats(self):
        return self._pub_stats
    pub_stats = property(_get_pub_stats)

    def _subscribe_to_own_commands(self):
        self.subscribe(callback=self._command, pattern='{0}.command'.format(self._root))

    def publish(self, path, value):
        """
        Publish a value to Dealer
        :param path: path of the variable, rootname is added in front
        :param value: any python valid value
        :return:
        """
        complete_path = '{0}.{1}'.format(self._root, path)
        self._dc.pub(complete_path, value)
        try:
            self._pub_stats[complete_path] += 1
        except Exception:
            self._pub_stats[complete_path] = 1

    def subscribe(self, callback, pattern, flags=0):
        """
        Subscribe pattern at Dealer
        :param callback: function to be executed. This function must accept a single argument of type QueueValue
        :param pattern:
        :param flags:
        :return: return identifier of the callback. To be used to be able to unsubscribe
        """
        cb = self.callbacks.add_cb(callback, pattern, flags)
        subscription = self._dc.sub(pattern=pattern, flags=flags)
        cb.set_subscription(subscription)
        return cb

    def unsubscribe(self, callback):
        """
        Remove a callback subscription
        :param callback: value returned on subscribe
        :return: None
        """
        self._dc.unsub(callback.subscription)
        self.callbacks.rem_cb(callback.ix)

    def _gen_cmd_id(self):
        self._cmd_index += 1
        return '{0}.{1}'.format(self._root, self._cmd_index)

    def get_command_instance(self, target_mod, command, arguments={}):
        """
        Get a command instance to make a request
        :param target_mod: Name of the target module to execute the command
        :param command: identifier of the command to be executed
        :param arguments: dictionary with arguments of the command
        :return: pubsub.mod.command.Command instance
        """
        cmd = Command(command_id=self._gen_cmd_id(),
                      generator_mod=self._root,
                      target_mod=target_mod,
                      command=command,
                      arguments=arguments)
        return cmd

    def request_cmd(self, target_mod, command, arguments={}, timeout=1):
        """
        Request a module to execute a command
        :param target_mod: rootname of the module which has to execute the command
        :param command: identifier of the command to execute at module
        :param arguments: dictionary of the arguments of the command
        :param timeout: raise timeout exception if time elapsed without answer is bigger than. Set to 0 to disable
                        timeout
        :return:
        """
        # cmd = self.get_command_instance(target_mod, command, arguments)
        # # ToDo: Implement timeout
        # l = Lock()
        # ans = None
        #
        # def wait_for_answer(pqv):
        #     global ans
        #     ans = pqv
        #     self.unsubscribe(cb)
        #     l.release()
        # l.acquire()
        # cb = self.subscribe(callback=wait_for_answer, pattern=cmd.get_ans_path)
        # self.publish(path=cmd.get_req_path(), value=cmd)
        # l.acquire()
        #
        # return ans
        pass

    def _queue_worker(self):
        # ToDo: send value to go out of the while
        # ToDo: This was thought as non blocking get, but for throughput it must be blocking, check, it makes sense
        while self._exit is False:
            pqv = self._dc.q.get()
            if pqv is True:
                continue
            # we got some update as a QueueValue
            # Find which _cbs met the pattern:
            cbs = self.callbacks.get_matches(pqv.path)
            for c in cbs:
                try:
                    c.function(pqv)
                except Exception as ex:
                    # log.exception()
                    #print(ex)
                    pass
            self._dc.q.task_done()
        # log.info("Queue worker exiting")

    def _command(self, pqv):
        """
        This method is registered automatically for messages arrived at:
            rootname.command
        This method calls command executer and publish its return as:
            rootname.return.cid
        Where cid is command id provided by caller
        :param pqv: QueueValue, value must be a Command instance
        :return: None
        """
        try:
            if not isinstance(pqv.value, Command):
                raise TypeError("value must be a Command instance instead of {0}".format(type(pqv.value)))
            ret = self.cmd_executer(pqv.value)
        except Exception as ex:
            ret = pqv.value
            ret.set_error(ex)
        finally:
            self.publish(path='{0}.return.{1}'.format(self._root, ret.cmd_id),
                         value=ret)

    @abc.abstractmethod
    def cmd_executer(self, cmd):
        """
        Abstract method to be filled by each module
        :param cmd: instance of Command to be executed by module
        :return: Command instance with filled values
        """
        pass

    def _get_subsnum(self):
        return len(self.callbacks)
    sub_num = property(_get_subsnum)

    def _get_qsize(self):
        return self._dc.q.qsize()
    queue_size = property(_get_qsize)

    def _get_push_q_size(self):
        return self._dc.push_queue.qsize()
    push_queue_size = property(_get_push_q_size)