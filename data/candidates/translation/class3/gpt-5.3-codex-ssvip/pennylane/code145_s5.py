# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml


def qft_inverse(n):
    def circuit():
        qml.adjoint(qml.QFT)(wires=list(range(n)))
    return qml.tape.make_qscript(circuit)()
