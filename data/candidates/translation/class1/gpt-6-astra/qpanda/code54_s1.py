# EVAL_META: task_id=54, framework=qpanda, class=1
import math
from pyqpanda3.core import CPUQVM, QProg, X, H, CNOT, RZ, measure

def and_gate(a, b):
    program = QProg()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "1":
            program << X(i)
        if b[2 - i] == "1":
            program << X(3 + i)

    for i in range(3):
        control_a, control_b, target = i, 3 + i, 6 + i
        program << H(target)
        program << CNOT(control_b, target)
        program << RZ(target, -math.pi / 4)
        program << CNOT(control_a, target)
        program << RZ(target, math.pi / 4)
        program << CNOT(control_b, target)
        program << RZ(target, -math.pi / 4)
        program << CNOT(control_a, target)
        program << RZ(control_b, math.pi / 4)
        program << RZ(target, math.pi / 4)
        program << H(target)
        program << CNOT(control_a, control_b)
        program << RZ(control_a, math.pi / 4)
        program << RZ(control_b, -math.pi / 4)
        program << CNOT(control_a, control_b)

    for i in range(3):
        program << measure(6 + i, i)

    simulator = CPUQVM()
    result = simulator.run(program, 1024)
    if not hasattr(result, "get_counts"):
        result = simulator.result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
