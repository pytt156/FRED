import json

AUDIO_START_TOPIC = "fred/audio/start"
AUDIO_CHUNK_TOPIC = "fred/audio/chunk"
AUDIO_END_TOPIC = "fred/audio/end"

CHUNK_SIZE = 4096


def publish_audio(client, audio_bytes: bytes):
    metadata = {
        "sample_rate": 24000,
        "bits": 16,
        "channels": 1,
        "size": len(audio_bytes),
    }

    client.publish(
        AUDIO_START_TOPIC,
        json.dumps(metadata),
    )

    for offset in range(0, len(audio_bytes), CHUNK_SIZE):
        chunk = audio_bytes[offset : offset + CHUNK_SIZE]
        client.publish(AUDIO_CHUNK_TOPIC, chunk)

    client.publish(AUDIO_END_TOPIC, b"")
