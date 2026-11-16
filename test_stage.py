import threading
from stage import StageRunner


def test_exactly_once_receipt_under_cancellation():
    runner = StageRunner()
    worker_ready_to_commit = threading.Event()
    watchdog_fired = threading.Event()

    def pause_before_commit():
        worker_ready_to_commit.set()
        watchdog_fired.wait(timeout=2.0)

    worker_thread = threading.Thread(
        target=runner.complete_work,
        kwargs={"before_commit_hook": pause_before_commit},
    )
    worker_thread.start()

    assert worker_ready_to_commit.wait(timeout=2.0)
    runner.timeout()
    watchdog_fired.set()

    worker_thread.join(timeout=2.0)

    assert len(runner.receipts) == 1
    assert runner.receipts == ["timeout"]
