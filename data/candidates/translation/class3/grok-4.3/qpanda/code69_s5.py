# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CS, CSdag

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[0]) << CS(qubits[0], qubits[1]) << H(qubits[1]) << CSdag(qubits[1], qubits[0])
    return circuit
