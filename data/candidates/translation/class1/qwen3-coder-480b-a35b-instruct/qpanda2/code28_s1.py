# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import math

def visualize_bell_states():
    # Create QVM
    machine = pq.QVM()
    machine.init_qvm()

    # Prepare Phi Plus state
    qubits_plus = machine.qAlloc_many(2)
    cbits_plus = machine.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus.insert(pq.H(qubits_plus[0]))
    prog_plus.insert(pq.CNOT(qubits_plus[0], qubits_plus[1]))
    prog_plus.insert(pq.Measure(qubits_plus[0], cbits_plus[0]))
    prog_plus.insert(pq.Measure(qubits_plus[1], cbits_plus[1]))

    result_plus = machine.run_with_configuration(prog_plus, cbits_plus, 1000)
    
    # Prepare Phi Minus state
    qubits_minus = machine.qAlloc_many(2)
    cbits_minus = machine.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus.insert(pq.X(qubits_minus[0]))
    prog_minus.insert(pq.H(qubits_minus[0]))
    prog_minus.insert(pq.CNOT(qubits_minus[0], qubits_minus[1]))
    prog_minus.insert(pq.Measure(qubits_minus[0], cbits_minus[0]))
    prog_minus.insert(pq.Measure(qubits_minus[1], cbits_minus[1]))

    result_minus = machine.run_with_configuration(prog_minus, cbits_minus, 1000)

    # Calculate probabilities for phi plus
    phi_plus_counts = {}
    for key, value in result_plus.items():
        # Reverse the bit string to match Qiskit's convention (qubit order)
        reversed_key = key[::-1]
        phi_plus_counts[reversed_key] = value
    
    # Calculate probabilities for phi minus
    phi_minus_counts = {}
    for key, value in result_minus.items():
        # Reverse the bit string to match Qiskit's convention (qubit order)
        reversed_key = key[::-1]
        phi_minus_counts[reversed_key] = value

    # Calculate totals
    import builtins
    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    # Normalize to get probabilities
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}

    machine.finalize()
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
