# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    def _has_unassigned_parameters(operation):
        for param in getattr(operation, "params", []):
            if isinstance(param, ParameterExpression) and len(param.parameters) > 0:
                return True
            if hasattr(param, "parameters") and len(param.parameters) > 0:
                return True
        return False

    try:
        new_circuit = circuit.copy_empty_like()
    except Exception:
        new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
        try:
            new_circuit.global_phase = circuit.global_phase
        except Exception:
            pass
        try:
            new_circuit.metadata = dict(circuit.metadata) if circuit.metadata is not None else None
        except Exception:
            pass

    for instruction in circuit.data:
        try:
            operation = instruction.operation
            qargs = instruction.qubits
            cargs = instruction.clbits
        except AttributeError:
            operation, qargs, cargs = instruction

        if not _has_unassigned_parameters(operation):
            new_circuit.append(operation, qargs, cargs)

    return new_circuit
