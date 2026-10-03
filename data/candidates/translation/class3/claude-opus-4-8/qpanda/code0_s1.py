# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg

def create_quantum_circuit(n_qubits):
    circuit = QCircuit(n_qubits)
    prog = QProg()
    prog << circuit
    return prog
