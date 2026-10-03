# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    for instruction in circuit.data:
        if not instruction.operation.params or all(
            not getattr(param, "parameters", None) for param in instruction.operation.params
        ):
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    return new_circuit
