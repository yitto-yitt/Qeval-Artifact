# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(unitary)
    
    circ = pq.QCircuit()
    for inst in qiskit_circ.data:
        if hasattr(inst, 'operation'):
            op = inst.operation
            qargs = inst.qubits
        else:
            op, qargs, _ = inst
            
        gate_name = op.name
        params = [float(np.real(p)) for p in op.params]
        pq_qargs = [qubits[qiskit_circ.find_bit(q).index] for q in qargs]
        
        if gate_name in ('u', 'u3'):
            circ << pq.U3(pq_qargs[0], params[0], params[1], params[2])
        elif gate_name == 'u2':
            circ << pq.U2(pq_qargs[0], params[0], params[1])
        elif gate_name in ('u1', 'p'):
            circ << pq.U1(pq_qargs[0], params[0])
        elif gate_name == 'rz':
            circ << pq.RZ(pq_qargs[0], params[0])
        elif gate_name == 'ry':
            circ << pq.RY(pq_qargs[0], params[0])
        elif gate_name == 'rx':
            circ << pq.RX(pq_qargs[0], params[0])
        elif gate_name == 'cx':
            circ << pq.CNOT(pq_qargs[0], pq_qargs[1])
        elif gate_name == 'id':
            pass
        elif gate_name == 'sx':
            circ << pq.RX(pq_qargs[0], np.pi/2)
        elif gate_name == 'x':
            circ << pq.X(pq_qargs[0])
        elif gate_name == 'y':
            circ << pq.Y(pq_qargs[0])
        elif gate_name == 'z':
            circ << pq.Z(pq_qargs[0])
        elif gate_name == 'h':
            circ << pq.H(pq_qargs[0])
        elif gate_name == 's':
            circ << pq.S(pq_qargs[0])
        elif gate_name == 'sdg':
            circ << pq.S(pq_qargs[0]).dagger()
        elif gate_name == 't':
            circ << pq.T(pq_qargs[0])
        elif gate_name == 'tdg':
            circ << pq.T(pq_qargs[0]).dagger()

    return circ

machine.finalize()
