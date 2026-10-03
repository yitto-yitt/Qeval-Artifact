# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CRZ(qubits[0], qubits[1], theta)
    circ << H(qubits[1])
    circ << CRY(qubits[1], qubits[0], theta)
    return circ

if __name__ == "__main__":
    machine.finalize()
