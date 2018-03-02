#! /usr/bin/python
from ansible.inventory import Inventory
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import time, os
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):


    def __init__(self, stats, verbose=None):
        super(PlaybookRunnerCallbacks, self).__init__(stats, verbose)


    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)

        if host_result.get('msg'):
            PlaybookRunnerCallbacks.error.append(host_result)


        else:
                pass

    def on_unreachable(self, host, results):
        super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
        PlaybookRunnerCallbacks.error.append(results)


    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
        PlaybookRunnerCallbacks.error.append(results)

    def on_skipped(self, host, item=None):
        super(PlaybookRunnerCallbacks, self).on_skipped(host, item)
        PlaybookRunnerCallbacks.error.append(results)



class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    def __init__(self, verbose=False):
        super(PlaybookCallbacks, self).__init__(verbose)

    def on_stats(self, stats):
        super(PlaybookCallbacks, self).on_stats(stats)
        logger.info("palybook executes completed====")


class PlayUbook(object):
    def __init__(self, host_dir, yaml_dir, getfile_path):
        self.host_dir = host_dir
        self.yaml_dir = yaml_dir
        self.getfile_path = getfile_path

    def playnow(self):
        inventory = Inventory(self.host_dir)
        stats = callbacks.AggregateStats()
        playbook_cb = PlaybookCallbacks()
        runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        results = PlayBook(playbook=self.yaml_dir, stats=stats, callbacks=playbook_cb, runner_callbacks=runner_cb,
                           inventory=inventory, forks=200, extra_vars={"dir": self.getfile_path})
        res = results.run()
        playbook_cb.on_stats(results.stats)


def core():
    hosts_dir = os.path.join(BASE_DIR, 'conf', 'hosts')
    yaml_dir = os.path.join(BASE_DIR, 'conf', 'key')
    print(hosts_dir)
    inventory = Inventory(hosts_dir)
    stats = callbacks.AggregateStats()

    playbook_cb = PlaybookCallbacks()
    runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    getfile_path = os.path.join(BASE_DIR, 'outfile', 'remote_file')
    results = PlayBook(playbook=yaml_dir, stats=stats, callbacks=playbook_cb, runner_callbacks=runner_cb,
                       inventory=inventory, forks=200, extra_vars={"dir": getfile_path})
    res = results.run()
    playbook_cb.on_stats(results.stats)
    # return runner_cb.error
    return PlaybookRunnerCallbacks.error


if __name__ == '__main__':
    core()