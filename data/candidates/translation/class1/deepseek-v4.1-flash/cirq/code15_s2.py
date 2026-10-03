# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    # Bell state preparation
    circuit.append(cirq.H(q0))
    circuit.append(cirq.depolarize(0.001).on(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.depolarize(0.01, n_qubits=2).on(q0, q1))
    # Readout error
    circuit.append(cirq.bit_flip(0.02).on(q0))
    circuit.append(cirq.bit_flip(0.02).on(q1))
    # Measurement
    circuit.append(cirq.measure(q0, q1, key='m'))
    
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
