# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(
        cirq.H(qubit),
        cirq.measure(qubit, key='result')
    )
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    measurements = result.histogram(key='result')
    
    total = sum(measurements.values())
    heads_count = measurements.get(0, 0)
    tails_count = measurements.get(1, 0)
    
    return {
        'Heads': heads_count / total,
        'Tails': tails_count / total
    }
