# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])
    ops = []
    
    for pauli_string, time in zip(pauli_strings, times):
        obs_list = []
        for i, p in enumerate(pauli_string):
            if p == 'X':
                obs_list.append(qml.PauliX(i))
            elif p == 'Y':
                obs_list.append(qml.PauliY(i))
            elif p == 'Z':
                obs_list.append(qml.PauliZ(i))
                
        if not obs_list:
            ops.append(qml.GlobalPhase(time))
        else:
            obs = qml.prod(*obs_list) if len(obs_list) > 1 else obs_list[0]
            ops.append(qml.exp(obs, -1j * time))
                
    return qml.tape.QuantumScript(ops, [], num_wires)
