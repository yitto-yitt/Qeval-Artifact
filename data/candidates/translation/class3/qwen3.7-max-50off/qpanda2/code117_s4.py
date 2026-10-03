# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    from qiskit.synthesis import TwoQubitBasisDecomposer
    from qiskit.circuit.library import CXGate
    
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(unitary)
    
    prog = pq.QProg()
    for instruction in qiskit_circ.data:
        if hasattr(instruction, 'operation'):
            inst = instruction.operation
            qargs = instruction.qubits
        else:
            inst, qargs, _ = instruction
            
        gate_name = inst.name
        params = [float(p) for p in inst.params]
        q_indices = [qiskit_circ.qubits.index(q) for q in qargs]
        
        if gate_name == 'cx':
            prog << pq.CNOT(qubits[q_indices[0]], qubits[q_indices[1]])
        elif gate_name in ('u3', 'u'):
            prog << pq.U3(qubits[q_indices[0]], params[0], params[1], params[2])
        elif gate_name == 'u2':
            prog << pq.U2(qubits[q_indices[0]], params[0], params[1])
        elif gate_name in ('u1', 'p'):
            prog << pq.U1(qubits[q_indices[0]], params[0])
        elif gate_name == 'rz':
            prog << pq.RZ(qubits[q_indices[0]], params[0])
        elif gate_name == 'ry':
            prog << pq.RY(qubits[q_indices[0]], params[0])
        elif gate_name == 'rx':
            prog << pq.RX(qubits[q_indices[0]], params[0])
        elif gate_name == 'id':
            pass
        elif gate_name == 'x':
            prog << pq.X(qubits[q_indices[0]])
        elif gate_name == 'y':
            prog << pq.Y(qubits[q_indices[0]])
        elif gate_name == 'z':
            prog << pq.Z(qubits[q_indices[0]])
        elif gate_name == 'h':
            prog << pq.H(qubits[q_indices[0]])
        elif gate_name == 's':
            prog << pq.S(qubits[q_indices[0]])
        elif gate_name == 't':
            prog << pq.T(qubits[q_indices[0]])
        elif gate_name == 'sx':
            prog << pq.RX(qubits[q_indices[0]], np.pi/2)
        elif gate_name == 'sdg':
            prog << pq.U1(qubits[q_indices[0]], -np.pi/2)
        elif gate_name == 'tdg':
            prog << pq.U1(qubits[q_indices[0]], -np.pi/4)
            
    return prog

machine.finalize()
