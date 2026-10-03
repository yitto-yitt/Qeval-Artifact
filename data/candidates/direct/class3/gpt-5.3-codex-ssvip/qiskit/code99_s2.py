# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
    for instruction, qargs, cargs in circuit.data:
        params = getattr(instruction, "params", [])
        has_unassigned = False
        for p in params:
            if hasattr(p, "parameters") and len(p.parameters) > 0:
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit.append(instruction, qargs, cargs)
    return new_circuit
