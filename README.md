# meshtastic-juniper

This simple project puts the power of Google's freely available Gemma 3 model on-mesh.

Just connect any Meshtastic hardware to your (decently-powered) PC and you will have a completely off-grid, on-mesh LLM chatbot that works without any Internet connection.

Default model prompt is written in Italian, because this was made primarily to provide my local mesh network with a fun and useful tool for propagation testing and general experimentation. Feel free to change it as you wish, but please don't remove the instructions about keeping messages short. The mesh doesn't need to be recklessly flooded by AI slop!

## Usage

Prepare a virtual environment and install the required packages:
```
python3 -m venv .venv
source .venv/bin/activate
pip install ollama meshtastic
```

Then, install Ollama. After installation, customize the system prompt in the Modelfile, then create the "juniper" model:
```
ollama create juniper -f Modelfile.juniper
```

In juniper.service you have a systemd template which you can use, that also preloads the model to avoid first-message delays.

Have fun!

