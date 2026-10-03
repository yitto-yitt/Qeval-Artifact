# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def remove_gate_in_position(circuit, position):
    # Convert position to zero-based index
    gates = []
    for gate in circuit.get_gates():
        gates.append(gate)
    
    new_circuit = pq.QCircuit()
    for i, gate in enumerate(gates):
        if i != position:
            new_circuit.insert(gate)
    
    return new_circuit

machine.finalize()
