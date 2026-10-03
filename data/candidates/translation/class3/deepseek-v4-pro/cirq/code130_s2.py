# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    q = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[1]))
    circuit.append(cirq.H(q[2]))
    circuit.append(cirq.CNOT(q[1], q[3]))
    circuit.append(cirq.CNOT(q[2], q[4]))
    return cirq.inverse(circuit)
