# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator


def create_operator():
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    pm = generate_preset_pass_manager(optimization_level=1, backend=AerSimulator())
    transpiled = pm.run(qc)
    return transpiled
