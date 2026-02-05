# ☁️ AWS EC2 Night Watchman (Cost Optimizer)

[![aws-environment-scheduler CI](https://github.com/emredogan-cloud/aws-environment-scheduler/actions/workflows/main.yaml/badge.svg)](https://github.com/emredogan-cloud/aws-environment-scheduler/actions/workflows/main.yaml)

**Night Watchman** is a Python-based automation tool designed to optimize AWS costs by managing the lifecycle of EC2 instances. It automatically identifies development servers based on specific tags and toggles their state (Stop/Start) to prevent unnecessary billing during off-hours.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AWS](https://img.shields.io/badge/AWS-Boto3-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

* **Smart Filtering:** Targets only specific instances using AWS Tags (e.g., `Environment: Dev`), leaving production servers untouched.
* **State Awareness:** Checks the current state of instances (Running/Stopped) before attempting any action to avoid API errors.
* **Safety Mechanisms:** Uses `wait_until_stopped` and `wait_until_running` waiters to ensure operations are completed successfully.
* **Interactive CLI:** Simple menu-driven interface to choose between "Night Mode" (Stop) and "Morning Mode" (Start).
* **Modular Design:** Built with functional programming principles for easy maintenance and scalability.

## 🛠️ Prerequisites

Before running this project, ensure you have the following:

* **Python 3.x** installed.
* **AWS CLI** installed and configured with appropriate permissions (`AmazonEC2FullAccess` or similar).
    * Run `aws configure` to set up your credentials and region.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/emredogan-cloud/aws-night-watchman.git](https://github.com/emredogan-cloud/aws-night-watchman.git)
    cd aws-night-watchman
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

By default, the script targets instances with the following tag:
* **Key:** `Environment`
* **Value:** `Dev`

To change this target, open `yonetici.py` and modify the `custom_filter` variable:

```python
custom_filter = [
    {
        "Name": "tag:YourTagName",
        "Values": ["YourTagValue"]
    }
]
