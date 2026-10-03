# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    q = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q[3]).controlled_by(q[0], q[1], q[2]))
    return circuit
