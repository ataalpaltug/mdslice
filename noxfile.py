import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.8", "3.10", "3.12"])
def tests(session: nox.Session) -> None:
    """Run tests."""
    # Install the project and its development dependencies
    session.run(
        "uv",
        "sync",
        "--group",
        "dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # Run the tests
    session.run("pytest", *session.posargs)
