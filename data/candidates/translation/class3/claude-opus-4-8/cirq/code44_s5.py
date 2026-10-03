# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q[0]))
    circuit.append(cirq.ry(0.2).controlled().on(q[1], q[2]))
    return circuit
