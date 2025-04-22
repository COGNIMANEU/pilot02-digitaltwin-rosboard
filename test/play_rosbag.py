#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rosbag2_py import SequentialReader
from rosbag2_py import StorageOptions, ConverterOptions
import os
import sys  # Import sys to access stdout.flush()

def play_rosbag(bag_file):
    rclpy.init()
    node = Node('rosbag_player')

    # Print and immediately flush
    print(f"Playing the rosbag: {bag_file}", end='', flush=True)

    # Setup rosbag reader
    storage_options = StorageOptions(uri=bag_file, storage_id="sqlite3")
    converter_options = ConverterOptions("", "")
    reader = SequentialReader()
    reader.open(storage_options, converter_options)

    # Read and publish messages from the bag file
    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        print(f"Publishing to topic {topic}", end='', flush=True)
        publisher = node.create_publisher(type(data), topic, 10)
        publisher.publish(data)

    rclpy.spin_once(node)

    # Clean up after finishing
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Play a rosbag or mcap file")
    parser.add_argument('--bag-file', type=str, required=True, help="Path to the rosbag or mcap file")
    args = parser.parse_args()

    # If the environment variable for BAG_FILE_PATH is set, use that
    bag_file_path = os.environ.get('BAG_FILE_PATH', args.bag_file)

    try:
        play_rosbag(bag_file_path)
    except Exception as e:
        print(f"Error playing the rosbag: {e}", end='', flush=True)
