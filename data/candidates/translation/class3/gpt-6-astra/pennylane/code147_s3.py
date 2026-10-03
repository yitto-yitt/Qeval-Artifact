# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    with qml.QueuingManager.stop_recording():
        gate = qml.ctrl(qml.PauliY(wires=4), control=[0, 1, 2, 3])
    return qml.tape.QuantumScript(
        ops=list(qc.operations) + [gate],
        measurements=list(qc.measurements),
        shots=qc.shots,
    )
