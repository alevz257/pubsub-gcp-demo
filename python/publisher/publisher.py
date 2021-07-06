"""TODO(alevz): DO NOT SUBMIT without one-line documentation for publisher.

TODO(alevz): DO NOT SUBMIT without a detailed description of publisher.
"""

import argparse

def publish_messages(project_number, cloud_region, zone_id, topic_id, message_data):
  #start
  from google.cloud.pubsublite.cloudpubsub import PublisherClient
  from google.cloud.pubsublite.types import (
      CloudRegion,
      CloudZone,
      MessageMetadata,
      TopicPath,
  )

  location = CloudZone(CloudRegion(cloud_region), zone_id)
  topic_path = TopicPath(project_number, location, topic_id)

  with PublisherClient() as publisher_client:
    data = message_data
    api_future = publisher_client.publish(topic_path, data.encode("utf-8"))

    message_id = api_future.result()
    message_metadata = MessageMetadata.decode(message_id)
    print(
        f"Published a messasge to partition {message_metadata.partition.value} and offset {message_metadata.cursor.offset}."
    )

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description =__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument("project_number", help="Your Google Cloud Project Number, 966837857153")
  parser.add_argument("cloud_region", help="Your Cloud Region, 'asia-southeast2'")
  parser.add_argument("zone_id", help="Your zone id, 'b'")
  parser.add_argument("topic_id", help="Your topic id, 'demo-pubsub-lite'")
  parser.add_argument("message_data", help="Please put some message")

  args = parser.parse_args()

  publish_messages(
    args.project_number, args.cloud_region, args.zone_id, args.topic_id, args.message_data,
  )

