# EVAL_META: task_id=71, framework=qiskit, class=3
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import CSXGate

def create_quantum_circuit_based_h0_csx01_h1():
    qr = QuantumRegister(3, 'q')
    qc = QuantumCircuit(qr)
    qc.h(qr[0])
    qc.append(CSXGate(), [qr[0], qr[1]])
    qc.h(qr[1])
    return qc
