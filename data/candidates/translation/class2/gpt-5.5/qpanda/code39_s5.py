# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *

def create_uniform_superposition(n):
    machine_cls = globals().get("CPUQVM")
    qvm = machine_cls()

    for init_name in ("init_qvm", "initQVM", "init", "initialize"):
        init_func = getattr(qvm, init_name, None)
        if callable(init_func):
            try:
                init_func()
                break
            except TypeError:
                pass

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        alloc_func = getattr(qvm, alloc_name, None)
        if callable(alloc_func):
            try:
                qubits = alloc_func(n)
                break
            except Exception:
                pass

    if qubits is None:
        qalloc_func = getattr(qvm, "qAlloc", None) or getattr(qvm, "qalloc", None)
        if callable(qalloc_func):
            qubits = [qalloc_func() for _ in range(n)]
        else:
            qubits = list(range(n))

    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])

    ran = False
    last_error = None
    for run_name in ("directly_run", "run", "run_qprog"):
        run_func = getattr(qvm, run_name, None)
        if callable(run_func):
            try:
                run_func(prog)
                ran = True
                break
            except Exception as exc:
                last_error = exc

    if not ran and last_error is not None:
        try:
            qvm.directly_run(prog)
            ran = True
        except Exception:
            pass

    for state_name in ("get_qstate", "getQState", "get_q_state", "get_statevector", "get_state_vector", "get_state", "statevector"):
        state_attr = getattr(qvm, state_name, None)
        if callable(state_attr):
            try:
                return state_attr()
            except TypeError:
                try:
                    return state_attr(prog)
                except Exception:
                    pass
        elif state_attr is not None:
            return state_attr

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 simulator")
