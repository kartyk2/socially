"# socially" 

Insatallation-steps:

    git clone https://github.com/kartyk2/socially.git
    cd socially
    python -m venv "venv"
    pip install -r requirements.txt
    uvicorn main:app --reload # to start server
    install live server on VS code
    goto: "localhost:5050/websocket_client.html" 
    