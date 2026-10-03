# EVAL_META: task_id=38, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    ops = []
    ops.append(qml.Hadamard(wires=0))
    ops.append(qml.CRZ(theta, wires=[0, 1]))
    ops.append(qml.Hadamard(wires=1))
    ops.append(qml.CRY(theta, wires=[1, 0]))
    return ops
