# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    prog << pq.H(qubits[1]).control(qubits[0])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.X(qubits[0])
    prog << pq.measure_all(qubits, cbits)

    result = machine.run_with_configuration(prog, cbits, 1024)
    machine.finalize()
    return result
