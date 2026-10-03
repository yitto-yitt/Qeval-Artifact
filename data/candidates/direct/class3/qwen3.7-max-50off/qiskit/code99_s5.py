# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit.parameterexpression import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for inst in circuit.data:
        if not any(isinstance(p, ParameterExpression) for p in inst.operation.params):
            new_circuit.append(inst)
    return new_circuit
