# EVAL_META: task_id=37, framework=cirq, class=1
import cirq

def bv_algorithm(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    ancilla = qubits[n]
    circuit = cirq.Circuit(
        cirq.X(ancilla),
        cirq.H.on_each(qubits),
    )
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], ancilla))
    for i in range(n):
        circuit.append(cirq.H(qubits[i]))
    circuit.append(cirq.measure(*qubits[:n], key="meas"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    meas = result.measurements["meas"][0]
    bitstring = "".join(str(bit) for bit in meas)
    bitstrings = [bitstring]
    return [bitstrings, result]
