# EVAL_META: task_id=109, framework=cirq, class=3
import cirq

def circuit():
    q = cirq.LineQubit(0)
    th = cirq.linspace(0, 2*cirq.pi, 100, key='th')
    c = cirq.Circuit([
        cirq.H(q),
        cirq.rz(th)(q),
    ])
    return c
