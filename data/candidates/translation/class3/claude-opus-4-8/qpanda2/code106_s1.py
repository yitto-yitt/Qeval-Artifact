# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def _build_circuit():
    prog = pq.QCircuit()
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.T(qubits[0])
    return prog


def compose_cnot_dihedral():
    circ1 = _build_circuit()

    circ2 = pq.QCircuit()
    circ2 << pq.CNOT(qubits[0], qubits[1])
    circ2 << pq.T(qubits[0])
    circ2 << pq.X(qubits[1])

    composed = pq.QCircuit()
    composed << circ1 << circ2

    prog = pq.QProg()
    prog << composed

    machine.directly_run(prog)
    state = machine.get_qstate()

    result = np.array(state)
    return result
    machine.finalize()
