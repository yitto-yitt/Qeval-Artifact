# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instruction in circuit.data:
        has_unassigned = any(
            isinstance(param, Parameter) or
            (hasattr(param, "parameters") and len(getattr(param, "parameters")) > 0)
            for param in instruction.operation.params
        )
        if not has_unassigned:
            new_circuit.append(instruction)
    return new_circuit
