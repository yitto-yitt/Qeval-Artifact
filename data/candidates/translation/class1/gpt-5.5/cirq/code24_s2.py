# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    oracle_qubits = []
    if isinstance(oracle, cirq.Operation):
        oracle_qubits = list(oracle.qubits)
    elif hasattr(oracle, "all_qubits"):
        oracle_qubits = sorted(oracle.all_qubits())
    
    if oracle_qubits:
        qubits = oracle_qubits
        n = len(qubits)
    else:
        num_qubits = getattr(oracle, "num_qubits", None)
        if callable(num_qubits):
            n = int(num_qubits())
        elif num_qubits is not None:
            n = int(num_qubits)
        else:
            n = int(cirq.num_qubits(oracle))
        qubits = list(cirq.LineQubit.range(n))
    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    
    if isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    else:
        circuit.append(oracle)
    
    circuit.append(cirq.H.on_each(*qubits))
    
    result = cirq.Simulator(dtype=np.complex128).simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector
    
    probs = {}
    input_len = n - 1
    for idx, amp in enumerate(state):
        p = float(abs(amp) ** 2)
        if p <= 1e-12:
            continue
        bits = [(idx >> (n - 1 - i)) & 1 for i in range(n)]
        key = "".join(str(bits[i]) for i in range(input_len - 1, -1, -1))
        probs[key] = probs.get(key, 0.0) + p
    
    total = sum(probs.values())
    return {key: value / total for key, value in probs.items()}
