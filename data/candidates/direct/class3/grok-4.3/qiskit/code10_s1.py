# EVAL_META: task_id=10, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    unitary = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    qc = QuantumCircuit(2)
    qc.unitary(unitary, [0, 1])
    pm = generate_preset_pass_manager(optimization_level=1, basis_gates=["cx", "rz", "sx", "x"])
    transpiled = pm.run(qc)
    return transpiled
