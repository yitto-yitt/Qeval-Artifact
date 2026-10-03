# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    # Create the base quantum program for the custom gate
    base_prog = pq.QProg()
    q_base = machine.qAlloc_many(2)
    
    # Apply X gate on qubit 0 and H gate on qubit 1
    base_prog << pq.X(q_base[0]) << pq.H(q_base[1])
    
    # Convert to a custom gate (in pyQPanda we use QProg directly)
    # For controlled version, we need to construct the full program with control logic
    
    # Create the main program with 4 qubits
    main_prog = pq.QProg()
    
    # Apply the custom operation controlled by qubits 0 and 3, acting on qubits 1 and 2
    # In pyQPanda, we can use CNOT and other controlled operations
    # We'll implement the double-controlled operation manually
    
    # To implement a double-controlled operation where both qubits 0 and 3 are controls
    # for the operation (X on qubit 1 and H on qubit 2), we need to build it step by step
    
    # First, create a temporary ancilla qubit if needed or use multi-control directly
    # PyQPanda supports multi-controlled gates via control flow
    main_prog << pq.Toffoli(qubits[0], qubits[3], qubits[1]).control({qubits[0], qubits[3]}) << pq.X(qubits[1])
    main_prog << pq.Toffoli(qubits[0], qubits[3], qubits[2]).control({qubits[0], qubits[3]}) << pq.H(qubits[2])
    
    # Actually, in pyQPanda, we should implement this differently
    # Reset the program and implement correctly
    main_prog = pq.QProg()
    
    # Implement double controlled X on qubits[1] and H on qubits[2]
    # Using Toffoli gate to implement control logic
    # We need to implement the equivalent of controlled custom gate
    
    # Build the controlled gate operation manually
    # When both qubits[0] and qubits[3] are 1, apply X on qubits[1] and H on qubits[2]
    main_prog << pq.Toffoli(qubits[0], qubits[3], qubits[1]).control({qubits[0], qubits[3]}) << pq.X(qubits[1])
    main_prog << pq.Toffoli(qubits[0], qubits[3], qubits[2]).control({qubits[0], qubits[3]}) << pq.H(qubits[2])
    
    # Correct implementation using conditional execution
    main_prog = pq.QProg()
    
    # Create a temporary program that represents the operation to be controlled
    temp_prog = pq.QProg()
    temp_prog << pq.X(qubits[1]) << pq.H(qubits[2])
    
    # Apply the operation controlled by both qubits[0] and qubits[3]
    # In pyQPanda, we can use control flow or multi-controlled gates
    controlled_prog = pq.QCircuit()
    controlled_prog << pq.X(qubits[1]) << pq.H(qubits[2])
    controlled_circuit = controlled_prog.control({qubits[0], qubits[3]})
    
    main_prog << controlled_circuit
    
    return main_prog

machine.finalize()
