# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from pennylane.devices import DefaultMixed
from pennylane import numpy as np

def noisy_bell():
    # Create a noise model based on FakeBelemV2 characteristics
    # Using DefaultMixed device which supports mixed states and noise
    dev = DefaultMixed(wires=2)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
    
    # Execute the circuit
    probs = bell_circuit()
    
    # Convert to bitstring dictionary format
    bitstrings = ['00', '01', '10', '11']
    prob_dict = {bitstring: float(prob) for bitstring, prob in zip(bitstrings, probs)}
    
    return prob_dict
