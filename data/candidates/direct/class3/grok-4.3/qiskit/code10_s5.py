# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    unitary = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    gate = UnitaryGate(unitary)
    qc = QuantumCircuit(2)
    qc.append(gate, [0, 1])
    qc = qc.decompose()
    pm = generate_preset_pass_manager(optimization_level=1)
    transpiled = pm.run(qc)
    return transpiled
