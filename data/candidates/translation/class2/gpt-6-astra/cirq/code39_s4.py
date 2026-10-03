# EVAL_META: task_id=39, framework=cirq, class=2
import cirq
import numpy as np

def create_uniform_superposition(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(cirq.H.on_each(*qubits))
    result = cirq.Simulator(dtype=np.complex128).simulate(
        circuit, qubit_order=qubits[::-1]
    )
    return result.final_state_vector
