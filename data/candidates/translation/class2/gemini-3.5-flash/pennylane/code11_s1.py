# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    try:
        tape = qml.workflow.construct_tape(circuit)()
    except Exception:
        try:
            tape = qml.make_tape(circuit)()
        except Exception:
            tape = circuit
            
    wires = tape.wires if len(tape.wires) > 0 else [0]
    dev = qml.device("default.qubit", wires=wires)
    new_tape = qml.tape.QuantumScript(tape.operations, [qml.state()])
    return qml.execute([new_tape], dev)[0]
