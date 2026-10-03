# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, Sampler

def or_gate(a, b):
    circuit = QuantumCircuit(9, 3)
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            circuit.x(i)
        if b_bin[2-i] == '0':
            circuit.x(3+i)
            
    for i in range(3):
        if hasattr(circuit, 'ccx'):
            circuit.ccx(i, 3+i, 6+i)
        else:
            circuit.toffoli(i, 3+i, 6+i)
            
    for i in range(3):
        circuit.x(6+i)
        
    for i in range(3):
        circuit.measure(6+i, i)
        
    sampler = Sampler()
    result = sampler.run(circuit, shots=1024).result()
    
    if hasattr(result, 'get_counts'):
        counts = result.get_counts()
    elif hasattr(result, 'data'):
        counts = result[0].data.measure.get_counts()
    else:
        counts = result[0].get_counts()
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
