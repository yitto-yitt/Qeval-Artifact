# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml


def dj_algorithm(oracle):
    if hasattr(oracle, "num_qubits"):
        from qiskit.quantum_info import Operator

        n = oracle.num_qubits
        matrix = Operator(oracle).data

        def apply_oracle():
            qml.QubitUnitary(matrix, wires=list(reversed(range(n))))

    else:
        if isinstance(oracle, qml.tape.QuantumScript):
            operations = oracle.operations
            oracle_wires = list(oracle.wires)
        elif isinstance(oracle, qml.operation.Operator):
            operations = [oracle]
            oracle_wires = list(oracle.wires)
        elif callable(oracle):
            tape = qml.tape.make_qscript(oracle)()
            operations = tape.operations
            oracle_wires = list(tape.wires)
        else:
            raise TypeError("Expected a quantum circuit, operator, or oracle callable.")

        if not oracle_wires:
            raise ValueError("The oracle must contain at least one qubit.")

        if all(isinstance(w, int) and w >= 0 for w in oracle_wires):
            n = max(oracle_wires) + 1
            wire_map = {w: w for w in oracle_wires}
        else:
            n = len(oracle_wires)
            wire_map = {w: i for i, w in enumerate(oracle_wires)}

        def apply_oracle():
            for operation in operations:
                qml.apply(operation.map_wires(wire_map))

    if n < 2:
        raise ValueError("The oracle must have an input register and an output qubit.")

    device = qml.device("default.qubit", wires=n)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        qml.PauliX(wires=n - 1)
        for wire in range(n):
            qml.Hadamard(wires=wire)
        apply_oracle()
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.counts(wires=list(reversed(range(n - 1))))

    counts = circuit()
    total = sum(counts.values())
    return {key: int(value) / total for key, value in counts.items()}
