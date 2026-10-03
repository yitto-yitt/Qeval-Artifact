# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator


def create_operator():
    target = Operator([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [1, 0, 0, 0]])
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    transpiled = transpile(qc, basis_gates=["u", "cx"], optimization_level=1)
    return transpiled
