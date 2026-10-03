# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, ParameterExpression

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    new_circ = circuit.copy()
    new_circ.data.clear()
    
    for inst in circuit.data:
        if hasattr(inst, 'operation'):
            op = inst.operation
            qargs = inst.qubits
            cargs = inst.clbits
        else:
            op, qargs, cargs = inst
            
        has_unassigned = False
        if hasattr(op, 'params'):
            for p in op.params:
                if isinstance(p, ParameterExpression):
                    if len(p.parameters) > 0:
                        has_unassigned = True
                        break
        if not has_unassigned:
            new_circ.append(op, qargs, cargs)
            
    return new_circ
