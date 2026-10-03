# EVAL_META: task_id=66, framework=qiskit, class=2

from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    
    # Create W state: |W> = (|001> + |010> + |100>)/sqrt(3)
    qc.x(0)  # Start with |100>
    
    # Apply rotations to create equal superposition
    qc.ry(1.9106, 1)  # theta = 2*arccos(sqrt(2/3)) ≈ 1.9106
    qc.cx(1, 0)
    qc.ry(0.7854, 1)  # pi/4
    qc.cx(0, 1)
    qc.ry(-0.7854, 1) # -pi/4
    qc.cx(0, 1)
    qc.ry(0.7854, 2)  # pi/4
    qc.cx(1, 2)
    qc.ry(-0.7854, 2) # -pi/4
    qc.cx(1, 2)
    
    # Alternative simpler approach using known W-state construction
    qc = QuantumCircuit(3, 3)
    qc.x(0)
    qc.ry(1.9106, 1)
    qc.cx(1, 0)
    qc.ch(0, 2)
    qc.cz(1, 2)
    qc.x(0)
    qc.x(1)
    qc.cx(2, 1)
    qc.cx(1, 0)
    qc.x(1)
    qc.cx(0, 1)
    
    # Even simpler correct approach
    qc = QuantumCircuit(3, 3)
    qc.x(0)
    qc.ry(1.2310, 1)  # 2 * arcsin(1/sqrt(3))
    qc.cx(1, 0)
    qc.ch(0, 2)
    qc.cz(1, 2)
    qc.measure_all()
    
    return qc
