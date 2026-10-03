# EVAL_META: task_id=50, framework=qpanda, class=3

def remove_gate_in_position(circuit, position):
    nodes = []
    for node in circuit:
        nodes.append(node)
    
    del nodes[position]
    
    new_circuit = type(circuit)()
    for node in nodes:
        new_circuit.insert(node)
        
    return new_circuit
