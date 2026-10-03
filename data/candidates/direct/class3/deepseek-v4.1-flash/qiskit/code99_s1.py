# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    def _has_unassigned(param):
        if isinstance(param, ParameterExpression):
            return bool(param.parameters)
        if isinstance(param, (list, tuple)):
            return any(_has_unassigned(p) for p in param)
        return False

    new_circuit = QuantumCircuit(
        *circuit.qregs,
        *circuit.cregs,
        name=circuit.name,
        global_phase=circuit.global_phase,
    )
    new_circuit.metadata = circuit.metadata

    for instruction in circuit.data:
        params = getattr(instruction.operation, 'params', [])
        if not any(_has_unassigned(p) for p in params):
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)

    return new_circuit
