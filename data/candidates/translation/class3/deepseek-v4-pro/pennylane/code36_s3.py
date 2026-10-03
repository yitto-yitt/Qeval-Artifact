# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)
    dev = qml.device('default.qubit', wires=n + 1)

    @qml.qnode(dev)
    def circuit():
        for index, bit in enumerate(reversed(s)):
            if bit == '1':
                qml.CNOT(wires=[index, n])
        return qml.state()

    return circuit
