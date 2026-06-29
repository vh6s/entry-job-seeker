

KNOWN_TECHNOLOGIES = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node.js",
    "django",
    "flask",
    "fastapi",
    "spring",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "aws",
    "azure",
    "gcp",
    "html",
    "css",
    "rest",
    "graphql",
    "mcp",
}

def extract_technologies(description: str) -> list[str]:
    text = description.lower()

    return sorted(technology for technology in KNOWN_TECHNOLOGIES if technology.lower() in text)