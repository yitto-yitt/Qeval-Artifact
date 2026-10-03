# EVAL_META: task_id=53, framework=cirq, class=1
import cirq


def xor_gate(a, b):
    # compute the classical XOR of the two 8-bit integers
    c = a ^ b

    # 8 qubits, initialised in |0⋯0>
    qubits = cirq.LineQubit.range(8)

    # build the circuit: apply an X on every qubit where the corresponding bit of c is 1
    circuit = cirq.Circuit()
    for i in range(8):
        if (c >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    # measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))

    # simulate with a reasonable number of shots (same spirit as the original Qiskit code)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)

    # extract counts
    counts = result.histogram(key='result')

    total = sum(counts.values())
    # return normalized probabilities with 8‑bit string keys (little‑endian: qubit 0 as LSB)
    return {
        format(outcome, '08b'): count / total
        for outcome, count in counts.items()
    }
