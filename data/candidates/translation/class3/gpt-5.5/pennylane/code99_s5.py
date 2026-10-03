# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned_parameter(param):
        if param is None:
            return False

        if isinstance(param, str):
            return True

        free_symbols = getattr(param, "free_symbols", None)
        if free_symbols is not None:
            try:
                if len(free_symbols) > 0:
                    return True
            except TypeError:
                if free_symbols:
                    return True

        params_attr = getattr(param, "parameters", None)
        module_name = param.__class__.__module__
        if params_attr is not None and "qiskit.circuit" in module_name:
            try:
                return len(params_attr) > 0
            except TypeError:
                return bool(params_attr)

        if isinstance(param, np.ndarray):
            if param.dtype == object:
                return any(is_unassigned_parameter(item) for item in param.flat)
            return False

        if isinstance(param, dict):
            return any(is_unassigned_parameter(value) for value in param.values())

        if isinstance(param, (list, tuple, set)):
            return any(is_unassigned_parameter(item) for item in param)

        return False

    def operation_has_unassigned_parameters(op):
        params = getattr(op, "parameters", getattr(op, "data", ()))
        return any(is_unassigned_parameter(param) for param in params)

    if hasattr(circuit, "operations"):
        operations = [
            op for op in circuit.operations
            if not operation_has_unassigned_parameters(op)
        ]
        measurements = list(getattr(circuit, "measurements", []))
        shots = getattr(circuit, "shots", None)
        return qml.tape.QuantumScript(operations, measurements, shots=shots)

    return [
        op for op in circuit
        if not operation_has_unassigned_parameters(op)
    ]
