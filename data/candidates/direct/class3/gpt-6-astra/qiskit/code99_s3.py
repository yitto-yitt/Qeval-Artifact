# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    result = circuit.copy_empty_like()
    for instruction in circuit.data:
        if not instruction.operation.is_parameterized():
            result.append(instruction)
    return result
