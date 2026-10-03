# EVAL_META: task_id=92, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def calculate_stabilizer_state_info():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = bell_circuit()
    n_qubits = 2
    prob_dict = {
        format(i, f"0{n_qubits}b"): float(probs[i])
        for i in range(len(probs))
        if not np.isclose(probs[i], 0.0)
    }
    return prob_dict
