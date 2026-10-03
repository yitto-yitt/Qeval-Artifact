# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    with qml.tape.QuantumTape() as tape:
        for i in range(2):
            qml.Hadamard(wires=i+1)
        for i in range(2):
            qml.CNOT(wires=[i+1, i+3])
    inv_ops = [qml.adjoint(op) for op in reversed(tape.ops)]
    inv_tape = qml.tape.QuantumTape(ops=inv_ops, wires=tape.wires)
    return inv_tape
