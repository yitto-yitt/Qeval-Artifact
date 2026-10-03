# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(desired_vector).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
