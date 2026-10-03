# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(100)

def inv_circuit(n):
    circuit = QCircuit()
    circuit << CNOT(qubits[2], qubits[4])
    circuit << CNOT(qubits[1], qubits[3])
    circuit << H(qubits[2])
    circuit << H(qubits[1])
    return circuit

qvm.finalize()
