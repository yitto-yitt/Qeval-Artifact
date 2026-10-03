# EVAL_META: task_id=39, framework=cirq, class=2
import cirq

def create_uniform_superposition(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(cirq.H(q) for q in qubits)
    return cirq.Simulator().simulate(circuit).final_state_vector
