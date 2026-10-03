# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import copy

def equivalent_clifford_circuit(circuit, n):
    return [copy.deepcopy(circuit) for _ in range(n)]
