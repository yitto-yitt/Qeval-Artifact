# EVAL_META: task_id=78, framework=pennylane, class=3
import math
import pennylane as qml

def qft_no_swaps(num_qubits):
    ops = []
    for j in range(num_qubits):
        for k in range(j):
            ops.append(qml.ControlledPhaseShift(-math.pi / (2 ** (j - k)), wires=[j, k]))
        ops.append(qml.Hadamard(wires=j))
    return qml.tape.QuantumScript(ops=ops)
