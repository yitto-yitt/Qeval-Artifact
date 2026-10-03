# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate

def create_operator():
    U = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    qc = QuantumCircuit(2)
    qc.append(UnitaryGate(U), [0, 1])
    return transpile(qc, optimization_level=1)
