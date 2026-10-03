# EVAL_META: task_id=2, framework=cirq, class=2
import numpy as np
import cirq


def create_bell_statevector():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1)])
    result = cirq.Simulator().simulate(circuit)
    return result.final_state_vector
