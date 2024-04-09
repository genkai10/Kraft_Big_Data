

records_store = {
    "RegisterBrokerRecords": {
        "records": [],
        "timestamp": "",  
        # Additional fields if needed for RegisterBrokerRecord
        "fields": {
            "internalUUID": "",
            "brokerId": 0,
            "brokerHost": "",
            "brokerPort": "",
            "securityProtocol": "",
            "brokerStatus": "",
            "rackId": "",
            "epoch": 0
        }
    },
    "TopicRecords": {
        "records": [],
        "timestamp": "",
        # Additional fields if needed for TopicRecord
        "fields": {
            "topicUUID": "",
            "name": ""
        }
    },
    "PartitionRecords": {
        "records": [],
        "timestamp": "",
        # Additional fields if needed for PartitionRecord
        "fields": {
            "partitionId": 0,
            "topicUUID": "",
            "replicas": [],
            "ISR": [],
            "removingReplicas": [],
            "addingReplicas": [],
            "leader": "",
            "partitionEpoch": 0
        }
    },
    "ProducerIdsRecords": {
        "records": [],
        "timestamp": "",
        # Additional fields if needed for ProducerIdsRecord
        "fields": {
            "brokerId": "",
            "brokerEpoch": 0,
            "producerId": 0
        }
    },
    "BrokerRegistrationChangeRecords": {
        "records": [],
        "timestamp": "",
        # Additional fields if needed for BrokerRegistrationChangeBrokerRecord
        "fields": {
            "brokerId": "",
            "brokerHost": "",
            "brokerPort": "",
            "securityProtocol": "",
            "brokerStatus": "",
            "epoch": 0
        }
    }
    # Add more record types if needed using a similar structure
}
