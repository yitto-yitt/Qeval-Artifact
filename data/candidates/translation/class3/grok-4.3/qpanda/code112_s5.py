# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit
from pyqpanda3.core import Pauli, SparsePauliOp, PauliEvolutionGate, LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qc = QCircuit(len(pauli_strings[0]))
    synthesizer = LieTrotter(reps=reps)
    for pauli_string, time in zip(pauli_strings, times):
        pauli = Pauli(pauli_string)
        hamiltonian = SparsePauliOp(pauli)
        evolution_gate = PauliEvolutionGate(hamiltonian, time)
        synthesized_circuit = synthesizer.synthesize(evolution_gate)
        qc.append(synthesized_circuit.to_gate(), range(len(pauli_string)))
    return qc
