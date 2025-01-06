# Deployment Instructions

This guide outlines the steps to deploy the `sync_stock_levels.py` script on a Windows Server for automated synchronization of stock levels to the Luminovo API.

---

## Prerequisites

1. **Python Installation**:
   - Download and install Python 3.8+ from [python.org](https://www.python.org/).
   - During installation, ensure you check the option to **Add Python to PATH**.

2. **Required Libraries**:
   - Open Command Prompt or PowerShell and run:
     ```bash
     pip install pandas requests openpyxl
     ```

3. **Script and File Setup**:
   - Save the `sync_stock_levels.py` script in a directory (e.g., `C:\LuminovoSync\`).
   - Place the exported `Availability.xlsx` file in the same directory or update the `INPUT_FILE` variable in the script to match the file location.

4. **API Key Configuration**:
   - Open the script and replace `your_api_key_here` with the API key provided by Luminovo.

---

## Scheduling the Script

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and press Enter.

2. **Create a New Task**:
   - Click **Create Task** in the right-hand panel.
   - Name the task (e.g., `Luminovo Stock Sync`).

3. **Set Triggers**:
   - Go to the **Triggers** tab and click **New**.
   - Set the task to run **daily** at the desired time (e.g., 2:00 AM).

4. **Set the Action**:
   - Go to the **Actions** tab and click **New**.
   - Choose **Start a Program**.
   - In the **Program/script** field, enter the path to the Python executable (e.g., `C:\Python39\python.exe`).
   - In the **Add arguments** field, enter the path to the script:
     ```bash
     C:\LuminovoSync\sync_stock_levels.py
     ```

5. **Configure General Settings**:
   - In the **General** tab, ensure the task is set to run **whether the user is logged on or not**.
   - Provide the server’s admin credentials when prompted.

6. **Test the Task**:
   - Right-click the task and select **Run**.
   - Verify success by checking the `sync_log.log` file in the script directory.

---

## Testing and Verification

1. **Manual Testing**:
   - Open Command Prompt or PowerShell, navigate to the script directory:
     ```bash
     cd C:\LuminovoSync
     ```
   - Run the script manually:
     ```bash
     python sync_stock_levels.py
     ```

2. **Check Logs**:
   - Logs are stored in `sync_log.log`. Verify the sync process or troubleshoot errors.

---
