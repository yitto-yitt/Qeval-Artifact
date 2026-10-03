# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(1024)

def create_quantum_circuit(n_qubits):
    circuit = QCircuit()
    for i in range(n_qubits):
        circuit << I(qubits[i])
    return circuit

machine.finalize()
