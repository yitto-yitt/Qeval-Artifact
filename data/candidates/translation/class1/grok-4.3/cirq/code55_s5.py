# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a, b):
    qa = cirq.NamedQubit.range(3, prefix='qa')
    qb = cirq.NamedQubit.range(3, prefix='qb')
    anc = cirq.NamedQubit.range(3, prefix='anc')
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    circuit = cirq.Circuit()
    for i in range(3):
        if a_bin[2 - i] == '0':
            circuit.append(cirq.X(qa[i]))
        if b_bin[2 - i] == '0':
            circuit.append(cirq.X(qb[i]))
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], anc[i]))
    for i in range(3):
        circuit.append(cirq.X(anc[i]))
    circuit.append(cirq.measure(*anc, key='result'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    meas = result.measurements['result']
    bitstrings = [''.join(map(str, row[::-1])) for row in meas]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
