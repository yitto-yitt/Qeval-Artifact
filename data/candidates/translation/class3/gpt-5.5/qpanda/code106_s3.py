# EVAL_META: task_id=106, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_cnot_dihedral():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(2)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(2)
    else:
        q = [machine.qAlloc(), machine.qAlloc()]

    cnot = pq.CNOT if hasattr(pq, "CNOT") else pq.CX

    circ1 = pq.QCircuit()
    circ1 << cnot(q[0], q[1]) << pq.T(q[0])

    circ2 = pq.QCircuit()
    circ2 << cnot(q[0], q[1]) << pq.T(q[0]) << pq.X(q[1])

    composed_circ = pq.QCircuit()
    composed_circ << circ1 << circ2

    prog = pq.QProg()
    prog << composed_circ

    compose_cnot_dihedral._machine = machine
    compose_cnot_dihedral._qubits = q

    return prog
