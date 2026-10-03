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
    
    # Prepare phi minus circuit
    qubits_minus = qvm.qAlloc_many(2)
    cbits_minus = qvm.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus.insert(pq.X(qubits_minus[0]))
    prog_minus.insert(pq.H(qubits_minus[0]))
    prog_minus.insert(pq.CNOT(qubits_minus[0], qubits_minus[1]))
    prog_minus.insert(pq.Measure(qubits_minus[0], cbits_minus[0]))
    prog_minus.insert(pq.Measure(qubits_minus[1], cbits_minus[1]))
    
    # Run phi plus circuit
    result_plus = pq.run_with_configuration(prog_plus, qvm, 1000)
    
    # Run phi minus circuit
    result_minus = pq.run_with_configuration(prog_minus, qvm, 1000)
    
    # Calculate probabilities for phi plus
    phi_plus_counts = {}
    for key, value in result_plus.items():
        phi_plus_counts[key] = value / 1000
    
    # Calculate probabilities for phi minus
    phi_minus_counts = {}
    for key, value in result_minus.items():
        phi_minus_counts[key] = value / 1000
    
    pq.destroy_quantum_machine(qvm)
    
    return {
        "phi_plus": phi_plus_counts,
        "phi_minus": phi_minus_counts
    }
