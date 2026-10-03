# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def create_operator():
    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.x(1)
    pass_manager = generate_preset_pass_manager(
        optimization_level=1, basis_gates=["u", "cx"]
    )
    return pass_manager.run(circuit)
