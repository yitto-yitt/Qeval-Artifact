# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(10)

def remove_gate_in_position(circuit, position):
    # Convert position to 0-based index
    pos = int(position)
    
    # Get all gates in the circuit
    gates = []
    for gate in circuit.get_gates():
        gates.append(gate)
    
    # Create new circuit without the gate at the specified position
    new_circuit = pq.QCircuit()
    
    for i, gate in enumerate(gates):
        if i != pos:
            new_circuit.insert(gate)
    
    # Clear original circuit and insert the new gates
    circuit = pq.QCircuit()
    for gate in new_circuit.get_gates():
        circuit.insert(gate)
        
    return circuit

machine.finalize()
