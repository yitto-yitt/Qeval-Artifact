# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    new_circuit.name = circuit.name
    new_circuit.global_phase = circuit.global_phase
    
    for inst in circuit.data:
        op = inst.operation if hasattr(inst, 'operation') else inst[0]
        keep = True
        for p in op.params:
            if isinstance(p, ParameterExpression) and len(p.parameters) > 0:
                keep = False
                break
        if keep:
            qargs = inst.qubits if hasattr(inst, 'qubits') else inst[1]
            cargs = inst.clbits if hasattr(inst, 'clbits') else inst[2]
            new_circuit.append(op, qargs, cargs)
            
    return new_circuit
