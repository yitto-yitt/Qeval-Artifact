# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = pq.QProg()

    theta = 2 * arccos(1 / sqrt(3))

    # ch(0,1) via controlled-Hadamard decomposition
    def controlled_h(ctrl, tgt):
        gates = pq.QCircuit()
        gates << pq.RY(tgt, -0.7853981633974483)
        gates << pq.CNOT(ctrl, tgt)
        gates << pq.RY(tgt, 0.7853981633974483)
        return gates

    prog << pq.RY(qubits[0], theta)
    prog << controlled_h(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.X(qubits[0])

    prog << pq.measure_all(qubits, cbits)

    result = machine.run_with_configuration(prog, cbits, 1000)
    return result
