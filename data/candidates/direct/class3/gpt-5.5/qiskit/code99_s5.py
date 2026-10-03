# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    def has_unassigned_parameters(obj):
        if hasattr(obj, "parameters"):
            try:
                if len(obj.parameters) > 0:
                    return True
            except TypeError:
                pass

        if isinstance(obj, (list, tuple, set)):
            return any(has_unassigned_parameters(item) for item in obj)

        if isinstance(obj, dict):
            return any(
                has_unassigned_parameters(key) or has_unassigned_parameters(value)
                for key, value in obj.items()
            )

        return False

    def operation_has_unassigned_parameters(operation):
        try:
            if operation.is_parameterized():
                return True
        except Exception:
            pass

        for param in getattr(operation, "params", []):
            if has_unassigned_parameters(param):
                return True

        return False

    new_circuit = circuit.copy_empty_like()

    for instruction in circuit.data:
        try:
            operation = instruction.operation
            qargs = instruction.qubits
            cargs = instruction.clbits
        except AttributeError:
            operation, qargs, cargs = instruction

        if operation_has_unassigned_parameters(operation):
            continue

        new_qargs = [new_circuit.qubits[circuit.find_bit(qubit).index] for qubit in qargs]
        new_cargs = [new_circuit.clbits[circuit.find_bit(clbit).index] for clbit in cargs]
        new_circuit.append(operation, new_qargs, new_cargs)

    return new_circuit
