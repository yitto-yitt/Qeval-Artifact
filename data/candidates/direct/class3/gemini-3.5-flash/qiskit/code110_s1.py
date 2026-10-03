# EVAL_META: task_id=110, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford, Operator
from qiskit.synthesis import synth_clifford_full

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    equivalent_circuits = []
    
    for _ in range(n):
        u = random_clifford(num_qubits)
        u_circ = synth_clifford_full(u)
        u_adj_circ = synth_clifford_full(u.adjoint())
        
        new_circ = circuit.compose(u_circ).compose(u_adj_circ)
        
        op_target = Operator(circuit)
        op_source = Operator(new_circ)
        dim = op_target.dim
        val = np.trace(op_target.adjoint().data @ op_source.data) / dim
        theta = np.angle(val)
        new_circ.global_phase -= theta
        
        equivalent_circuits.append(new_circ)
        
    return equivalent_circuits
