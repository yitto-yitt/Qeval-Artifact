# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import math

def visualize_bell_states():
    # Create QVM
    machine = pq.QMachineType.CPU
    qvm = pq.init_quantum_machine(machine)
    
    # Prepare phi plus circuit
    qubits_plus = qvm.qAlloc_many(2)
    cbits_plus = qvm.cAlloc_many(2)
    prog_plus = pq.QProg()
    prog_plus.insert(pq.H(qubits_plus[0]))
    prog_plus.insert(pq.CNOT(qubits_plus[0], qubits_plus[1]))
    prog_plus.insert(pq.Measure(qubits_plus[0], cbits_plus[0]))
    prog_plus.insert(pq.Measure(qubits_plus[1], cbits_plus[1]))
    
    # Run phi plus circuit
    result_plus = pq.run_with_configuration(prog_plus, qvm, 1000)
    
    # Prepare phi minus circuit
    qubits_minus = qvm.qAlloc_many(2)
    cbits_minus = qvm.cAlloc_many(2)
    prog_minus = pq.QProg()
    prog_minus.insert(pq.X(qubits_minus[0]))
    prog_minus.insert(pq.H(qubits_minus[0]))
    prog_minus.insert(pq.CNOT(qubits_minus[0], qubits_minus[1]))
    prog_minus.insert(pq.Measure(qubits_minus[0], cbits_minus[0]))
    prog_minus.insert(pq.Measure(qubits_minus[1], cbits_minus[1]))
    
    # Run phi minus circuit
    result_minus = pq.run_with_configuration(prog_minus, qvm, 1000)
    
    # Calculate probabilities for phi plus
    import builtins
    total_plus = builtins.sum(result_plus.values())
    phi_plus_probs = {key: value / total_plus for key, value in result_plus.items()}
    
    # Calculate probabilities for phi minus
    total_minus = builtins.sum(result_minus.values())
    phi_minus_probs = {key: value / total_minus for key, value in result_minus.items()}
    
    # Free allocated resources
    qvm.finalize()
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
