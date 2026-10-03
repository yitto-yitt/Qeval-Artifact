# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key="meas"))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(state, "08b"): count / total for state, count in counts.items()}
