# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits[::-1], key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {format(key, "08b"): value / total for key, value in counts.items()}
