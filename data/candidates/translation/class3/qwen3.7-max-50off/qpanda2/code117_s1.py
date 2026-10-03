# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    prog = pq.QProg()
    from qiskit.synthesis import TwoQubitBasisDecomposer
    from qiskit.circuit.library import CXGate
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qc = decomposer(unitary)
    
    for inst in qc.data:
        if hasattr(inst, 'operation'):
            operation = inst.operation
            qargs = inst.qubits
        else:
            operation, qargs, cargs = inst
            
        gate_name = operation.name
        params = operation.params
        qubits = [q[qarg.index] for qarg in qargs]
        
        if gate_name == 'cx':
            prog << pq.CNOT(qubits[0], qubits[1])
        elif gate_name in ['u3', 'u']:
            prog << pq.U3(qubits[0], params[0], params[1], params[2])
        elif gate_name == 'u2':
            prog << pq.U3(qubits[0], np.pi/2, params[0], params[1])
        elif gate_name in ['u1', 'p']:
            prog << pq.U1(qubits[0], params[0])
        elif gate_name == 'rx':
            prog << pq.RX(qubits[0], params[0])
        elif gate_name == 'ry':
            prog << pq.RY(qubits[0], params[0])
        elif gate_name == 'rz':
            prog << pq.RZ(qubits[0], params[0])
        elif gate_name == 'x':
            prog << pq.X(qubits[0])
        elif gate_name == 'y':
            prog << pq.Y(qubits[0])
        elif gate_name == 'z':
            prog << pq.Z(qubits[0])
        elif gate_name == 'h':
            prog << pq.H(qubits[0])
        elif gate_name == 's':
            prog << pq.S(qubits[0])
        elif gate_name == 't':
            prog << pq.T(qubits[0])
        elif gate_name == 'id':
            pass

    return prog

machine.finalize()
