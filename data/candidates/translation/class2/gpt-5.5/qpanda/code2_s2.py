# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_bell_statevector():
    qvm = pq.CPUQVM()

    if hasattr(qvm, "set_configure"):
        try:
            qvm.set_configure(2, 2)
        except Exception:
            pass

    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(qvm, alloc_name):
            try:
                qubits = getattr(qvm, alloc_name)(2)
                break
            except Exception:
                qubits = None

    if qubits is None:
        qubits = [0, 1]

    prog = pq.QProg()
    cnot = pq.CNOT if hasattr(pq, "CNOT") else pq.CX

    try:
        prog << pq.H(qubits[0]) << cnot(qubits[0], qubits[1])
    except Exception:
        prog.insert(pq.H(qubits[0]))
        prog.insert(cnot(qubits[0], qubits[1]))

    ran = False
    for run_name in ("directly_run", "run"):
        if hasattr(qvm, run_name):
            try:
                getattr(qvm, run_name)(prog)
                ran = True
                break
            except TypeError:
                continue

    if not ran and hasattr(pq, "directly_run"):
        pq.directly_run(prog)

    for state_name in ("get_qstate", "get_q_state", "get_statevector", "get_state_vector", "get_state"):
        if hasattr(qvm, state_name):
            return getattr(qvm, state_name)()

    if hasattr(pq, "get_qstate"):
        return pq.get_qstate()

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 backend")
