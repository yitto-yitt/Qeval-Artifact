# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    # Qubits (Belem-like assignment – qubit pair with high connectivity)
    q0, q1 = cirq.LineQubit.range(2)

    # Build Bell circuit
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    )

    # Emulate Qiskit’s optimization level 1 on a target gateset typical for IBM devices
    gateset = cirq.Gateset(
        cirq.PhasedXPowGate,
        cirq.ZPowGate,
        cirq.CZPowGate,
        cirq.MeasurementGate,
    )
    circuit = cirq.optimize_for_target_gateset(circuit, gateset=gateset)

    # Noise model roughly mimicking FakeBelemV2 calibration data
    noise_model = cirq.ConstantQubitNoiseModel(
        {cirq.ops.PhasedXPowGate: cirq.depolarize(0.0005),
         cirq.ops.CZPowGate: cirq.depolarize(0.01),
         cirq.ops.MeasurementGate: cirq.bit_flip(0.02)}
    )

    # Simulator with noise
    simulator = cirq.DensityMatrixSimulator(noise=noise_model)

    # Run 1000 shots
    result = simulator.run(circuit, repetitions=1000)

    # Extract counts and convert to probability distribution
    hist = result.multi_measurement_histogram(keys=['result'])
    total = sum(hist.values())
    prob_dist = {}
    for outcome, count in hist.items():
        # outcome is a tuple of ints, e.g., (0,1) -> '01'
        bitstring = ''.join(str(bit) for bit in outcome)
        prob_dist[bitstring] = count / total

    return prob_dist
