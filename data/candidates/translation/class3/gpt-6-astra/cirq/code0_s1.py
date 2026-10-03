# EVAL_META: task_id=0, framework=cirq, class=3
import cirq

def create_quantum_circuit(n_qubits):
    return cirq.Circuit(cirq.I.on_each(cirq.LineQubit.range(n_qubits)))
