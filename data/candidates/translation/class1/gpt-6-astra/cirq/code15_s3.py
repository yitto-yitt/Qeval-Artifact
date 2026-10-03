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
    t1 = 80e-6
    t2 = 70e-6

    for moment in compiled:
        noisy_circuit.append(moment)
        durations = {}
        errors = []
        for operation in moment.operations:
            two_qubit = len(operation.qubits) == 2
            duration = 350e-9 if two_qubit else 35e-9
            probability = 0.012 if two_qubit else 0.0004
            errors.append(
                cirq.depolarize(
                    probability, n_qubits=len(operation.qubits)
                ).on(*operation.qubits)
            )
            for qubit in operation.qubits:
                durations[qubit] = duration

        noisy_circuit.append(errors)
        moment_duration = max(durations.values(), default=0.0)
        for qubit in (q0, q1):
            noisy_circuit.append(
                cirq.amplitude_damp(
                    1.0 - np.exp(-moment_duration / t1)
                ).on(qubit)
            )
            noisy_circuit.append(
                cirq.phase_damp(
                    1.0
                    - np.exp(
                        -2.0 * moment_duration * (1.0 / t2 - 0.5 / t1)
                    )
                ).on(qubit)
            )

    noisy_circuit.append(cirq.bit_flip(0.025).on_each(q0, q1))
    noisy_circuit.append(cirq.measure(q1, q0, key="meas"))

    result = cirq.DensityMatrixSimulator().run(
        noisy_circuit, repetitions=1000
    )
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {
        format(int(outcome), "02b"): count / total
        for outcome, count in counts.items()
    }
