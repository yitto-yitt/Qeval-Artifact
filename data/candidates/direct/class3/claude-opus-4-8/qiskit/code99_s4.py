# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instruction in circuit.data:
        if len(instruction.operation.params) == 0 or not any(
            len(getattr(param, "parameters", set())) > 0 for param in instruction.operation.params
        ):
            new_circuit.append(instruction)
    return new_circuit
