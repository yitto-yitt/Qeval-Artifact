# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # In pyQPanda, we need to decompose multi-controlled gates manually
    # C3SX can be implemented as a multi-controlled X gate with 3 controls
    # Using Toffoli gates and single-qubit rotations
    
    # First, implement a multi-controlled X gate with 3 control qubits
    # We'll use ancilla-based approach for 3-controlled X gate
    
    # For C3SX (3 control, 1 target), we implement it as multi-controlled Rx(pi/2) 
    prog << pq.S(qubits[0]) << pq.S(qubits[1]) << pq.S(qubits[2])
    prog << pq.T(qubits[3])
    
    # Implement CCX (Toffoli) between qubits[0], qubits[1] as controls and qubits[3] as target
    prog << pq.H(qubits[3])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.T(qubits[3]).dagger()
    prog << pq.CNOT(qubits[1], qubits[3])
    prog << pq.T(qubits[3])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.T(qubits[3]).dagger()
    prog << pq.CNOT(qubits[0], qubits[3])
    prog << pq.T(qubits[3])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.T(qubits[3]).dagger()
    prog << pq.CNOT(qubits[1], qubits[3])
    prog << pq.T(qubits[3])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.T(qubits[3]).dagger()
    prog << pq.CNOT(qubits[0], qubits[3])
    prog << pq.T(qubits[3])
    prog << pq.H(qubits[3])
    
    return prog

# Execute the circuit to verify
result = pq.prob_run_dict(create_c3sx_circuit(), qubits)
machine.finalize()
