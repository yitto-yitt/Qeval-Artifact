# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    
    noise = cirq.ConstantQubitNoiseModel(cirq.depolarize(0.01))
    simulator = cirq.DensityMatrixSimulator(noise=noise)
    result = simulator.run(circuit, repetitions=1000)
    
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    
    probs = {}
    for state, count in counts.items():
        b0 = (state >> 1) & 1
        b1 = state & 1
        qiskit_str = f"{b1}{b0}"
        probs[qiskit_str] = count / total
        
    return probs
