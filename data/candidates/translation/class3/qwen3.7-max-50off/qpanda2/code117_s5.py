# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate
from qiskit import transpile

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(unitary)
    qiskit_circ = transpile(qiskit_circ, basis_gates=['cx', 'u3'])
    
    prog = pq.QProg()
    q_map = {qiskit_circ.qubits[i]: qubits[i] for i in range(len(qiskit_circ.qubits))}
    
    for instruction in qiskit_circ.data:
        if hasattr(instruction, 'operation'):
            inst = instruction.operation
            qargs = instruction.qubits
        else:
            inst, qargs, _ = instruction
            
        gate_name = inst.name
        params = inst.params
        if gate_name == 'cx':
            prog << pq.CNOT(q_map[qargs[0]], q_map[qargs[1]])
        elif gate_name == 'u3':
            prog << pq.U3(q_map[qargs[0]], float(params[0]), float(params[1]), float(params[2]))
        elif gate_name == 'id':
            pass
            
    return prog

machine.finalize()
