# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def noisy_bell():
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()
    
    device_backend = FakeBelemV2()
    simulator = AerSimulator.from_backend(device_backend)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    bell_circ = pass_manager.run(bell)
    
    # Extract measurement mapping to preserve the correct bit ordering
    bit_map = {}
    for op in bell_circ.data:
        if op.operation.name == 'measure':
            q_idx = bell_circ.find_bit(op.qubits[0]).index
            c_idx = bell_circ.find_bit(op.clbits[0]).index
            bit_map[c_idx] = q_idx
            
    measured_wires = [bit_map[1], bit_map[0]]
    
    # Create a copy of the circuit without measurements for PennyLane conversion
    bell_no_meas = bell_circ.copy()
    bell_no_meas.data = [op for op in bell_no_meas.data if op.operation.name != 'measure']
    
    # Initialize the PennyLane device with the Qiskit Aer simulator backend
    dev = qml.device('qiskit.aer', wires=5, backend=simulator, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.from_qiskit(bell_no_meas)()
        return qml.counts(wires=measured_wires)
        
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
