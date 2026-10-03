# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()

    try:
        if isinstance(new_circuit.global_phase, ParameterExpression) and new_circuit.global_phase.parameters:
            new_circuit.global_phase = 0
    except Exception:
        pass

    def has_unassigned_parameters(operation):
        try:
            return bool(operation.is_parameterized())
        except Exception:
            pass

        for param in getattr(operation, "params", []):
            if isinstance(param, ParameterExpression) and param.parameters:
                return True
            if hasattr(param, "parameters"):
                try:
                    if param.parameters:
                        return True
                except Exception:
                    pass
        return False

    for instruction in circuit.data:
        operation = instruction.operation
        if has_unassigned_parameters(operation):
            continue

        qubits = [new_circuit.qubits[circuit.find_bit(q).index] for q in instruction.qubits]
        clbits = [new_circuit.clbits[circuit.find_bit(c).index] for c in instruction.clbits]
        new_circuit.append(operation.copy(), qubits, clbits)

    return new_circuit
