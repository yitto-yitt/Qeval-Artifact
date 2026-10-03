# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    ops = [qml.Hadamard(wires=0), qml.CNOT(wires=[0, 1]), qml.measure(0)]
    tape = qml.tape.QuantumTape(ops)
    dag = qml.commutation_dag(tape)
    return dag
