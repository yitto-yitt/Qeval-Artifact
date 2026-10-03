# EVAL_META: task_id=69, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = qml.tape.QuantumTape()
    with qc:
        qml.Hadamard(wires=0)
        qml.ControlledPhase(0, wires=[0, 1])
        qml.Hadamard(wires=1)
        qml.ControlledPhase(0, wires=[1, 0])
    return qc
