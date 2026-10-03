# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            obs_factors = []
            for i, p in enumerate(pauli_string):
                if p == "I":
                    continue
                if p == "X":
                    obs_factors.append(qml.X(i))
                elif p == "Y":
                    obs_factors.append(qml.Y(i))
                elif p == "Z":
                    obs_factors.append(qml.Z(i))
                else:
                    raise ValueError(f"Invalid Pauli character: {p}")
            if len(obs_factors) == 0:
                continue
            op = obs_factors[0]
            for f in obs_factors[1:]:
                op = op @ f
            for _ in range(reps):
                qml.PauliRot(2.0 * time / reps, pauli_string, wires=range(n_qubits))
        return qml.state()

    circuit()
    return circuit.qtape
