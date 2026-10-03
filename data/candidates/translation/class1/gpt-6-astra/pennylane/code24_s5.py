# EVAL_META: task_id=24, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def dj_algorithm(oracle):
    n = oracle.num_qubits
    device = qml.device("default.qubit", wires=n)

    def apply_operation(operation, wires):
        if operation.name in ("barrier", "delay"):
            return

        try:
            matrix = operation.to_matrix()
        except Exception:
            matrix = None

        if matrix is not None:
            qml.QubitUnitary(
                np.asarray(matrix, dtype=complex),
                wires=list(reversed(wires)),
            )
            return

        definition = getattr(operation, "definition", None)
        if definition is None:
            raise ValueError(f"Cannot translate oracle operation {operation.name!r}")
        apply_circuit(definition, wires)

    def apply_circuit(circuit, wires):
        for instruction in circuit.data:
            mapped_wires = [
                wires[circuit.find_bit(qubit).index]
                for qubit in instruction.qubits
            ]
            apply_operation(instruction.operation, mapped_wires)

    @qml.qnode(device)
    def routine():
        qml.PauliX(wires=n - 1)
        for wire in range(n):
            qml.Hadamard(wires=wire)

        if hasattr(oracle, "data"):
            apply_circuit(oracle, list(range(n)))
        else:
            apply_operation(oracle, list(range(n)))

        for wire in range(n):
            qml.Hadamard(wires=wire)

        return qml.counts(wires=list(range(n - 2, -1, -1)))

    counts = qml.set_shots(routine, shots=1024)()
    total = sum(counts.values())
    return {key: float(value / total) for key, value in counts.items()}
