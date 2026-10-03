# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *


def create_uniform_superposition(n):
    qvm = CPUQVM()

    for init_name in ("init_qvm", "init"):
        init_method = getattr(qvm, init_name, None)
        if init_method is not None:
            init_method()
            break

    alloc_method = getattr(qvm, "qAlloc_many", None)
    if alloc_method is None:
        alloc_method = getattr(qvm, "qalloc_many")
    qubits = alloc_method(n)

    prog = QProg()
    for i in range(n):
        gate = H(qubits[i])
        try:
            prog << gate
        except Exception:
            prog.insert(gate)

    run_result = None
    for run_name in ("directly_run", "run"):
        run_method = getattr(qvm, run_name, None)
        if run_method is not None:
            run_result = run_method(prog)
            break

    for state_name in ("get_qstate", "get_q_state", "get_state", "get_state_vector", "getQState"):
        state_method = getattr(qvm, state_name, None)
        if state_method is not None:
            try:
                return state_method()
            except TypeError:
                return state_method(qubits)

    return run_result
