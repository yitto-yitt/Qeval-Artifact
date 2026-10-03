# EVAL_META: task_id=26, framework=cirq, class=3
import cirq

def bell_dag():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, q2, key='c')
    ])
    return circuit
