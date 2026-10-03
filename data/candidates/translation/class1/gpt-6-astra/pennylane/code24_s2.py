# EVAL_META: task_id=24, framework=pennylane, class=1
import inspect
import numpy as np
import pennylane as qml


def dj_algorithm(oracle):
    matrix = None
    operations = None
    quantum_callable = None
    reverse_matrix_wires = False

    if isinstance(oracle, qml.tape.QuantumScript):
        wires = list(oracle.wires)
        operations = list(oracle.operations)
    elif isinstance(oracle, qml.operation.Operator):
        wires = list(oracle.wires)
        operations = [oracle]
    elif hasattr(oracle, "num_qubits") and hasattr(oracle, "data"):
        from qiskit.quantum_info import Operator

        wires = list(range(oracle.num_qubits))
        matrix = np.asarray(Operator(oracle).data, dtype=complex)
        reverse_matrix_wires = True
    elif callable(oracle):
        if hasattr(oracle, "num_qubits"):
            wires = list(range(oracle.num_qubits))
        elif hasattr(oracle, "num_wires"):
            wires = list(range(oracle.num_wires))
        elif hasattr(oracle, "wires"):
            wires = list(oracle.wires)
        else:
            raise ValueError("The oracle must specify its wires or qubit count.")
        quantum_callable = oracle
    else:
        matrix = np.asarray(oracle, dtype=complex)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("The oracle matrix must be square.")
        n = matrix.shape[0].bit_length() - 1
        if matrix.shape[0] != 2**n:
            raise ValueError("The oracle dimension must be a power of two.")
        wires = list(range(n))

    if len(wires) < 2:
        raise ValueError("The oracle must have an input register and an output qubit.")

    callable_arguments = None
    if quantum_callable is not None:
        parameters = inspect.signature(quantum_callable).parameters
        if "wires" in parameters or any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters.values()
        ):
            callable_arguments = {"wires": wires}
        else:
            callable_arguments = {}

    device = qml.device("default.qubit", wires=wires)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=wires[-1])
        for wire in wires:
            qml.Hadamard(wires=wire)

        if matrix is not None:
            unitary_wires = list(reversed(wires)) if reverse_matrix_wires else wires
            qml.QubitUnitary(matrix, wires=unitary_wires)
        elif operations is not None:
            for operation in operations:
                qml.apply(operation)
        else:
            quantum_callable(**callable_arguments)

        for wire in wires:
            qml.Hadamard(wires=wire)

        return qml.counts(wires=list(reversed(wires[:-1])))

    counts = circuit()
    total = sum(int(value) for value in counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
