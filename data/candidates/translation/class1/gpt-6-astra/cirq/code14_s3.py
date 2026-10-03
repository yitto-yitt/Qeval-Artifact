# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key="meas"),
    )
    bell_circ = cirq.optimize_for_target_gateset(
        bell, gateset=cirq.CZTargetGateset()
    )
    result = cirq.Simulator().run(bell_circ, repetitions=10)
    counts = Counter(
        "".join(str(int(bit)) for bit in row)
        for row in result.measurements["meas"]
    )
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
