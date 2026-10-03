# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np
from collections import Counter

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    qiskit_order = [qubits[2], qubits[1], qubits[0]]

    state = np.asarray(desired_vector, dtype=np.complex128)
    circuit = cirq.Circuit(
        cirq.StatePreparationChannel(state).on(*qiskit_order),
        cirq.measure(*qiskit_order, key="meas"),
    )

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4096)

    counts = Counter("".join(str(int(bit)) for bit in row) for row in result.measurements["meas"])
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
