# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    with qml.tape.QuantumTape() as tape:
        def custom_gate():
            qml.PauliX(wires=1)
            qml.Hadamard(wires=2)
        
        controlled_op = qml.ctrl(custom_gate, control=[0, 3])
        controlled_op()
        
    return tape
