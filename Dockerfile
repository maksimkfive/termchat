FROM python:3.11-slim

WORKDIR /app

# Копируем только то, что нужно для сервера
COPY protocol.py server.py ./

EXPOSE 6000

ENTRYPOINT ["python3", "server.py"]
CMD ["6000"]
