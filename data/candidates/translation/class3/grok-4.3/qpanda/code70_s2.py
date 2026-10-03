# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CSWAP, CSdg, qAlloc_many

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qubits = qAlloc_many(3)
    qc = QCircuit()
    qc << H(qubits[0])
    qc << CSWAP(qubits[0], qubits[1], qubits[2])
    qc << H(qubits[1])
    qc << CSdg(qubits[1], qubits[0])
    return qc
