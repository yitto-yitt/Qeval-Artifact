# EVAL_META: task_id=37, framework=cirq, class=1
import cirq

def bv_algorithm(s):
    n = len(s)
    q = cirq.LineQubit.range(n)
    ancilla = cirq.LineQubit(n)
    
    circuit = cirq.Circuit()
    
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*q, ancilla))
    
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(q[index], ancilla))
            
    circuit.append(cirq.H.on_each(*q))
    if n > 0:
        circuit.append(cirq.measure(*q, key='meas'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    if n > 0:
        bits = result.measurements['meas'][0]
        bitstring = ''.join(str(b) for b in reversed(bits))
    else:
        bitstring = ""
    bitstrings = [bitstring]
    
    return [bitstrings, result]
