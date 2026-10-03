# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    circuit_without_params = qml.tape.QuantumTape()
    with circuit_without_params:
        for op in circuit.operations:
            params = op.parameters
            if all(isinstance(p, numbers.Number) for p in params):
                qml.apply(op)
    return circuit_without_params
