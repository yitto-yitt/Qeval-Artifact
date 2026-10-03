# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    q0, q1, q2 = cirq.LineQubit.range(3)
    th = [sympy.Symbol(f'θ{i}') for i in range(12)]

    moments = [
        cirq.Moment([cirq.ry(th[0])(q0), cirq.ry(th[2])(q1), cirq.ry(th[4])(q2)]),
        cirq.Moment([cirq.rz(th[1])(q0), cirq.rz(th[3])(q1), cirq.rz(th[5])(q2)]),
        cirq.Moment(),

        cirq.Moment([cirq.CNOT(q0, q1)]),
        cirq.Moment([cirq.CNOT(q0, q2)]),
        cirq.Moment([cirq.CNOT(q1, q2)]),
        cirq.Moment(),

        cirq.Moment([cirq.ry(th[6])(q0), cirq.ry(th[8])(q1), cirq.ry(th[10])(q2)]),
        cirq.Moment([cirq.rz(th[7])(q0), cirq.rz(th[9])(q1), cirq.rz(th[11])(q2)]),
        cirq.Moment(),
    ]

    return cirq.Circuit(moments)
