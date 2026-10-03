# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    def has_unassigned_parameter(value):
        if isinstance(value, Parameter):
            return True
        if isinstance(value, ParameterExpression):
            return bool(value.parameters)
        if hasattr(value, "parameters"):
            try:
                return bool(value.parameters)
            except Exception:
                pass
        if isinstance(value, dict):
            return any(has_unassigned_parameter(k) or has_unassigned_parameter(v) for k, v in value.items())
        if isinstance(value, (list, tuple, set)):
            return any(has_unassigned_parameter(item) for item in value)
        try:
            if not isinstance(value, (str, bytes)):
                return any(has_unassigned_parameter(item) for item in value)
        except TypeError:
            pass
        return False

    def operation_has_unassigned_parameters(operation):
        try:
            if operation.is_parameterized():
                return True
        except Exception:
            pass
        return any(has_unassigned_parameter(param) for param in getattr(operation, "params", ()))

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

    for item in circuit.data:
        try:
            operation = item.operation
            qargs = item.qubits
            cargs = item.clbits
        except AttributeError:
            operation, qargs, cargs = item

        if operation_has_unassigned_parameters(operation):
            continue

        mapped_qargs = [new_circuit.qubits[circuit.qubits.index(qubit)] for qubit in qargs]
        mapped_cargs = [new_circuit.clbits[circuit.clbits.index(clbit)] for clbit in cargs]
        new_circuit.append(operation, mapped_qargs, mapped_cargs)

    return new_circuit
