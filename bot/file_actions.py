import logging
import aiofiles as aiof

logger = logging.getLogger(__name__)

async def load_file(file_path):
    try:
        async with aiof.open(file_path, "r") as f:
            file = await f.read()
            await f.flush()
        return file
    except Exception as e:
        logger.critical(e)
        return False


async def write_file(file_path, what_to_write):
    try:
        async with aiof.open(file_path, "w") as f:
            await f.write(what_to_write)
            await f.flush()
        return True
    except Exception as e:
        logger.error(e)
        return False
