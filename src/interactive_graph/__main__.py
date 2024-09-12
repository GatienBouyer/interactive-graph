import uvicorn  # type: ignore[import-not-found]

if __name__ == "__main__":
    uvicorn.run(
        "interactive_graph.app:app",
        port=5000,
        host="0.0.0.0",
        log_level="info",
        reload=True,
        reload_dirs=["src/interactive_graph"],
    )
