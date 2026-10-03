# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    compiled = cirq.optimize_for_target_gateset(
        bell, gateset=cirq.CZTargetGateset()
    )

    noisy_circuit = cirq.Circuit()
    for moment in compiled:
        noisy_circuit.append(moment)
        noise_operations = []
        for operation in moment.operations:
            if len(operation.qubits) == 2:
                noise_operations.append(
                    cirq.depolarize(p=0.02, n_qubits=2).on(*operation.qubits)
                )
            else:
                noise_operations.extend(
                    cirq.depolarize(p=0.001).on(q)
                    for q in operation.qubits
                )
        noisy_circuit.append(noise_operations)

    noisy_circuit.append(
        cirq.amplitude_damp(gamma=0.01).on_each(q0, q1)
    )
    noisy_circuit.append(cirq.bit_flip(p=0.025).on_each(q0, q1))
    noisy_circuit.append(cirq.measure(q1, q0, key="meas"))

    result = cirq.DensityMatrixSimulator().run(
        noisy_circuit, repetitions=1000
    )
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {
        format(int(outcome), "02b"): int(count) / total
        for outcome, count in counts.items()
    }
