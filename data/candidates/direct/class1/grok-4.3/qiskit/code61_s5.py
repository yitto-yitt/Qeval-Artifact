# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def create_quantum_circuit_with_one_qubit_and_measure():
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)
    qc.measure(qr, cr)
    return qc
