# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(oracle.all_qubits()))
    n = len(qubits)
    circuit = cirq.Circuit(
        cirq.X(qubits[-1]),
        cirq.H.on_each(*qubits),
    )
    circuit += oracle
    circuit.append(cirq.H.on_each(*qubits))

    if n == 1:
        cirq.Simulator().simulate(circuit, qubit_order=qubits)
        return {"": 1.0}

    key = "__dj_input__"
    existing_keys = cirq.measurement_key_names(oracle)
    while key in existing_keys:
        key += "_"
    circuit.append(cirq.measure(*reversed(qubits[:-1]), key=key))

    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = result.histogram(key=key)
    total = sum(counts.values())
    return {
        format(value, f"0{n - 1}b"): count / total
        for value, count in counts.items()
    }
