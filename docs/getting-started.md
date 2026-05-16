# Getting Started

Getting started with OrbitalPlay is quick and easy. Follow these steps to set up your local "Quantum Playground".

## Prerequisites

- **Python 3.8+**
- A modern web browser (Chrome, Firefox, or Safari)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/elkins/orbital-play.git
   cd orbital-play
   ```

2. **Install dependencies:**
   We recommend using a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Running the App

Once the dependencies are installed, you can launch the Streamlit application:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

## Troubleshooting

- **ModuleNotFoundError:** Ensure you have activated your virtual environment and installed the dependencies.
- **PySCF Installation:** PySCF currently has limited support on Windows. We recommend using WSL2 or a Linux/macOS environment for the best experience.
nce.
