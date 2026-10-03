# EVAL_META: task_id=58, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = pq.QCircuit()
    circuit << pq.RY(qubits[1], pi / 4)
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.RY(qubits[1], -pi / 4)
    return circuit

machine.finalize()
