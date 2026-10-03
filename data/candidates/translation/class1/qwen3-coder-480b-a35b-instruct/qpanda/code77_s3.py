# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import *

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    # Create a quantum program to prepare the state
    prog = QProg()
    
    # Initialize with |0> state and then apply state preparation
    # We need to use amplitude encoding via appropriate gates
    # First reset all qubits to |0>
    for qubit in qubits:
        prog << Measure(qubit, None)  # This ensures initialization
    
    # Apply state preparation using amplitude encoding
    # In pyQPanda3, we can use U3 gates and entangling operations to create arbitrary states
    # For this implementation, we'll use the built-in state preparation functionality if available
    # Otherwise, construct the state manually
    
    # Create the state preparation circuit
    # Since pyQPanda3 may not have direct state preparation like Qiskit,
    # we'll build it using basic gates based on the amplitude vector
    
    # Reset the program
    prog = QProg()
    
    # For state preparation in pyQPanda3, we need to decompose the desired state
    # into a sequence of quantum gates
    
    # If there's a specific state preparation method in pyQPanda3, use it
    # Otherwise, we'll construct it manually using rotations
    
    # Build the circuit to prepare the given amplitudes
    # Using QAOA-style state preparation or direct gate sequences
    
    # Since pyQPanda3 has state preparation capability, let's use it
    prog << state_to_prog(amplitudes, qubits)
    
    return {"prog": prog, "qubits": qubits, "machine": machine}
