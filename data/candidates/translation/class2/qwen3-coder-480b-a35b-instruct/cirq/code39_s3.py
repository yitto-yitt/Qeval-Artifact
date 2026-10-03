# EVAL_META: task_id=39, framework=cirq, class=2
import cirq
import numpy as np

def create_uniform_superposition(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    return result.final_state_vector.reshape(2**n)
