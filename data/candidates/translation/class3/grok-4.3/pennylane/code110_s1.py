# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
from pennylane.ops.op_math import random_clifford

def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit)
    num_qubits = len(circuit.wires)
    qc_list = []
    counter = 0
    while counter < n:
        cliff = random_clifford(num_qubits)
        ops = cliff.decomposition()
        qc = qml.tape.QuantumScript(ops)
        op_qc = qml.matrix(qc)
        if qml.math.allclose(op_qc, op_or, rtol=0.4, atol=0.4) == True:
            counter += 1
            qc_list.append(qc)
    return qc_list
