# EVAL_META: task_id=118, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import C3SXGate
def create_c3sx_circuit():
    qc = QuantumCircuit(4)
    qc.append(C3SXGate(), [0, 1, 2, 3])
    return qc
