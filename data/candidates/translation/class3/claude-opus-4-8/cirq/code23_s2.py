# EVAL_META: task_id=23, framework=cirq, class=3
import cirq

def dj_constant_oracle():
    qubits = cirq.LineQubit.range(3)
    oracle = cirq.Circuit()
    oracle.append(cirq.X(qubits[2]))
    return oracle
