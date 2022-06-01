import asyncio
from aio_pika import ExchangeType
import aio_pika
import PIL
from PIL import Image
import os
import io

async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        #print(message.body)
        image = Image.open(io.BytesIO(message.body))
        image.save('image.png')
        await asyncio.sleep(1)


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = "IMAGE_EXCHANGE"  # Твое название exchange 

    # Creating channel
    channel = await connection.channel()

    # Declaring queue
    input_exchange = await channel.declare_exchange(
        name=queue_name,  # Твое название exchange 
        type=ExchangeType.FANOUT,
        durable=True
    )
        
    output_queue = await channel.declare_queue(
        name=queue_name,  # Твое название exchange
        durable=True
    )

    await channel.set_qos(prefetch_count=100)
    await output_queue.bind(input_exchange)
    await output_queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())