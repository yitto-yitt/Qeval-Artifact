# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.S(q[1])**-1)
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.S(q[1]))
    return circuit
