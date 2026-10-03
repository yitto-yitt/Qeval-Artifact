# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit.circuit import Parameter, QuantumCircuit

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)
cbits = machine.cAlloc_many(32)

def remove_unassigned_parameterized_gates(circuit):
    circuit_data = circuit.data.copy()
    circuit_without_params = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    
    for instruction in circuit_data:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        has_param = False
        if hasattr(instr, 'params'):
            for p in instr.params:
                if isinstance(p, Parameter):
                    has_param = True
                    break
        if not has_param:
            circuit_without_params.append(instr, qargs, cargs)

    return circuit_without_params

machine.finalize()
