FROM docker.io/python

WORKDIR /app
COPY . ./
RUN pip install uv && uv sync

EXPOSE 5000 
CMD ["uv", "run", "flask", "run", "--debug"]
