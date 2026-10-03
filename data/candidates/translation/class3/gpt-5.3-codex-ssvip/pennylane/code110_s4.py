# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.wires)
    target_u = qml.matrix(circuit, wire_order=range(num_qubits))
    qc_list = []
    while len(qc_list) < n:
        candidate = qml.ops.op_math.Prod(*qml.ops.functions.clifford_t_decomposition(
            qml.random.random_clifford(wires=range(num_qubits))
        )).simplify()
        cand_u = qml.matrix(candidate, wire_order=range(num_qubits))
        if np.allclose(cand_u, target_u, rtol=0.4, atol=0.4):
            qc_list.append(candidate)
    return qc_list
