# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    class CustomGate(qml.operation.Operation):
        num_wires = 2
        @staticmethod
        def compute_decomposition(wires):
            return [qml.X(wires=wires[0]), qml.Hadamard(wires=wires[1])]

    with qml.tape.QuantumTape() as tape:
        qml.ctrl(CustomGate(wires=[1, 2]), control=[0, 3])
        
    return tape
