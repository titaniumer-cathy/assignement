# 📝 Prompt Management Pipeline

A streamlined pipeline for managing and deploying AI prompts with automated testing and cloud deployment.

## 🚀 Pipeline Overview

1. **Config Management**  
   `config_files/` ← Store YAML files with prompts and test requirements

2. **Automated Validation**  
   Workflow step 1 → `pytest` evaluation

3. **Cloud Deployment** \
    Run cloud deployment if all tests passed. Will keep cloud files the same as config_files \
    Workflow step 2 → Deploy to AWS S3

4. **Production Access**  
   AWS API → Access validated prompts via `main.py`

## 🛠️ Usage Guide

### 1. Manage Prompts
```bash
# Add/Modify/Delete config files
vim config_files/my_prompt.yaml
```
### 2. Local Test(optional)
```bash
export OPENAI_API_KEY="your-api-key"
pytest -s -v --log-cli-level=INFO test.py
```
### 3. Commit & Deploy
```bash
git add .
git commit -m "Add new prompt configuration"
git push origin main
```
Observe Run Status in "Action" section on github
### 4. Use prompt store in cloud with main.py
```bash
python3 main.py
```