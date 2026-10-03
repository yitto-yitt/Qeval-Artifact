# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QProg, I

def create_quantum_circuit(n_qubits):
    circuit = QProg()
    for qubit in range(n_qubits):
        circuit << I(qubit)
    return circuit
