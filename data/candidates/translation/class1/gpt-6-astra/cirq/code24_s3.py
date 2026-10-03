# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
from collections import Counter


def dj_algorithm(oracle):
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(oracle.all_qubits()))
    circuit = cirq.Circuit(
        cirq.X(qubits[-1]),
        cirq.H.on_each(*qubits),
    )
    circuit += oracle
    circuit.append(cirq.H.on_each(*qubits))

    inputs = qubits[:-1]
    measurement_key = "__dj_result__"
    circuit.append(
        cirq.measure(*(inputs if inputs else qubits), key=measurement_key)
    )
    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = Counter(
        "".join(str(int(bit)) for bit in row[:len(inputs)][::-1])
        for row in result.measurements[measurement_key]
    )
    total = sum(counts.values())
    return {key: count / total for key, count in counts.items()}
