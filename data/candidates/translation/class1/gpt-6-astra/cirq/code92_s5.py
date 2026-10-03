# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np


def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    result = cirq.Simulator(dtype=np.complex128).simulate(
        circuit, qubit_order=[q1, q0]
    )
    return {
        format(index, "02b"): float(abs(amplitude) ** 2)
        for index, amplitude in enumerate(result.final_state_vector)
        if abs(amplitude) > 0
    }
