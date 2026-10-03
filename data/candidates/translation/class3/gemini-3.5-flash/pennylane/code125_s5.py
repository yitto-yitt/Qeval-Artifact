# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    if isinstance(circ, qml.tape.QuantumTape):
        return qml.prod(*circ.operations)
    
    def gate(*args, **kwargs):
        tape = qml.make_tape(circ)(*args, **kwargs)
        return qml.prod(*tape.operations)
    return gate
