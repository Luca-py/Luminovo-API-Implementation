# User Guide

This document provides instructions for using and maintaining the `sync_stock_levels.py` script, which automates stock synchronization to the Luminovo API.

---

## Purpose

The script reads stock information from a daily exported Excel file and sends the data to the Luminovo API in the required format.

---

## Workflow

1. **Daily Execution**:
   - The script processes the `Availability.xlsx` file, which must be placed in the configured directory.
   - The script transforms the data into a JSON payload and sends it to the API.

2. **Scheduled Automation**:
   - The script is executed automatically via Windows Task Scheduler, based on the configured schedule.

3. **Logging**:
   - All operations are logged in `sync_log.log`, including any errors or successful executions.

---

## Configuration

1. **API Key**:
   - Update the `API_KEY` variable in the script with the key provided by Luminovo.

2. **Excel File Path**:
   - Update the `INPUT_FILE` variable in the script to reflect the location of the `Availability.xlsx` file.

3. **Excel File Structure**:
   - Ensure the following columns exist in the sheets:
     - **Sheet1**: `Available Stock`, `Total Stock`, `Unit Price`, `Internal Part Number`.
     - **Sheet2**: `Internal part number (IPN) from BOM`, `Customer Name`, `Supplier Name`, etc.

---

## Troubleshooting

1. **Common Issues**:
   - **Invalid API Key**: Ensure the correct API key is set in the script.
   - **Script Execution Errors**: Check Python installation and required libraries.

2. **Logs**:
   - Refer to the `sync_log.log` file for detailed information on script execution and errors.

3. **Manual Testing**:
   - Run the script manually using:
     ```bash
     python sync_stock_levels.py
     ```

---

## Maintenance

1. **API Updates**:
   - If Luminovo updates the API, modify the `transform_data()` function to match the new JSON structure.

2. **Excel Format Changes**:
   - If the ERP system changes the structure of the exported Excel file, update the script to match the new column names or formats.

---

## Contacts

For additional support, contact your system administrator or Luminovo’s support team.
