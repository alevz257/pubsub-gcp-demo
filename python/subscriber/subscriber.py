"""TODO(alevz): DO NOT SUBMIT without one-line documentation for subscriber.

TODO(alevz): DO NOT SUBMIT without a detailed description of subscriber.
"""

import argparse

from google.cloud.pubsublite.types import MessageMetadata
from google.pubsub_v1 import PubsubMessage

def recieve_messages(
    project_number, cloud_region, zone_id, subscription_id, timeout=60
):

  from concurrent.futures._base import TimeoutError
  from google.cloud.pubsublite.cloudpubsub import SubscriberClient
  from google.cloud.pubsublite.types import (
      CloudRegion,
      CloudZone,
      FlowControlSettings,
      SubscriptionPath,
  )

  location = CloudZone(CloudRegion(cloud_region), zone_id)
  subscription_path = SubscriptionPath(project_number, location, subscription_id)

  per_partition_flow_control_settings = FlowControlSettings(
      messages_outstanding=1000,
      bytes_outstanding=10 * 1024 * 1024,
  )

  def callback(message: PubsubMessage):
    message_data = message.data.decode("utf-8")
    metadata = MessageMetadata.decode(message.message_id)
    print(f"Received ~ {message_data} ~ of ordering key {message.ordering_key} with id {metadata}.")
    message.ack()

  with SubscriberClient() as subscriber_client:

    streaming_pull_future = subscriber_client.subscribe(
        subscription_path,
        callback=callback,
        per_partition_flow_control_settings=per_partition_flow_control_settings,
    )

    print(f"Listening for messages on {str(subscription_path)}..")

    try:
      streaming_pull_future.result(timeout=timeout)
    except TimeoutError or keyboardInterrupt:
      streaming_pull_future.cancel()
      assert streaming_pull_future.done()

if __name__=="__main__":
  parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  project_number_var = "" #input your project number 

  #parser.add_argument("project_number", default='966837857153',type=str, help="You Google Cloud Project Number")
  parser.add_argument("cloud_region", default='asia-southeast2', help="Your Cloud Region, 'asia-southeast2'")
  parser.add_argument("zone_id", default='b', help="Your zone ID, 'b'")
  parser.add_argument("subscription_id", default='demo-pubsub-lite-sub', help="Your subscription ID, demo-pubsub-lite-sub")

  parser.add_argument(
      "timeout",
      nargs="?",
      default=60,
      type=int,
      help="Timeout in second (default to 60s)",
  )

  args = parser.parse_args()

  recieve_messages(
      project_number_var,
      args.cloud_region,
      args.zone_id,
      args.subscription_id,
      args.timeout,
  )
