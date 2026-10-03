# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    ops = []
    ops.append(qml.Hadamard(wires=0))
    ops.append(qml.CSWAP(wires=[0, 1, 2]))
    ops.append(qml.Hadamard(wires=1))
    ops.append(qml.ctrl(qml.adjoint(qml.S), control=1)(wires=0))
    return ops
