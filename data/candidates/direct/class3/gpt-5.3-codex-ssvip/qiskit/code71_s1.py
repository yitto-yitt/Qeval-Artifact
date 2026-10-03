# EVAL_META: task_id=71, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_quantum_circuit_based_h0_csx01_h1():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.csx(0, 1)
    qc.h(1)
    return qc
