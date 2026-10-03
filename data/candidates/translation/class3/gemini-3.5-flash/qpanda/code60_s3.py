# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, S, CNOT

def create_cy_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    circuit = QCircuit()
    circuit << S(qubits[1]).dagger()
    circuit << CNOT(qubits[0], qubits[1])
    circuit << S(qubits[1])
    return circuit
