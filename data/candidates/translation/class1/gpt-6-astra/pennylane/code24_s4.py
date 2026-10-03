# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    device = qml.device("default.qubit", wires=n)

    def apply_oracle(circuit, wire_map):
        for instruction in circuit.data:
            operation = instruction.operation
            wires = [
                wire_map[circuit.find_bit(qubit).index]
                for qubit in instruction.qubits
            ]

            if operation.name in {"barrier", "delay"}:
                continue

            try:
                matrix = operation.to_matrix()
            except (AttributeError, NotImplementedError):
                definition = operation.definition
                if definition is None:
                    raise ValueError(
                        f"Cannot translate oracle operation {operation.name!r}"
                    )
                apply_oracle(definition, wires)
            else:
                qml.QubitUnitary(
                    np.asarray(matrix, dtype=complex),
                    wires=list(reversed(wires)),
                )

    @qml.set_shots(1024)
    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=n - 1)
        for wire in range(n):
            qml.Hadamard(wires=wire)

        apply_oracle(oracle, list(range(n)))

        for wire in range(n):
            qml.Hadamard(wires=wire)

        return qml.counts(wires=list(reversed(range(n - 1))))

    counts = circuit()
    total = sum(counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
