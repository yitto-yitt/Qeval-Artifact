# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    machine = CPUQVM()
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << S(qubits[1]).control([qubits[0]])
    circuit << H(qubits[1])
    circuit << S(qubits[0]).dagger().control([qubits[1]])
    return circuit
