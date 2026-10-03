# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda import *

def create_swap_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(CNOT(qubits[1], qubits[0]))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    return circuit
