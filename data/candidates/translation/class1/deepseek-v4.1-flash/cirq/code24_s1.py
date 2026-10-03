# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        qubits = sorted(oracle.all_qubits())
        n = len(qubits)
        apply_oracle = lambda circuit: circuit.append(oracle)
    elif isinstance(oracle, cirq.Gate):
        n = oracle.num_qubits()
        qubits = cirq.LineQubit.range(n)
        apply_oracle = lambda circuit: circuit.append(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        qubits = sorted(oracle.qubits)
        n = len(qubits)
        apply_oracle = lambda circuit: circuit.append(oracle)
    else:
        raise TypeError("Unsupported oracle type: {}".format(type(oracle)))

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append([cirq.H(q) for q in qubits])
    apply_oracle(circuit)
    circuit.append([cirq.H(q) for q in qubits])

    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state = result.final_state_vector

    probs = {}
    for i in range(2**(n-1)):
        bits = format(i, '0{}b'.format(n-1))
        key = bits[::-1]
        prob = 0.0
        for out_bit in (0, 1):
            index = (i << 1) | out_bit
            prob += abs(state[index])**2
        probs[key] = prob
    return probs
