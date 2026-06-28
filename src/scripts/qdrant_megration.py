from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import time
from src.helpers.config import get_settings

settings = get_settings()

QDRANT_CLOUD_URL = settings.QUADRANT_END_POINT_CLUSTER
QDRANT_CLOUD_API_KEY = settings.QUADRANT_KEY_CLUSTER
collection_name = "books_chunks"
BATCH_SIZE = 100

print("Connecting to local Qdrant...")
local_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

print("Connecting to Qdrant Cloud...")
cloud_client = QdrantClient(
    url=QDRANT_CLOUD_URL,
    api_key=QDRANT_CLOUD_API_KEY,
)

# Get collection info from local
print(f"Getting collection info: {collection_name}")
collection_info = local_client.get_collection(collection_name=collection_name)
vector_size = collection_info.config.params.vectors.size
distance = collection_info.config.params.vectors.distance

print(f"   Vector size: {vector_size}")
print(f"   Distance: {distance}")

# Create collection on cloud if not exists
if not cloud_client.collection_exists(collection_name):
    print(f"✨ Creating collection on Qdrant Cloud...")
    cloud_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance),
    )
else:
    print("Collection already exists on cloud")

# Migrate points in batches
print(f" Starting migration...")
offset = None
total_migrated = 0

while True:
    results = local_client.scroll(
        collection_name=collection_name,
        limit=BATCH_SIZE,
        offset=offset,
        with_vectors=True,
        with_payload=True,
    )

    points, next_offset = results

    if not points:
        break

    # Convert Records → PointStruct
    formatted_points = [
        PointStruct(id=p.id, vector=p.vector, payload=p.payload)
        for p in points
    ]

    cloud_client.upsert(
        collection_name=collection_name,
        points=formatted_points,
    )

    total_migrated += len(points)
    print(f" Migrated {total_migrated} points...")

    if next_offset is None:
        break

    offset = next_offset
    time.sleep(0.1)

print(f"\n Migration complete! Total points migrated: {total_migrated}")

# Verify
cloud_count = cloud_client.count(collection_name=collection_name)
print(f" Verified on cloud: {cloud_count.count} points")
