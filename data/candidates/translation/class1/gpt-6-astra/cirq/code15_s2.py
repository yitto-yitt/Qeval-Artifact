# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    compiled = cirq.optimize_for_target_gateset(
        bell, gateset=cirq.CZTargetGateset()
    )

    noisy_circuit = cirq.Circuit()
    for operation in compiled.all_operations():
        noisy_circuit.append(operation)
        error_probability = 0.001 if len(operation.qubits) == 1 else 0.015
        noisy_circuit.append(
            cirq.depolarize(
                error_probability, n_qubits=len(operation.qubits)
            ).on(*operation.qubits)
        )

    # Local surrogate for backend readout errors.
    p_0_to_1, p_1_to_0 = 0.015, 0.035
    readout_channel = cirq.KrausChannel(
        [
            np.diag([np.sqrt(1 - p_0_to_1), np.sqrt(1 - p_1_to_0)]),
            np.array([[0, 0], [np.sqrt(p_0_to_1), 0]]),
            np.array([[0, np.sqrt(p_1_to_0)], [0, 0]]),
        ]
    )
    noisy_circuit.append(readout_channel.on_each(q0, q1))

    # Qiskit displays classical bits in descending index order.
    noisy_circuit.append(cirq.measure(q1, q0, key="meas"))
    result = cirq.DensityMatrixSimulator().run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(bits, "02b"): count / total for bits, count in counts.items()}
