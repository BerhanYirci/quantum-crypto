## Access Lagrange quantum computer
To test your access to the quantum computer follow the subsequent points:
- install [uv package](https://docs.astral.sh/uv/getting-started/installation/);
- run `uv sync`;
- run the command `lagrangeclient`;
- you should now have a file on the directory called `token.json`;
- parse the file and extract your api token;
- run your circuit with the following code:
```
from iqm import qiskit_iqm
from iqm.qiskit_iqm import IQMProvider
from qiskit import transpile

# Here define computer urls
iqm_url = "https://spark.quantum.linksfoundation.com/"
quantum_computer = "default"

provider = IQMProvider(iqm_url, quantum_computer=quantum_computer, token = api_token)
backend = provider.get_backend()

# Here define your circuit
from qiskit import QuantumCircuit
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.measure([0,1],[0,1])

# Transpile the circuit
transpiled_circuit = transpile(circuit, backend=backend)
job = backend.run([transpiled_circuit], shots=1024)
counts = job.result().get_counts()
```