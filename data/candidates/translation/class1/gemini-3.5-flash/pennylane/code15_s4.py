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
    
    # Map classical bits to physical qubits
    meas_map = {}
    for instruction in bell_circ.data:
        if instruction.operation.name == 'measure':
            q_index = bell_circ.find_bit(instruction.qubits[0]).index
            c_index = bell_circ.find_bit(instruction.clbits[0]).index
            meas_map[c_index] = q_index
            
    # Sort in reverse order of classical bits to match Qiskit's MSB-to-LSB
    measured_qubits = [meas_map[i] for i in sorted(meas_map.keys(), reverse=True)]
    
    # Strip measurements for PennyLane conversion
    bell_circ_no_meas = QuantumCircuit(5, len(bell_circ.clbits))
    for inst in bell_circ.data:
        if inst.operation.name != 'measure':
            bell_circ_no_meas.append(inst.operation, inst.qubits, inst.clbits)
            
    dev = qml.device('qiskit.aer', wires=5, backend=simulator, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.from_qiskit(bell_circ_no_meas)()
        return qml.counts(wires=measured_qubits)
        
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
