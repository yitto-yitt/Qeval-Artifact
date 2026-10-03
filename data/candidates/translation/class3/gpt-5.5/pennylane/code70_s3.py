# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    ops = [
        qml.Hadamard(wires=0),
        qml.CSWAP(wires=[0, 1, 2]),
        qml.Hadamard(wires=1),
        qml.ctrl(qml.adjoint(qml.S), control=1)(wires=0),
    ]
    return qml.tape.QuantumScript(ops, [])
