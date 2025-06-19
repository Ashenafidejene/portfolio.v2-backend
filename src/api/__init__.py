from .routers import llm, projects, greet, comments

routers = [
    llm.router,
    projects.router,
    greet.router,
    comments.router
]