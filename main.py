import uvicorn


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    uvicorn.run("app.app:app", port=8000, reload=True)
