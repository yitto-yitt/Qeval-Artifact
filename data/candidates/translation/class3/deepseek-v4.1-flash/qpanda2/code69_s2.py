# EVAL_META: task_id=69, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QCircuit()
    qc << H(qubits[0])
    qc << CP(qubits[0], qubits[1], PI/2)
    qc << H(qubits[1])
    qc << CP(qubits[1], qubits[0], -PI/2)
    return qc
