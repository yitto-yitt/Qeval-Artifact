# EVAL_META: task_id=10, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    unitary = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    circuit = QuantumCircuit(2)
    circuit.append(UnitaryGate(unitary), [0, 1])
    pass_manager = generate_preset_pass_manager(optimization_level=1)
    transpiled_circuit = pass_manager.run(circuit)
    return transpiled_circuit
