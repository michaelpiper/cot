from ...utils.cot_cli import CoTCLI

async def start_cli():
    from ..dependencies import container, engine
    container.wire(modules=[__name__])
    await engine.init()
    cli = CoTCLI()
    await cli.run_async(engine)