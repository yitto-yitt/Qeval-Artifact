# EVAL_META: task_id=57, framework=cirq, class=3
import cirq


def create_swap_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT.on(q0, q1))
    circuit.append(cirq.CNOT.on(q1, q0))
    circuit.append(cirq.CNOT.on(q0, q1))
    return circuit
