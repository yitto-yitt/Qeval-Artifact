# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_bell_statevector():
    qvm = pq.CPUQVM()

    for name in ("init_qvm", "init", "initialize"):
        if hasattr(qvm, name):
            getattr(qvm, name)()
            break

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(2)
    elif hasattr(qvm, "allocate_qubits"):
        qubits = qvm.allocate_qubits(2)
    elif hasattr(qvm, "qAlloc"):
        qubits = [qvm.qAlloc(), qvm.qAlloc()]
    elif hasattr(qvm, "qalloc"):
        qubits = [qvm.qalloc(), qvm.qalloc()]
    else:
        qubits = [qvm.allocate_qubit(), qvm.allocate_qubit()]

    prog = pq.QProg()
    h_gate = pq.H(qubits[0])
    cnot_gate = pq.CNOT(qubits[0], qubits[1]) if hasattr(pq, "CNOT") else pq.CX(qubits[0], qubits[1])

    try:
        prog << h_gate << cnot_gate
    except Exception:
        prog.insert(h_gate)
        prog.insert(cnot_gate)

    run_result = None
    for name in ("directly_run", "run", "execute"):
        if hasattr(qvm, name):
            run_result = getattr(qvm, name)(prog)
            break
    else:
        if hasattr(pq, "directly_run"):
            run_result = pq.directly_run(prog)
        else:
            run_result = pq.run(prog)

    for name in ("get_qstate", "get_qstate_vector", "get_statevector", "get_state"):
        if hasattr(qvm, name):
            return getattr(qvm, name)()

    return run_result
