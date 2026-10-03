# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
    for instruction, qargs, cargs in circuit.data:
        has_unassigned = False
        for param in instruction.params:
            if isinstance(param, ParameterExpression) and param.parameters:
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit.append(instruction, qargs, cargs)
    return new_circuit
