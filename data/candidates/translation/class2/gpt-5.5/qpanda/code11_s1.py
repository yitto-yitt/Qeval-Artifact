# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *


def get_statevector(circuit):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    prog = circuit
    if "QProg" in globals() and not isinstance(circuit, QProg):
        prog = QProg()
        prog << circuit

    run_ok = False
    for name in ("directly_run", "run"):
        if hasattr(qvm, name):
            try:
                getattr(qvm, name)(prog)
                run_ok = True
                break
            except TypeError:
                pass

    if not run_ok:
        try:
            qvm.execute(prog)
            run_ok = True
        except AttributeError:
            pass

    for name in ("get_qstate", "get_qstate_vector", "get_statevector", "get_state_vector"):
        if hasattr(qvm, name):
            return getattr(qvm, name)()

    if hasattr(qvm, "state"):
        return qvm.state

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 simulator")
