# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit.circuit.library import HGate, SGate, SdgGate, XGate, YGate, ZGate, CXGate, CZGate, SwapGate

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    if num_qubits == 0:
        return [circuit.copy() for _ in range(n)]
    
    single_gates = [HGate(), SGate(), SdgGate(), XGate(), YGate(), ZGate()]
    two_gates = [CXGate(), CZGate(), SwapGate()]
    
    result = []
    for _ in range(n):
        new_circuit = circuit.copy()
        length = random.randint(1, 20)
        gates = []
        for _ in range(length):
            if num_qubits >= 2 and random.random() < 0.3:
                q1, q2 = random.sample(range(num_qubits), 2)
                gate = random.choice(two_gates)
                gates.append((gate, (q1, q2)))
            else:
                q = random.randrange(num_qubits)
                gate = random.choice(single_gates)
                gates.append((gate, (q,)))
        for gate, qubits in gates:
            new_circuit.append(gate, qubits)
        for gate, qubits in reversed(gates):
            if isinstance(gate, HGate):
                inv_gate = HGate()
            elif isinstance(gate, SGate):
                inv_gate = SdgGate()
            elif isinstance(gate, SdgGate):
                inv_gate = SGate()
            elif isinstance(gate, XGate):
                inv_gate = XGate()
            elif isinstance(gate, YGate):
                inv_gate = YGate()
            elif isinstance(gate, ZGate):
                inv_gate = ZGate()
            elif isinstance(gate, CXGate):
                inv_gate = CXGate()
            elif isinstance(gate, CZGate):
                inv_gate = CZGate()
            elif isinstance(gate, SwapGate):
                inv_gate = SwapGate()
            else:
                raise ValueError("Unknown gate")
            new_circuit.append(inv_gate, qubits)
        result.append(new_circuit)
    return result
