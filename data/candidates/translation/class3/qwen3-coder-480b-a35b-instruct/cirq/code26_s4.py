# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    q = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.measure(q[0], key='m0'))
    
    # Create a DAG representation by converting to operations list
    dag_ops = []
    for moment in circuit:
        for op in moment:
            dag_ops.append(op)
    
    # Since Cirq doesn't have a direct DAG equivalent like Qiskit,
    # we return the circuit which represents the same structure
    return circuit
