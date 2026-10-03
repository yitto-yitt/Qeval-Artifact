# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = qml.tape.QuantumTape()
    for op in circuit.operations:
        params = op.parameters
        if not params or not isinstance(params[0], qml.QueuingManager):
            with new_circuit:
                qml.apply(op)
    return new_circuit
