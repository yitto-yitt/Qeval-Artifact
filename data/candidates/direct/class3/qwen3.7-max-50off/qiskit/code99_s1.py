# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for inst in circuit.data:
        unassigned = False
        for p in inst.operation.params:
            if isinstance(p, ParameterExpression) and p.parameters:
                unassigned = True
                break
        if not unassigned:
            new_circuit.append(inst.operation, inst.qubits, inst.clbits)
    return new_circuit
