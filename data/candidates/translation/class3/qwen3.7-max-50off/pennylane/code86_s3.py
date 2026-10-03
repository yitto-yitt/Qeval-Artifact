# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4])
    ]
    tape = qml.tape.QuantumScript(ops, [])
    
    # PennyLane does not have a direct equivalent to Qiskit's CollectLinearFunctions pass.
    # We return the equivalent quantum tapes representing the circuits.
    return tape, tape
