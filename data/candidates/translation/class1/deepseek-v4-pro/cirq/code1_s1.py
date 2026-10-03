# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='m')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total_shots = sum(counts.values())
    return {format(k, '02b'): v / total_shots for k, v in counts.items()}
