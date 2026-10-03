# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_quantum_circuit_with_one_qubit_and_measure():
    qr = QuantumRegister(1, "q")
    cr = ClassicalRegister(1, "c")
    qc = QuantumCircuit(qr, cr)
    qc.measure(qr[0], cr[0])
    return qc
