# EVAL_META: task_id=26, framework=cirq, class=3
import cirq
from cirq.contrib.circuitdag import CircuitDag


def bell_dag():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.measure(q[0], key="c0"),
        cirq.I(q[2]),
    )
    return CircuitDag.from_circuit(circuit)
