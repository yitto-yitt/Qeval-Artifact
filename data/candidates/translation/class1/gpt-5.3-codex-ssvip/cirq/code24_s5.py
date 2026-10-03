# EVAL_META: task_id=24, framework=cirq, class=1
import cirq


def dj_algorithm(oracle):
    all_qubits = sorted(oracle.all_qubits())
    n = len(all_qubits)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(all_qubits[-1]))
    circuit.append(cirq.H.on_each(*all_qubits))
    circuit += oracle
    circuit.append(cirq.H.on_each(*all_qubits))
    circuit.append(cirq.measure(*all_qubits[:-1], key="c"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=4096)
    hist = result.multi_measurement_histogram(keys=["c"])
    total = sum(hist.values())

    probs = {}
    for bits_tuple, count in hist.items():
        bitstring = "".join(str(b) for b in bits_tuple[::-1])
        probs[bitstring] = count / total
    return probs
