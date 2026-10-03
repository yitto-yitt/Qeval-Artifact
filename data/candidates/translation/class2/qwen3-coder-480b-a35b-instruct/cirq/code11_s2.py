# EVAL_META: task_id=11, framework=cirq, class=2
import cirq
import numpy as np

def get_statevector(circuit):
    # Convert Cirq circuit to a state vector
    # Initialize the simulator
    simulator = cirq.Simulator()
    # Simulate the circuit and get the final state
    result = simulator.simulate(circuit)
    # Return the state vector as a numpy array
    return result.final_state_vector
