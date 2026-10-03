# EVAL_META: task_id=5, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qalloc = getattr(machine, "qAlloc_many", None)
    if qalloc is None:
        qalloc = getattr(machine, "qalloc_many")
    qubits = qalloc(2)

    prog = pq.QProg()
    prog << pq.X(qubits[0])

    if hasattr(pq, "I"):
        prog << pq.I(qubits[1])
    else:
        prog << pq.X(qubits[1]) << pq.X(qubits[1])

    if not hasattr(create_state_prep, "_resources"):
        create_state_prep._resources = []
    create_state_prep._resources.append((machine, qubits))

    return prog
