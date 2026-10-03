# EVAL_META: task_id=39, framework=cirq, class=2
import cirq
import numpy as np

def create_uniform_superposition(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(cirq.H(q) for q in qubits)
    simulator = cirq.Simulator(dtype=np.complex128)
    return simulator.simulate(circuit).final_state_vector.copy()
