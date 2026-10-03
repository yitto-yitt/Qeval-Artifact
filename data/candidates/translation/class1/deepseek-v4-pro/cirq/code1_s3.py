# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
import numpy as np

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
