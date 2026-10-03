# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CSWAP(qubits[0], qubits[1], qubits[2])
    circuit << H(qubits[1])
    circuit << CSDG(qubits[1], qubits[0])
    return circuit

machine.finalize()
