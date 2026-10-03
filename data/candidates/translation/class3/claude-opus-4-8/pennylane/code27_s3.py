# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    tape = qml.tape.QuantumScript(ops, [])
    dag = qml.tape.QuantumScript(tape.operations, tape.measurements)
    new_ops = list(dag.operations) + [qml.Hadamard(wires=0)]
    dag = qml.tape.QuantumScript(new_ops, dag.measurements)
    return dag
