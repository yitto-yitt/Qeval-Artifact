# EVAL_META: task_id=71, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit.insert(H(qubits[0]))
    circuit.insert(H(qubits[1]))
    circuit.insert(S(qubits[1]).control([qubits[0]]))
    circuit.insert(H(qubits[1]))
    circuit.insert(H(qubits[1]))
    return circuit
