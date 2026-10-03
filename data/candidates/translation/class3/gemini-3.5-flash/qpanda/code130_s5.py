# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT

def inv_circuit(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    
    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << H(qubits[2])
    circuit << CNOT(qubits[1], qubits[3])
    circuit << CNOT(qubits[2], qubits[4])
    
    return circuit.dagger()
