# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << SX(qubits[1]).control([qubits[0]])
    circuit << H(qubits[1])
    return circuit

machine.finalize()
