# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()

def create_quantum_circuit(n_qubits):
    qubits = machine.qAlloc_many(n_qubits)
    circuit = QCircuit()
    return circuit

machine.finalize()
