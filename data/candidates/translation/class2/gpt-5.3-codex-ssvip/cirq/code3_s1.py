# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q = [cirq.LineQubit(i) for i in range(3)]
    ghz = cirq.Circuit()
    ghz.append(cirq.H(q[0]))
    ghz.append(cirq.CNOT(q[0], q[1]))
    ghz.append(cirq.CNOT(q[0], q[2]))
    ghz.append(cirq.measure(*q, key="m"))
    if drawing:
        return ghz, ghz.to_text_diagram()
    return ghz
