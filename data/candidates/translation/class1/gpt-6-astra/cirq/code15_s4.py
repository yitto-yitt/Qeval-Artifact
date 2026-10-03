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
        width = len(operation.qubits)
        duration = 35e-9 if width == 1 else 650e-9
        error_probability = 0.001 if width == 1 else 0.015
        noisy_circuit.append(
            cirq.depolarize(error_probability, n_qubits=width).on(
                *operation.qubits
            )
        )
        for qubit in operation.qubits:
            t1, t2 = (80e-6, 70e-6) if qubit == q0 else (90e-6, 80e-6)
            noisy_circuit.append(
                cirq.amplitude_damp(1.0 - np.exp(-duration / t1)).on(qubit)
            )
            pure_dephasing_rate = 1.0 / t2 - 1.0 / (2.0 * t1)
            noisy_circuit.append(
                cirq.phase_damp(
                    1.0 - np.exp(-2.0 * duration * pure_dephasing_rate)
                ).on(qubit)
            )

    for qubit, p01, p10 in ((q0, 0.02, 0.04), (q1, 0.025, 0.045)):
        readout_channel = cirq.KrausChannel(
            [
                np.diag([np.sqrt(1.0 - p01), np.sqrt(1.0 - p10)]),
                np.array([[0.0, 0.0], [np.sqrt(p01), 0.0]]),
                np.array([[0.0, np.sqrt(p10)], [0.0, 0.0]]),
            ]
        )
        noisy_circuit.append(readout_channel.on(qubit))

    noisy_circuit.append(cirq.measure(q1, q0, key="meas"))
    result = cirq.DensityMatrixSimulator().run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(int(key), "02b"): value / total for key, value in counts.items()}
