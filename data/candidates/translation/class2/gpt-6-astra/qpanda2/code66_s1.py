# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    program = pq.QProg()
    program << pq.RY(qubits[0], float(2 * arccos(1 / sqrt(3))))
    program << pq.H(qubits[1]).control([qubits[0]])
    program << pq.CNOT(qubits[1], qubits[2])
    program << pq.CNOT(qubits[0], qubits[1])
    program << pq.X(qubits[0])
    program << pq.measure_all(qubits, cbits)

    machine.run_with_configuration(program, cbits, 1)
    return program
