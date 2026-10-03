# EVAL_META: task_id=90, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_custom_controlled():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(4)
    
    # Create the custom gate: X on qubit 0, H on qubit 1
    inner_circuit = pq.QCircuit()
    inner_circuit.insert(pq.X(qubits[0]))
    inner_circuit.insert(pq.H(qubits[1]))
    
    # Convert to gate and add 2 controls
    custom_gate = inner_circuit.to_gate("custom")
    controlled_gate = custom_gate.control([qubits[0], qubits[3]])
    
    # Create main circuit and append the controlled gate
    main_circuit = pq.QCircuit()
    main_circuit.insert(controlled_gate)
    
    prog = pq.QProg()
    prog.insert(main_circuit)
    
    return prog
