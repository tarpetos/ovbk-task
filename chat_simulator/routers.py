from typing import Dict, Union
from fastapi import Request, Form
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from .config import router, templates, chat_data, active_connections
from .utils import find_user, generate_fake_data, write_to_txt


@router.get("/")
async def login(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/chat")
async def chat(
        request: Request, username: str = Form(...), password: str = Form(...)
) -> templates.TemplateResponse:
    user = find_user(username, password)
    if user:
        return templates.TemplateResponse(
            "chat.html",
            {"request": request, "username": username, "chat_data": chat_data},
        )
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "message": "Invalid username or password"},
        )


@router.get("/register")
async def register(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_model=None)
async def register_user(
        username: str = Form(...),
        password: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        address: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        number_of_accounts: int = Form(...),
) -> Union[RedirectResponse, HTMLResponse]:
    if number_of_accounts == 1:
        write_to_txt({
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "email": email,
            "phone": phone,
        })
        redirect_url = f"/chat?username={username}"
        return RedirectResponse(url=redirect_url)
    else:
        registered_users = []

        for _ in range(number_of_accounts):
            fake_data = generate_fake_data()
            write_to_txt(fake_data)
            registered_users.append(fake_data["username"])
        popup_message = (
            f"Registered {number_of_accounts} users: {', '.join(registered_users)}"
        )
        alert_script = f"""
            <script>
                alert('{popup_message}');
                window.location.href = '/';
            </script>
        """
        return HTMLResponse(content=alert_script)


@router.get("/insert_fake_data")
async def insert_fake_data() -> Dict[str, str]:
    fake_data = generate_fake_data()
    return fake_data


@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str) -> None:
    await websocket.accept()
    active_connections[username] = websocket

    while True:
        try:
            message = await websocket.receive_text()
            chat_data.append({"username": username, "message": message})

            for user, user_ws in active_connections.items():
                if user_ws != websocket:
                    await user_ws.send_text(f"{username}: {message}")
        except WebSocketDisconnect:
            del active_connections[username]
            break
