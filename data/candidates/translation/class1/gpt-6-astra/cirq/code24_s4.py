# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(oracle.all_qubits()))
    n = len(qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit += cirq.Circuit(oracle)
    circuit.append(cirq.H.on_each(*qubits))

    if n == 1:
        cirq.Simulator().simulate(circuit, qubit_order=qubits)
        return {"": 1.0}

    circuit.append(cirq.measure(*reversed(qubits[:-1]), key="inputs"))
    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = result.histogram(key="inputs")
    total = sum(counts.values())
    return {
        format(key, f"0{n - 1}b"): value / total
        for key, value in counts.items()
    }
