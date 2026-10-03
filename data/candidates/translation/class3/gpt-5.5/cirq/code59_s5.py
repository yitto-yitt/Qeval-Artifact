# EVAL_META: task_id=59, framework=cirq, class=3
import cirq

def create_cz_gate():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[1]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.H(q[1]))
    return circuit
