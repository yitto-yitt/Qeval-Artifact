# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circ():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(0))

    circ.construct([], {})
    tape = circ.qtape

    class DAGCircuit:
        def __init__(self, tape):
            self.tape = tape
            self.operations = list(tape.operations)
            self.measurements = list(tape.measurements)

        def nodes(self):
            return self.operations + self.measurements

    return DAGCircuit(tape)
