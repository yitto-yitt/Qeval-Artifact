# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    q = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    
    # Create a DAG representation by converting to operations list
    # Since Cirq doesn't have a direct DAG equivalent like Qiskit,
    # we'll represent it as a circuit which maintains the operation order
    return circuit
