# EVAL_META: task_id=39, framework=cirq, class=2
import cirq

def create_uniform_superposition(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))
    return cirq.final_state_vector(circuit)
