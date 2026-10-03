# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml

def x_measurement(circuit, qubit, clbit):
    op1 = qml.Hadamard(wires=qubit)
    op2 = qml.measure(wires=qubit)
    
    if isinstance(circuit, list):
        circuit.append(op1)
        circuit.append(op2)
    elif hasattr(circuit, "_ops"):
        circuit._ops.append(op1)
        circuit._ops.append(op2)
    elif hasattr(circuit, "operations"):
        try:
            circuit.operations.append(op1)
            circuit.operations.append(op2)
        except AttributeError:
            pass
    else:
        qml.Hadamard(wires=qubit)
        qml.measure(wires=qubit)
        
    return circuit
