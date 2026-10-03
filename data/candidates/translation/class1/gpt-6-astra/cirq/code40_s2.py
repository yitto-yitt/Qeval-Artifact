# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=np.complex128)
    if state.shape != (8,):
        raise ValueError("desired_vector must contain exactly 8 amplitudes.")
    if not np.isclose(np.linalg.norm(state), 1.0, rtol=1e-10, atol=1e-10):
        raise ValueError("desired_vector must be normalized.")

    qubits = cirq.LineQubit.range(3)
    ordered_qubits = qubits[::-1]
    circuit = cirq.Circuit(
        cirq.StatePreparationChannel(state).on(*ordered_qubits),
        cirq.measure(*ordered_qubits, key="meas"),
    )
    simulator = cirq.Simulator(seed=42, dtype=np.complex128)
    result = simulator.run(circuit, repetitions=4096)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(key, "03b"): value / total for key, value in counts.items()}
