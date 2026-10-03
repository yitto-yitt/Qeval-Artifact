# EVAL_META: task_id=24, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def dj_algorithm(oracle):
    n = oracle.num_qubits
    device = qml.device("default.qubit", wires=n)
    operations = []

    def translate(circuit, wires):
        for instruction in circuit.data:
            operation = instruction.operation
            targets = [wires[circuit.find_bit(q).index] for q in instruction.qubits]

            if operation.name in ("barrier", "delay"):
                continue

            try:
                matrix = operation.to_matrix()
            except (AttributeError, NotImplementedError, Exception) as error:
                definition = getattr(operation, "definition", None)
                if definition is None:
                    raise ValueError(
                        f"Cannot translate oracle operation {operation.name!r}"
                    ) from error
                translate(definition, targets)
            else:
                operations.append(
                    (np.asarray(matrix, dtype=complex), tuple(reversed(targets)))
                )

    translate(oracle, list(range(n)))

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=n - 1)
        for wire in range(n):
            qml.Hadamard(wires=wire)

        for matrix, wires in operations:
            qml.QubitUnitary(matrix, wires=wires)

        for wire in range(n):
            qml.Hadamard(wires=wire)

        return qml.counts(wires=list(reversed(range(n - 1))))

    counts = circuit()
    total = sum(counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
