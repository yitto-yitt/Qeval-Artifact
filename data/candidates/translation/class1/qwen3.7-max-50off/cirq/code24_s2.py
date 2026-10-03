# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        qubits = []
        for op in oracle.all_operations():
            for q in op.qubits:
                if q not in qubits:
                    qubits.append(q)
        n = len(qubits)
        oracle_op = oracle
    else:
        if callable(getattr(oracle, 'num_qubits', None)):
            n = oracle.num_qubits()
        elif hasattr(oracle, 'num_qubits'):
            n = oracle.num_qubits
        else:
            n = len(oracle.all_qubits())
        qubits = cirq.LineQubit.range(n)
        oracle_op = oracle.on(*qubits)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle_op)
    circuit.append(cirq.H.on_each(*qubits))
    
    circuit.append(cirq.measure(*qubits[:-1][::-1], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector
    probs = np.abs(state_vector)**2
    
    n_meas = n - 1
    prob_dict = {}
    
    for i in range(2**n):
        meas_int = i >> 1
        meas_int_rev = int(format(meas_int, f'0{n_meas}b')[::-1], 2)
        bitstring = format(meas_int_rev, f'0{n_meas}b')
        
        if bitstring not in prob_dict:
            prob_dict[bitstring] = 0.0
        prob_dict[bitstring] += probs[i]
        
    prob_dict = {k: v for k, v in prob_dict.items() if v > 1e-9}
    total = sum(prob_dict.values())
    if total > 0:
        prob_dict = {k: v / total for k, v in prob_dict.items()}
        
    return prob_dict
