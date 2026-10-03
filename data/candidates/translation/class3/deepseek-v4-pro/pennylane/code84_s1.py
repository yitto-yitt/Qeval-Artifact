# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    theta, phi, delta = 0.3, 0.2, 0.1
    
    U = qml.U3(theta, phi, delta, wires=0).matrix()
    
    # Apply controlled version
    qml.ctrl(qml.QubitUnitary(U, wires=1), control=0)
    
    return qml.tape.QuantumScript.from_queue(qml.queuing.AnnotatedQueue())
    
    # Alternative: directly construct and return a tape
    with qml.queuing.AnnotatedQueue() as q:
        qml.ctrl(qml.QubitUnitary(qml.U3(theta, phi, delta, wires=0).matrix(), wires=1), control=0)
    tape = qml.tape.QuantumScript.from_queue(q)
    return tape
