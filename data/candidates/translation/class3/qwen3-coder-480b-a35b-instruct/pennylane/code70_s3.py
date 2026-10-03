# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    def circuit():
        qml.Hadamard(wires=0)
        qml.Toffoli(wires=[0, 1, 2])
        qml.Hadamard(wires=1)
        qml.C(S=qml.S.dag(wires=0), control_wires=1)
    return circuit
