# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    
    # Transpile the circuit to a standard target gateset
    circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.CZTargetGateset())
    
    # Simulate with depolarizing noise to mimic a noisy device
    simulator = cirq.Simulator(noise=cirq.depolarize(p=0.02))
    result = simulator.run(circuit, repetitions=1000)
    
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    
    return {f"{state:02b}": value / total for state, value in counts.items()}
