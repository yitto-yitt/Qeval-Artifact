# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, H, T, CNOT, measure


def or_gate(a, b):
    circuit = QProg()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "0":
            circuit << X(i)
        if b[2 - i] == "0":
            circuit << X(3 + i)

    for i in range(3):
        control_a, control_b, target = i, 3 + i, 6 + i
        circuit << H(target)
        circuit << CNOT(control_b, target)
        circuit << T(target).dagger()
        circuit << CNOT(control_a, target)
        circuit << T(target)
        circuit << CNOT(control_b, target)
        circuit << T(target).dagger()
        circuit << CNOT(control_a, target)
        circuit << T(control_b)
        circuit << T(target)
        circuit << H(target)
        circuit << CNOT(control_a, control_b)
        circuit << T(control_a)
        circuit << T(control_b).dagger()
        circuit << CNOT(control_a, control_b)

    for i in range(3):
        circuit << X(6 + i)
        circuit << measure(6 + i, i)

    simulator = CPUQVM()
    simulator.run(circuit, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
