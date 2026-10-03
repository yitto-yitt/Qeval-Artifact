# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit()
    circuit << H(qubits[0]) << CRZ(qubits[0], qubits[1], theta) << H(qubits[1]) << CRY(qubits[1], qubits[0], theta)
    return circuit
machine.finalize()
