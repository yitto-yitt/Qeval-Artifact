# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def remove_gate_in_position(circuit, position):
    # Convert position to zero-based index if needed
    # In pyQPanda, we need to recreate the circuit without the gate at the specified position
    qubits = circuit.get_used_qubits()
    cbits = circuit.get_used_cbits()
    
    new_circuit = pq.QCircuit()
    
    # Get all gates in the original circuit
    gates = []
    for gate in circuit:
        gates.append(gate)
    
    # Add all gates except the one at the specified position
    for i, gate in enumerate(gates):
        if i != position:
            new_circuit.insert(gate)
    
    return new_circuit

machine.finalize()
