# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml


def qft_no_swaps(num_qubits):
    def circuit():
        for i in range(num_qubits):
            target = num_qubits - 1 - i
            for j in range(i):
                control = num_qubits - 1 - j
                angle = -qml.numpy.pi / (2 ** (i - j))
                qml.ControlledPhaseShift(angle, wires=[control, target])
            qml.Hadamard(wires=target)

    return qml.tape.QuantumTape.from_queue(qml.queuing.AnnotatedQueue(), lambda: circuit())
