# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QuantumCircuit

def not_gate(a):
    qm = QuantumMachine()
    qubits = qm.qAlloc(8)
    circuit = QuantumCircuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            circuit.x(qubits[i])
            
    try:
        circuit.measure_all()
    except Exception:
        try:
            for q in qubits:
                circuit.measure(q)
        except Exception:
            pass

    result = qm.run(circuit, 1000)
    
    total = sum(result.values())
    if total == 0:
        return {}
        
    processed_result = {}
    for k, v in result.items():
        if isinstance(k, int):
            key_str = format(k, '08b')
        else:
            s = str(k)
            if set(s).issubset({'0', '1'}):
                key_str = s.zfill(8)
            else:
                key_str = format(int(s), '08b')
        processed_result[key_str] = v / total
        
    return processed_result
