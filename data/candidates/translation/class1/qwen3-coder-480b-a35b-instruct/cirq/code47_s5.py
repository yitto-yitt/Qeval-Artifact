# EVAL_META: task_id=47, framework=cirq, class=1
import cirq

def random_coin_flip(samples):
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubit))
    circuit.append(cirq.measure(qubit, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=samples)
    measurements = result.measurements['result']
    
    heads_count = int(sum(1 for m in measurements if m[0] == 0))
    tails_count = int(sum(1 for m in measurements if m[0] == 1))
    
    total = heads_count + tails_count
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
