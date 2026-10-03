# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.depolarize(0.005).on(q0),
        cirq.depolarize(0.005).on(q1),
        cirq.measure(q1, q0, key='meas')
    )
    
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    
    total = sum(counts.values())
    probs = {}
    for state, count in counts.items():
        bitstring = f"{state:02b}"
        probs[bitstring] = count / total
        
    return probs
