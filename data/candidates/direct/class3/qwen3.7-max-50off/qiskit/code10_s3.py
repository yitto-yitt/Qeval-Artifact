# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    U = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ]
    qc = QuantumCircuit(2)
    qc.append(UnitaryGate(U), [0, 1])
    pm = generate_preset_pass_manager(optimization_level=1)
    return pm.run(qc)
