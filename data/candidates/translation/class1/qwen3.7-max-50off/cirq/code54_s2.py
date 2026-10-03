# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    qa = cirq.LineQubit.range(3)
    qb = cirq.LineQubit.range(3, 6)
    qanc = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circuit.append(cirq.X(qa[i]))
        if b_bin[2-i] == '1':
            circuit.append(cirq.X(qb[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(qa[i], qb[i], qanc[i]))
        
    circuit.append(cirq.measure(*qanc[::-1], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='m')
    
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
