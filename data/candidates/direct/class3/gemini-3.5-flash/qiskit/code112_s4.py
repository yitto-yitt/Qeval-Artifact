# EVAL_META: task_id=112, framework=qiskit, class=3

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter, SuzukiTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    """
    Create a quantum circuit using a product formula (LieTrotter or SuzukiTrotter)
    for a list of Pauli strings and times.
    """
    op = SparsePauliOp(pauli_strings, coeffs=times)
    gate = PauliEvolutionGate(op, time=1.0)
    
    if order == 1:
        synthesis = LieTrotter(reps=reps)
    else:
        synthesis = SuzukiTrotter(order=order, reps=reps)
        
    return synthesis.synthesize(gate)
