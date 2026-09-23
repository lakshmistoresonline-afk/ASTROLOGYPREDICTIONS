# Community Web3 Ephemeris Oracle Node Container
FROM python:3.11-slim

WORKDIR /oracle_node

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV NODE_ROLE="WEB3_ORACLE_CONSENSUS_NODE"

CMD ["python", "node_runner.py"]
