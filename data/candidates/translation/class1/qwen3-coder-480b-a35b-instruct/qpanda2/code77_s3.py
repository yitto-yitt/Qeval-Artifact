# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq


def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys()) if probability_dist else 0
    num_qubits = math.ceil(math.log2(max_key + 1)) if max_key > 0 else 1
    
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    # Create the circuit
    prog = pq.QProg()
    
    # Prepare the state using amplitude encoding
    # In pyQPanda, we need to use U3 gates and entangling operations to prepare arbitrary states
    # This is more complex than Qiskit's prepare_state method
    
    # For this implementation, we'll create a state preparation circuit
    # using rotations and controlled operations based on the amplitudes
    
    # First, let's create the quantum program to initialize the desired state
    # We will use the built-in state preparation functionality if available
    # Otherwise, we'll implement it manually
    
    # Create a unitary matrix from amplitudes (this would be initialization from |0...0>)
    # We need to build the circuit that transforms |0...0> to the desired state
    
    # Initialize the circuit with a program that prepares the state
    # Using built-in state preparation in pyqpanda
    init_prog = pq.initStateToQVM(machine, qubits, amplitudes)
    
    machine.finalize()
    return init_prog
