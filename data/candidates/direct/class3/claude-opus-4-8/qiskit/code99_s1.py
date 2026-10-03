# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instruction in circuit.data:
        if len(instruction.operation.params) == 0:
            new_circuit.append(instruction)
            continue
        has_unassigned = False
        for param in instruction.operation.params:
            if hasattr(param, "parameters") and len(param.parameters) > 0:
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit.append(instruction)
    return new_circuit
