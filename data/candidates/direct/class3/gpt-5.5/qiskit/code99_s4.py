# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    def has_unassigned_parameters(value):
        if hasattr(value, "parameters"):
            try:
                return bool(value.parameters)
            except Exception:
                pass
        if isinstance(value, (list, tuple, set, frozenset)):
            return any(has_unassigned_parameters(item) for item in value)
        if isinstance(value, dict):
            return any(
                has_unassigned_parameters(key) or has_unassigned_parameters(val)
                for key, val in value.items()
            )
        return False

    new_circuit = circuit.copy()

    for index in reversed(range(len(new_circuit.data))):
        instruction = new_circuit.data[index]
        operation = getattr(instruction, "operation", instruction[0])
        if any(has_unassigned_parameters(param) for param in getattr(operation, "params", [])):
            del new_circuit.data[index]

    return new_circuit
