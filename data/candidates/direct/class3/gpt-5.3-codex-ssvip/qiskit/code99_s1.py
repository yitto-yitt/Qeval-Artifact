# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
    for instr, qargs, cargs in circuit.data:
        has_unassigned = False
        for p in instr.params:
            if getattr(p, "parameters", None):
                if len(p.parameters) > 0:
                    has_unassigned = True
                    break
        if not has_unassigned:
            new_circuit.append(instr.copy(), qargs, cargs)
    return new_circuit
