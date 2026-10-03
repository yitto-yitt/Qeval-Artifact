# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CSX

def create_quantum_circuit_based_h0_csx01_h1():
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.allocate_qubits(3)
    qc = QCircuit()
    qc.insert(H(qubits[0]))
    qc.insert(CSX(qubits[0], qubits[1]))
    qc.insert(H(qubits[1]))
    return qc
