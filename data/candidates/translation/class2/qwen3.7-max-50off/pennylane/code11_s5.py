# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    elif hasattr(circuit, "tape"):
        tape = circuit.tape
    else:
        tape = circuit
        
    dev = qml.device("default.qubit", wires=tape.wires)
    
    with qml.queuing.AnnotatedQueue() as q:
        for op in tape.operations:
            qml.apply(op)
        qml.state()
        
    new_tape = qml.tape.QuantumScript.from_queue(q)
    return qml.execute([new_tape], device=dev, gradient_fn=None)[0]
