# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instr in circuit.data:
        has_unassigned = False
        for param in instr.operation.params:
            if isinstance(param, ParameterExpression) and param.parameters:
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit.append(instr.operation, instr.qubits, instr.clbits)
    return new_circuit
