# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    control = cirq.LineQubit(0)
    target = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append((cirq.S**-1)(target))
    circuit.append(cirq.CNOT(control, target))
    circuit.append(cirq.S(target))
    return circuit
