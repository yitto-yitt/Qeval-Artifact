# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    new_ops = qc.operations + [qml.ctrl(qml.PauliY(wires=4), control=[0, 1, 2, 3])]
    new_tape = qml.tape.QuantumScript(new_ops, qc.measurements, shots=qc.shots)
    return new_tape
