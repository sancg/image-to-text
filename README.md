# 🍃 OCR - technical test

This project automates the extraction of invoices (images) and formatted in a structured Data using python.

---

## Usage 🧑‍💻

The core test using python is inside the folder scripts:

### Requirements:

To use the python scripts you'll need to setting up a virtual environment to install the required dependencies:

```shell
python -m venv root_directory
# Activate the venv to install the dependencies
python -m pip install -r requirements.txt
```

Create a **_.env_** file within the **scripts** folder with the corresponding VARIABLES for the veryfi API. Otherwise, the code won't work:

- CLIENT_ID
- CLIENT_SECRET
- USERNAME
- API_KEY

## To start the project
From the root directory type in terminal: `python .\scripts\main.py`

## Stage 🌱

- [x] Exploration phase
  - [x] Breaking down the requirements.
  - [x] Modeling the objects to make use of (UML).
- [ ] Creating the obj to get all data needed:
  - [x] vendor_name
  - [ ] bill_to_address
  - [x] ship_to_name
  - [x] ship_to_address
  - [x] line_items [dict]
    - Quantity
    - Description
    - Price
- [ ] [Additional] API Verify integration Next.js with python scripting.

### Dependencies

- Created with `npx create-next-app@latest`
- ```
    veryfi
    autopep8
    python-dotenv
  ```

### How to contribute

To use this project run the commands:

```
    npm install / yarn install
```

Want to contribute? Great! ✨

To fix a bug or enhance an existing module, follow these steps:

- Clone / Fork the repo.
- Create a new branch `git checkout -b improve-feature`
- Make the appropriate changes in the files.
- Commit your changes `git commit -am 'Improve feature`
- Push to the branch `git push origin improve-feature`
- Create a Pull Request

## Feedback

If you have any feedback or suggestion, please reach out to mr.santiago.cano@gmail.com
