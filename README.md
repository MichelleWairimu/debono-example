<div align="center">
<h1>
DeBono Example
</h1>

Built with `asyncflows`

[![main repo](https://img.shields.io/badge/main_repo-1f425f)](https://github.com/asynchronous-flows/asyncflows)
[![Discord](https://img.shields.io/badge/discord-7289da)](https://discord.gg/AGZ6GrcJCh)

</div>

## Introduction

This example demonstrates how to use the DeBono flow to analyze a problem.

It consists of five parallelized prompt calls, and a final prompt call to synthesize the results.

<div align="center">
<img width="1079" alt="debono" src="https://github.com/asynchronous-flows/asyncflows/assets/24586651/0768b653-efbf-44ce-b9ae-53dae6266a30">
</div>

## Running the Example

To run the example:

1. Set up [Ollama](https://github.com/asynchronous-flows/asyncflows#setting-up-ollama-for-local-inference) or configure [another language model](https://github.com/asynchronous-flows/asyncflows#using-any-language-model)  

2. Clone the repository

```bash
git clone ssh://git@github.com/asynchronous-flows/debono-example
```

3. Change into the directory

```bash
cd debono-example
```

4. Create and activate your virtual environment (with, for example)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

5. Install the dependencies

```bash
pip install -r requirements.txt
```

Now, either:

### Run the Script

To see output in the terminal, run:

```bash
python debono.py
```

### Run the Gradio App

To start a web interface, run:

```bash
python gradio_app.py
```
# debono-example
