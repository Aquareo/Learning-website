# Learning-website
This is a programming learning record.

## Project Overview
This project is a personal learning website that serves as a record of programming knowledge and includes a module on the Floyd Cycle Detection algorithm. The backend is built using Python's Flask framework, and the frontend is designed to be visually appealing.

## Project Structure
```
Learning-website
├── backend
│   ├── app.py                # Entry point for the Flask application
│   ├── requirements.txt       # Python dependencies
│   └── modules
│       ├── __init__.py       # Marks the modules directory as a Python package
│       └── floyd_cycle.py     # Implementation of Floyd's Cycle Detection algorithm
├── frontend
│   ├── index.html            # Main HTML page of the website
│   ├── styles
│   │   └── style.css         # Styles for the website
│   └── scripts
│       └── app.js            # Frontend JavaScript code for user interaction
├── .devcontainer
│   ├── devcontainer.json      # Configuration for the development container
│   └── Dockerfile             # Docker image build process for the development environment
├── .github
│   └── workflows
│       └── deploy.yml         # GitHub Actions workflow for automated deployment
├── .gitignore                 # Files and directories to ignore in version control
└── README.md                  # Documentation and project description
```

## Features
- **Knowledge Modules**: Organized sections for different programming topics.
- **Floyd Cycle Detection**: A dedicated module explaining and implementing the Floyd Cycle Detection algorithm.
- **Responsive Design**: A user-friendly interface that adapts to different screen sizes.

## Getting Started
1. Clone the repository.
2. Navigate to the `backend` directory and install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```
4. Open `frontend/index.html` in a web browser to view the website.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or suggestions.