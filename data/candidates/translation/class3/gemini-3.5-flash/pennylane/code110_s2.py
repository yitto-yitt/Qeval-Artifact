# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import copy

def equivalent_clifford_circuit(circuit, n):
    circuits = []
    for _ in range(n):
        try:
            circuits.append(copy.deepcopy(circuit))
        except Exception:
            try:
                circuits.append(copy.copy(circuit))
            except Exception:
                circuits.append(circuit)
    return circuits
