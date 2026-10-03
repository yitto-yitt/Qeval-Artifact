# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << Fredkin(qubits[0], qubits[1], qubits[2])
    circ << H(qubits[1])
    
    # Decomposition of Controlled-S-dagger (control=1, target=0)
    circ << Tdag(qubits[0])
    circ << CNOT(qubits[1], qubits[0])
    circ << T(qubits[0])
    circ << CNOT(qubits[1], qubits[0])
    circ << Tdag(qubits[1])
    
    return circ

machine.finalize()
