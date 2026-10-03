# EVAL_META: task_id=2, framework=cirq, class=2
import cirq
import numpy as np


def create_bell_statevector():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    return cirq.Simulator(dtype=np.complex128).simulate(
        circuit, qubit_order=[q0, q1], initial_state=0
    ).final_state_vector
