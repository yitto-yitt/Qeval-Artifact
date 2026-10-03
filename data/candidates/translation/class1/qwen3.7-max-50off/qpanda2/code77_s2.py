# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import builtins
import pyqpanda

def state_prep(qubits, amps):
    n = len(qubits)
    circ = pyqpanda.QCircuit()
    if n == 0:
        return circ
    if n == 1:
        theta = 2 * math.acos(max(-1.0, min(1.0, amps[0])))
        circ << pyqpanda.RY(qubits[0], theta)
        return circ
    
    half = 2**(n-1)
    left = amps[:half]
    right = amps[half:]
    
    norm_left = math.sqrt(builtins.sum(x**2 for x in left))
    norm_right = math.sqrt(builtins.sum(x**2 for x in right))
    
    theta_msb = 2 * math.acos(max(-1.0, min(1.0, norm_left)))
    circ << pyqpanda.RY(qubits[0], theta_msb)
    
    if norm_left > 1e-9:
        left_amps = [x / norm_left for x in left]
        left_circ = state_prep(qubits[1:], left_amps)
        circ << pyqpanda.X(qubits[0])
        left_circ_ctrl = pyqpanda.QCircuit()
        left_circ_ctrl << left_circ
        left_circ_ctrl.set_control([qubits[0]])
        circ << left_circ_ctrl
        circ << pyqpanda.X(qubits[0])
        
    if norm_right > 1e-9:
        right_amps = [x / norm_right for x in right]
        right_circ = state_prep(qubits[1:], right_amps)
        right_circ_ctrl = pyqpanda.QCircuit()
        right_circ_ctrl << right_circ
        right_circ_ctrl.set_control([qubits[0]])
        circ << right_circ_ctrl
        
    return circ

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
        
    qmachine = pyqpanda.init_quantum_machine(pyqpanda.QMachineType.CPU, num_qubits)
    qubits = qmachine.qAlloc_many(num_qubits)
    
    circ = state_prep(qubits[::-1], amplitudes)
    
    prog = pyqpanda.QProg()
    prog << circ
    return prog
