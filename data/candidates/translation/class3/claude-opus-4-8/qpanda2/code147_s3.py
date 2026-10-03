# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    # Multi-controlled Y gate: 4 control qubits (0-3), 1 target qubit (4)
    # Y = i*RY(pi) up to global phase, but we implement standard MCY decomposition
    # Standard decomposition: MCY = MCU1(pi/2) @ MCX @ MCU1(-pi/2)
    # But pyQPanda doesn't have direct MCY, we use: RY gates with MCZ controls
    
    # Decomposition: Y = RZ(-pi/2) @ X @ RZ(pi/2) up to global phase
    # More direct: use the V-chain method for multi-controlled gates
    
    # Standard MCY decomposition using ancilla-free method:
    # MCY = C^4(Y) where Y on qubit 4 controlled by 0,1,2,3
    
    # Using pyQPanda's RY and multi-control structure
    # Y = [[0, -i], [i, 0]], we decompose via standard gate library
    
    # Direct approach: MCY(q0,q1,q2,q3, target=q4)
    # pyQPanda syntax: controlled rotation gates
    
    # Multi-controlled Y: We build using RY gates with MCX structure
    # Standard: apply RY(pi/2), then MC-X pattern, then RY(-pi/2) pattern
    
    # Most direct: Use RY(pi) which is Y up to global phase i
    # Controlled RY: apply multi-controlled RY
    
    qvec = qc
    # MCY = controlled Y gate on qubit 4, controlled by 0,1,2,3
    # Y = RY(pi) up to phase
    
    # Use the standard decomposition with available gates
    # pyQPanda: RY gate with multi-control
    control_qubits = [qvec[0], qvec[1], qvec[2], qvec[3]]
    target = qvec[4]
    
    # Build 4-controlled Y using Gray code or V-chain
    # Simplified: use the library's capability
    # pyQPanda RY with controls: not directly available as MCY
    
    # Standard implementation: decompose Y and use Toffoli chains
    # Y = S @ X @ S†, but for MC we use direct RY structure
    
    # Most compatible: build using elementary controlled gates
    # C4Y decomposition following standard quantum computing pattern
    
    # Using available pyQPanda gates:
    prog = QProg()
    prog << RY(qvec[4], pi/2)
    # Multi-controlled X (Toffoli-4)
    prog << X(qvec[4]).control([qvec[0], qvec[1], qvec[2], qvec[3]])
    prog << RY(qvec[4], -pi/2)
    
    return prog

machine.finalize()
